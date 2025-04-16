from fastapi import APIRouter
from db import get_connection

router = APIRouter()

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
