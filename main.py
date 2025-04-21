from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import route files 
from routes import auth, game, leaderboard, media

app = FastAPI(title="Deepfake Detection Game API")

# Mount static files at /assets
app.mount("/media", StaticFiles(directory="Media"), name="media")

origins = [
    "http://localhost:5173",    # React dev server
    "http://127.0.0.1:5173",    # React dev server alternative URL
    "http://localhost:3000",    
    "http://127.0.0.1:3000",    
    "http://localhost:8080",    
    "http://127.0.0.1:8000",    
]

# Allow frontend (React, etc) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route files
app.include_router(auth.router, prefix="/api/user", tags=["User"])
app.include_router(game.router, prefix="/api/game", tags=["Game"])
app.include_router(leaderboard.router, prefix="/api/leaderboard", tags=["Leaderboard"])
app.include_router(media.router, prefix="/api/media", tags=["Media"])