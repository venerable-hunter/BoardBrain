from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Card and Column Schemas
class Card(BaseModel):
    id: str
    title: str
    details: str


class Column(BaseModel):
    id: str
    title: str
    cardIds: List[str]


# Board Schemas
class BoardCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)


class BoardUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    columns_data: Optional[List[Column]] = None
    cards_data: Optional[Dict[str, Card]] = None


class BoardResponse(BaseModel):
    id: int
    user_id: int
    title: str
    columns_data: List[Column]
    cards_data: Dict[str, Card]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Health Schema
class HealthResponse(BaseModel):
    status: str


# AI Schemas
class AITestRequest(BaseModel):
    prompt: str = "What is 2 + 2?"


class AITestResponse(BaseModel):
    response: str


class CardUpdate(BaseModel):
    id: str
    title: str
    details: str


class ColumnUpdate(BaseModel):
    id: str
    title: str
    cardIds: List[str]


class AIBoardUpdate(BaseModel):
    columns: Optional[List[ColumnUpdate]] = None
    cards: Optional[Dict[str, CardUpdate]] = None


class AIChatRequest(BaseModel):
    message: str
    board_id: int
    user_id: int
    conversation_history: Optional[List[Dict[str, str]]] = None


class AIChatResponse(BaseModel):
    response: str
    board_update: Optional[AIBoardUpdate] = None
