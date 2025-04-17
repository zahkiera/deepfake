from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import route files once created
from routes import auth, game, leaderboard, media

app = FastAPI(title="Deepfake Detection Game API")

# Mount static files at /assets
app.mount("/media", StaticFiles(directory="Media"), name="media")

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