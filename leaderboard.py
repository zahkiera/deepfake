from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_leaderboard_route():
    return {"message": "Leaderboard routes are working!"}