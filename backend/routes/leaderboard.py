from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_leaderboard, update_leaderboard

router = APIRouter()

@router.get("/")
def leaderboard(limit: int = 10):
    return get_leaderboard(limit)



class ScoreSubmission(BaseModel):
    user_id: int
    score: int

@router.post("/submit_score")
def submit_leaderboard_score(score_data: ScoreSubmission):
    try:
        if score_data.user_id != -1:
            leaderboard_id = update_leaderboard(score_data.user_id, score_data.score)
            return {"status": "success", "leaderboard_id": leaderboard_id}
        return {"status": "success", "message": "Guest score not recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))