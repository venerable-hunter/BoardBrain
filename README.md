# BoardBrain

An AI-powered Project Management MVP with a Kanban board interface. BoardBrain combines a traditional Kanban board with AI assistance to help you manage tasks more efficiently.

## Features

- **Kanban Board**: Drag-and-drop task management with 5 customizable columns
- **User Authentication**: Secure login system with password hashing
- **AI Chat Assistant**: Ask questions about your board or request AI to make changes
- **Persistent Storage**: SQLite database for reliable data persistence
- **Local AI Support**: Works with Ollama for private, local AI processing
- **Modern UI**: Beautiful interface built with NextJS and TailwindCSS
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Frontend
- **Framework**: NextJS 16.1.6 with React 19.2.3
- **Language**: TypeScript
- **Styling**: TailwindCSS v4
- **Drag & Drop**: @dnd-kit/core, @dnd-kit/sortable
- **Build**: Static export for Docker deployment

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: bcrypt password hashing
- **AI Integration**: OpenAI SDK (compatible with Ollama and OpenRouter)

## Prerequisites

- Python 3.12 or higher
- Node.js 18 or higher
- npm or yarn
- (Optional) Ollama for local AI processing

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/venerable-hunter/BoardBrain.git
cd BoardBrain
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run build
```

### 4. Copy Frontend Build to Backend

```bash
# From project root
cp -r frontend/out/* backend/static/
```

On Windows:
```powershell
Copy-Item -Path 'frontend\out\*' -Destination 'backend\static' -Recurse -Force
```

## Configuration

### AI Configuration

Create a `.env` file in the `backend/` directory:

```env
# Choose your AI provider: 'ollama' or 'openrouter'
AI_PROVIDER=ollama

# Ollama Configuration (for local AI)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2.5-coder:3b

# OpenRouter Configuration (alternative)
# OPENROUTER_API_KEY=your_openrouter_api_key_here
```

See `backend/.env.example` for more details.

## Usage

### Starting the Backend

```bash
cd backend
python main.py
```

The server will start on `http://localhost:8000`

### Using the Application

1. Open your browser and navigate to `http://localhost:8000`
2. Register a new account with any username and password
3. Login with your credentials
4. Start managing your Kanban board!

### Using AI Chat

1. Click the purple chat button in the bottom-right corner
2. Ask questions about your board (e.g., "What's in the backlog?")
3. Request AI to make changes (e.g., "Add a card called 'Review documentation' to backlog")
4. The AI will respond and optionally update your board

## Scripts

### Start/Stop Scripts

**Mac/Linux:**
```bash
./scripts/start.sh    # Start the server
./scripts/stop.sh     # Stop the server
```

**Windows:**
```cmd
scripts\start.bat    # Start the server
scripts\stop.bat     # Stop the server
```

### Frontend Scripts

```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
```

## Project Structure

```
BoardBrain/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── ai.py                # AI integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── static/              # Frontend build output
├── frontend/
│   ├── src/
│   │   ├── app/            # NextJS app directory
│   │   ├── components/     # React components
│   │   └── lib/            # Utility functions
│   ├── package.json
│   └── next.config.ts
├── scripts/                 # Start/stop scripts
├── docs/                    # Documentation
└── README.md
```

## Security Considerations

⚠️ **Important**: This is an MVP project with known security limitations:

- Authentication uses simple user ID tokens (not production-ready)
- No rate limiting on API endpoints
- No HTTPS configuration (use in development only)
- Session storage in sessionStorage (vulnerable to XSS)
- No CSRF protection
- Database file should be secured in production

**Do not use this in production without implementing proper security measures.**

See the security audit report in the project documentation for details.

## Development

### Running in Development Mode

For development, you can run the frontend and backend separately:

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Then update `frontend/src/lib/api.ts` to use `http://localhost:8000/api` for API calls.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [NextJS](https://nextjs.org/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- AI integration with [OpenAI SDK](https://github.com/openai/openai-python)
- UI components inspired by modern design patterns
