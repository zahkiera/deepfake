from fastapi import APIRouter
from db import get_leaderboard

router = APIRouter()

@router.get("/")
def leaderboard(limit: int = 10):
    return get_leaderboard(limit)
