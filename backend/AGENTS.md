# Backend Documentation

## Overview
The backend is a FastAPI application that serves the static frontend and provides API endpoints for the Project Management MVP. It uses SQLite for data persistence.

## Tech Stack
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Language**: Python 3.12
- **Package Manager**: uv (in Docker)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **AI**: OpenRouter (via OpenAI SDK)

### main.py
FastAPI application entry point with:
- Health check route GET /api/health - Returns {"status": "ok"}
- Authentication endpoints (register, login)
- Board CRUD endpoints
- AI test endpoint
- Static file mounting at / for frontend build output

### database.py
Database connection and initialization:
- `get_db()` - Context manager for database connections
- `init_db()` - Creates users and boards tables
- `ensure_db_exists()` - Ensures database is initialized on startup
- Database file: `backend/kanban.db`

### ai.py
AI integration with OpenRouter:
- `call_ai(prompt, model)` - Call AI with a prompt
- Uses OpenAI SDK with OpenRouter base URL
- Requires OPENROUTER_API_KEY environment variable

### requirements.txt
Python dependencies:
- fastapi
- uvicorn[standard]
- python-multipart
- sqlalchemy
- pydantic
- bcrypt
- openai
- python-dotenv

### static/
Directory for serving static files (frontend build output)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Boards Table
```sql
CREATE TABLE boards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    columns_data TEXT NOT NULL,
    cards_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### JSON Storage
- `columns_data` - JSON array of column objects with id, title, cardIds
- `cards_data` - JSON object with card IDs as keys, containing id, title, details

See `docs/database-schema.md` for detailed schema documentation.

## Current API Endpoints

### GET /api/health
Health check endpoint that returns {"status": "ok"}

### POST /api/auth/register
Register a new user.
- Request body: {"username": string, "password": string}
- Response: User object with id, username, created_at
- Status: 201 Created

### POST /api/auth/login
Authenticate a user.
- Request body: {"username": string, "password": string}
- Response: {"access_token": string, "token_type": "bearer", "user": User object}
- For MVP, access_token is the user ID (in production, use JWT)

### GET /api/boards?user_id={user_id}
Get all boards for a user.
- Query param: user_id (integer)
- Response: Array of Board objects

### GET /api/boards/{board_id}?user_id={user_id}
Get a specific board.
- Path param: board_id (integer)
- Query param: user_id (integer)
- Response: Board object with columns_data and cards_data

### POST /api/boards?user_id={user_id}
Create a new board.
- Query param: user_id (integer)
- Request body: {"title": string}
- Response: Board object with 5 empty columns (Backlog, Discovery, In Progress, Review, Done)
- Status: 201 Created

### PUT /api/boards/{board_id}?user_id={user_id}
Update a board.
- Path param: board_id (integer)
- Query param: user_id (integer)
- Request body: {"title"?: string, "columns_data"?: Column[], "cards_data"?: Dict[str, Card]}
- Response: Updated Board object

### POST /api/ai/test
Test AI connectivity.
- Request body: {"prompt": string}
- Response: {"response": string}
- Default model: openai/gpt-4o-mini
- Requires OPENROUTER_API_KEY environment variable

### POST /api/ai/chat
Chat with AI with board context.
- Request body: {"message": string, "board_id": int, "user_id": int, "conversation_history": array}
- Response: {"response": string, "board_update": object or null}
- AI receives full board context (columns and cards)
- AI can optionally return board updates (add/modify cards or columns)
- Board updates are automatically saved to database
- Requires OPENROUTER_API_KEY environment variable

## Running the Backend

### Direct (without Docker)
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### With Docker
The Dockerfile in the project root builds and runs the backend automatically.

## Next Steps
- Add AI integration endpoints (Part 8)
- Extend AI with Kanban context (Part 9)