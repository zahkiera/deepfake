from fastapi import APIRouter, Request
from pydantic import BaseModel
from db import get_connection
from db import update_leaderboard

router = APIRouter()

class SubmitRequest(BaseModel):
    user_id: int
    question_id: int
    selected_id: int
    correct_id: int
    score_earned: int

@router.post("/submit")
def submit_answer(data: SubmitRequest):
    #update leaderboard with score if user is not guest
    if data.user_id != -1:
        update_leaderboard(data.user_id, data.score_earned)
    return {
        "message": "Answer submitted.",
        "earned": data.score_earned
    }

@router.get("/random")
def get_random_question():
    conn = get_connection()
    cursor = conn.cursor()

    # Get a random question
    cursor.execute("SELECT * FROM Questions ORDER BY RANDOM() LIMIT 1")
    question = cursor.fetchone()


    if question is None: 
        return {"Error": "No questions found"}

    question_id, question_type, question_text = question

    # Get all associated answers
    cursor.execute("SELECT AnswerID, AnswerString FROM Answers WHERE QuestionID=?", (question_id,))
    answers = cursor.fetchall()

    return {
        "question_id": question_id,
        "question_type": question_type,
        "question_text": question_text,
        "answers": [{"id": aid, "text":atext} for (aid, atext) in answers]
    }
