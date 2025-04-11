from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_game_route():
    return {"message": "Game routes are working!"}
