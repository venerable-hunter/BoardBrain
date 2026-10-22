# Frontend Documentation

## Overview
The frontend is a NextJS 16 application that displays a Kanban board with drag-and-drop functionality. It is built as a static site and served by the FastAPI backend.

## Tech Stack
- **Framework**: NextJS 16.1.6 with React 19.2.3
- **Language**: TypeScript
- **Styling**: TailwindCSS v4
- **Drag & Drop**: @dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities
- **Testing**: Vitest (unit tests), Playwright (e2e tests)
- **Build Tool**: NextJS built-in bundler with static export

## Project Structure

### src/app/
- `page.tsx` - Main page that renders the KanbanBoard component
- `layout.tsx` - Root layout wrapper
- `globals.css` - Global styles with CSS variables for the color scheme

### src/components/
- `KanbanBoard.tsx` - Main board component managing state and drag-drop context
- `KanbanColumn.tsx` - Individual column component with rename functionality
- `KanbanCard.tsx` - Individual card component with edit and delete
- `KanbanCardPreview.tsx` - Preview shown during drag operations
- `NewCardForm.tsx` - Form for adding new cards to a column
- `AIChatSidebar.tsx` - Collapsible sidebar for AI chat with board context

### src/lib/
- `kanban.ts` - Core data structures and logic:
  - Types: Card, Column, BoardData
  - initialData: Sample board data with 5 columns and 8 cards
  - moveCard(): Logic for moving cards between columns and reordering
  - createId(): Helper for generating unique IDs
- `kanban.test.ts` - Unit tests for kanban logic

### src/test/
- Test utilities and helpers

## Data Model

### Card
```typescript
{
  id: string;
  title: string;
  details: string;
}
```

### Column
```typescript
{
  id: string;
  title: string;
  cardIds: string[];
}
```

### BoardData
```typescript
{
  columns: Column[];
  cards: Record<string, Card>;
}
```

## Key Features
- 5 fixed columns: Backlog, Discovery, In Progress, Review, Done
- Drag and drop cards between columns
- Reorder cards within a column
- Rename columns
- Add new cards with title and details
- Delete cards
- Beautiful UI with gradient backgrounds and the specified color scheme

## Color Scheme (CSS Variables)
- `--accent-yellow`: #ecad0a
- `--primary-blue`: #209dd7
- `--secondary-purple`: #753991
- `--navy-dark`: #032147
- `--gray-text`: #888888
- `--surface`: #f7f8fb
- `--surface-strong`: #ffffff
- `--stroke`: rgba(3, 33, 71, 0.08)
- `--shadow`: 0 18px 40px rgba(3, 33, 71, 0.12)

## Current Limitations
- Authentication is client-side only (dummy credentials removed, now uses backend)
- Simple token-based auth (user ID as token for MVP)

## Authentication

The app uses backend authentication via FastAPI API.

### auth.ts Functions
- `login(username, password)` - Calls backend /api/auth/login, stores session and token
- `logout()` - Clears session, user, and token from sessionStorage
- `isAuthenticated()` - Checks if user is logged in
- `getUserId()` - Returns the logged-in user's ID
- `getToken()` - Returns the authentication token

### Session Management
- Uses sessionStorage to persist authentication state
- Stores: authenticated flag, user object, access token
- Session persists across page refreshes
- Session is cleared on logout

### Login Flow
1. User visits the app
2. If not authenticated, LoginForm is displayed
3. User enters credentials (any username/password for registration)
4. Frontend calls backend /api/auth/login
5. On success, stores user data and token in sessionStorage
6. KanbanBoard is displayed and loads user's board from backend
7. Logout button clears session and reloads page

### Components
- `LoginForm.tsx` - Login form with username/password fields and loading state
- `KanbanBoard.tsx` - Includes logout button in header

## API Integration

The frontend communicates with the FastAPI backend via REST API.

### api.ts Functions
- `registerUser(username, password)` - Register a new user
- `loginUser(username, password)` - Authenticate and get token
- `getBoards(userId)` - Get all boards for a user
- `getBoard(boardId, userId)` - Get a specific board
- `createBoard(userId, title)` - Create a new board
- `updateBoard(boardId, userId, updates)` - Update board data
- `deleteBoard(boardId, userId)` - Delete a board
- `chatAI(request)` - Send message to AI with board context

### Data Persistence
- Board data is loaded from backend on mount
- Changes are automatically saved to backend after drag, rename, add, or delete
- Loading state displayed while fetching data
- Error handling with console logging

### Board Loading Logic
1. On mount, check if user has any boards
2. If yes, load the first board
3. If no, create a new board with default columns
4. Display loading state during fetch
5. Display error if fetch fails

## Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production (static export)
- `npm run start` - Start production server
- `npm run test:unit` - Run unit tests with Vitest
- `npm run test:e2e` - Run e2e tests with Playwright
- `npm run test:all` - Run all tests

## Static Build Configuration

The frontend is configured for static export in `next.config.ts`:
```typescript
const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
};
```

This configuration:
- Generates static HTML/CSS/JS files in the `out/` directory
- Disables server-side rendering
- Disables image optimization (images are served as-is)

### Build Process
1. Run `npm run build` in the frontend directory
2. Static files are generated in `frontend/out/`
3. Copy `frontend/out/*` to `backend/static/`
4. FastAPI serves these static files from the `/` path

### Why Static Export?
- Simplifies deployment (no Node.js server needed)
- Works well with Docker containerization
- FastAPI can serve static files efficiently
- Reduces infrastructure complexity

## AI Chat Feature

The app includes an AI chat sidebar that allows users to interact with their Kanban board using natural language.

### AIChatSidebar Component
- Collapsible sidebar with toggle button (bottom-right corner)
- Chat message display with user/assistant differentiation
- Message input with send button
- Conversation history tracking
- Loading states during AI responses
- Error handling for failed AI calls

### AI Chat Integration
- AI receives full board context (columns and cards)
- AI can optionally return board updates via structured outputs
- Board updates are automatically applied to the UI
- Board updates are persisted to the backend
- Conversation history is maintained for context

### AI Chat Flow
1. User clicks chat button to open sidebar
2. User types a message and sends
3. Frontend calls /api/ai/chat with message, board_id, user_id, and conversation_history
4. Backend sends request to AI with full board context
5. AI responds with text response and optional board updates
6. Frontend displays AI response
7. If board updates provided, apply them to board state and save to backend

### AI Capabilities
- Answer questions about the board
- Suggest improvements to tasks
- Add new cards to columns
- Move cards between columns
- Rename columns
- Edit card details

## Next Steps for Integration
1. Configure for static build (for Docker serving)
2. Add authentication UI (login/logout)
3. Add API client to communicate with FastAPI backend
4. Add AI chat sidebar component
5. Integrate real-time updates when backend changes data
