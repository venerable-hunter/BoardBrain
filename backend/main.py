from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import os
import json
import bcrypt

from database import engine, get_db, ensure_db_exists
from models import User, Board, Base
from schemas import (
    UserCreate,
    UserResponse,
    UserLogin,
    LoginResponse,
    BoardCreate,
    BoardUpdate,
    BoardResponse,
    HealthResponse,
    AITestRequest,
    AITestResponse,
    AIChatRequest,
    AIChatResponse,
    AIBoardUpdate,
)
from ai import call_ai, call_ai_with_board

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(script_dir, "static")

app = FastAPI(title="Project Management MVP")


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    ensure_db_exists()


@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")


# Authentication endpoints
@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Create user
    db_user = User(username=user.username, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/api/auth/login", response_model=LoginResponse)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    # Find user
    db_user = db.query(User).filter(User.username == user_login.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Verify password
    if not bcrypt.checkpw(user_login.password.encode("utf-8"), db_user.password_hash.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # For MVP, use user ID as token (in production, use JWT)
    access_token = str(db_user.id)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=db_user.id,
            username=db_user.username,
            created_at=db_user.created_at
        )
    )


# Board endpoints
@app.get("/api/boards", response_model=List[BoardResponse])
async def get_boards(user_id: int, db: Session = Depends(get_db)):
    boards = db.query(Board).filter(Board.user_id == user_id).all()
    result = []
    for board in boards:
        result.append(BoardResponse(
            id=board.id,
            user_id=board.user_id,
            title=board.title,
            columns_data=json.loads(board.columns_data),
            cards_data=json.loads(board.cards_data),
            created_at=board.created_at,
            updated_at=board.updated_at
        ))
    return result


@app.get("/api/boards/{board_id}", response_model=BoardResponse)
async def get_board(board_id: int, user_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == user_id
    ).first()

    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    return BoardResponse(
        id=board.id,
        user_id=board.user_id,
        title=board.title,
        columns_data=json.loads(board.columns_data),
        cards_data=json.loads(board.cards_data),
        created_at=board.created_at,
        updated_at=board.updated_at
    )


@app.post("/api/boards", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(board: BoardCreate, user_id: int, db: Session = Depends(get_db)):
    # Create initial empty board data
    initial_columns = [
        {"id": "col-1", "title": "Backlog", "cardIds": []},
        {"id": "col-2", "title": "Discovery", "cardIds": []},
        {"id": "col-3", "title": "In Progress", "cardIds": []},
        {"id": "col-4", "title": "Review", "cardIds": []},
        {"id": "col-5", "title": "Done", "cardIds": []},
    ]

    db_board = Board(
        user_id=user_id,
        title=board.title,
        columns_data=json.dumps(initial_columns),
        cards_data=json.dumps({})
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    return BoardResponse(
        id=db_board.id,
        user_id=db_board.user_id,
        title=db_board.title,
        columns_data=json.loads(db_board.columns_data),
        cards_data=json.loads(db_board.cards_data),
        created_at=db_board.created_at,
        updated_at=db_board.updated_at
    )


@app.put("/api/boards/{board_id}", response_model=BoardResponse)
async def update_board(board_id: int, board_update: BoardUpdate, user_id: int, db: Session = Depends(get_db)):
    db_board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == user_id
    ).first()

    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    # Update fields if provided
    if board_update.title is not None:
        db_board.title = board_update.title
    if board_update.columns_data is not None:
        db_board.columns_data = json.dumps([col.model_dump() for col in board_update.columns_data])
    if board_update.cards_data is not None:
        db_board.cards_data = json.dumps({k: v.model_dump() for k, v in board_update.cards_data.items()})

    db.commit()
    db.refresh(db_board)

    return BoardResponse(
        id=db_board.id,
        user_id=db_board.user_id,
        title=db_board.title,
        columns_data=json.loads(db_board.columns_data),
        cards_data=json.loads(db_board.cards_data),
        created_at=db_board.created_at,
        updated_at=db_board.updated_at
    )


@app.delete("/api/boards/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(board_id: int, user_id: int, db: Session = Depends(get_db)):
    db_board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == user_id
    ).first()

    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    db.delete(db_board)
    db.commit()

    return None


# AI endpoints
@app.post("/api/ai/test", response_model=AITestResponse)
async def test_ai(request: AITestRequest):
    """Test endpoint to verify AI connectivity."""
    try:
        response = call_ai(request.prompt)
        return AITestResponse(response=response)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI call failed: {str(e)}"
        )


@app.post("/api/ai/chat", response_model=AIChatResponse)
async def chat_ai(request: AIChatRequest, db: Session = Depends(get_db)):
    """Chat with AI with board context."""
    try:
        # Get the board
        board = db.query(Board).filter(
            Board.id == request.board_id,
            Board.user_id == request.user_id
        ).first()

        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found"
            )

        # Prepare board data
        board_data = {
            "columns": json.loads(board.columns_data),
            "cards": json.loads(board.cards_data)
        }

        # Call AI with board context
        result = call_ai_with_board(
            request.message,
            board_data,
            request.conversation_history
        )

        # If board update is provided, save it
        if result.get("board_update"):
            board_update = result["board_update"]
            if board_update.get("columns"):
                board.columns_data = json.dumps(board_update["columns"])
            if board_update.get("cards"):
                board.cards_data = json.dumps(board_update["cards"])
            db.commit()

        return AIChatResponse(
            response=result.get("response", ""),
            board_update=result.get("board_update")
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI call failed: {str(e)}"
        )


# Mount static files directory if it exists (must be after API routes)
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
