const API_BASE = "/api";

export interface User {
  id: number;
  username: string;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Card {
  id: string;
  title: string;
  details: string;
}

export interface Column {
  id: string;
  title: string;
  cardIds: string[];
}

export interface Board {
  id: number;
  user_id: number;
  title: string;
  columns_data: Column[];
  cards_data: Record<string, Card>;
  created_at: string;
  updated_at: string;
}

// Authentication
export async function registerUser(username: string, password: string): Promise<User> {
  const response = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Registration failed");
  }

  return response.json();
}

export async function loginUser(username: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
}

// Boards
export async function getBoards(userId: number): Promise<Board[]> {
  const response = await fetch(`${API_BASE}/boards?user_id=${userId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch boards");
  }

  return response.json();
}

export async function getBoard(boardId: number, userId: number): Promise<Board> {
  const response = await fetch(`${API_BASE}/boards/${boardId}?user_id=${userId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch board");
  }

  return response.json();
}

export async function createBoard(userId: number, title: string): Promise<Board> {
  const response = await fetch(`${API_BASE}/boards?user_id=${userId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    throw new Error("Failed to create board");
  }

  return response.json();
}

export async function updateBoard(
  boardId: number,
  userId: number,
  updates: {
    title?: string;
    columns_data?: Column[];
    cards_data?: Record<string, Card>;
  }
): Promise<Board> {
  const response = await fetch(`${API_BASE}/boards/${boardId}?user_id=${userId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    throw new Error("Failed to update board");
  }

  return response.json();
}

export async function deleteBoard(boardId: number, userId: number): Promise<void> {
  const response = await fetch(`${API_BASE}/boards/${boardId}?user_id=${userId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete board");
  }
}

// AI Chat
export interface AIChatRequest {
  message: string;
  board_id: number;
  user_id: number;
  conversation_history?: Array<{ role: string; content: string }>;
}

export interface AIChatResponse {
  response: string;
  board_update?: {
    columns?: Array<{ id: string; title: string; cardIds: string[] }>;
    cards?: Record<string, { id: string; title: string; details: string }>;
  };
}

export async function chatAI(request: AIChatRequest): Promise<AIChatResponse> {
  const response = await fetch(`${API_BASE}/ai/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Failed to chat with AI");
  }

  return response.json();
}
