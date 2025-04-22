from fastapi import APIRouter
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
    cursor.execute("SELECT AnswerID, Correct, AnswerString, Feedback FROM Answers WHERE QuestionID=?", (question_id,))
    answers = cursor.fetchall()

    return {
        "question_id": question_id,
        "question_type": question_type,
        "question_text": question_text,
        "answers": [{"id": aid, "correct":c, "text":atext, "feedback":f} for (aid,c, atext,f) in answers]
    }
