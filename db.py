import sqlite3
import hashlib

DB_NAME = "DeepfakeGame.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        HighScore INTEGER DEFAULT 0
    )
    ''')

    # create Questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Questions (
        QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
        QuestionType TEXT NOT NULL,
        QuestionString TEXT NOT NULL
    )
    ''')

    # create Answers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Answers (
        AnswerID INTEGER PRIMARY KEY AUTOINCREMENT,
        QuestionID INTEGER NOT NULL,
        Correct BOOLEAN NOT NULL,
        AnswerString TEXT NOT NULL,
        Feedback TEXT NOT NULL,
        FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID)
    )
    ''')

    # create Leaderboard table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Leaderboard (
        BoardID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Score INTEGER DEFAULT 0,
        ScoreDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    ''')

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


    # add user to database
def add_user(username: str, password: str):
    # add user to database, return userID
    conn = get_connection()
    cursor = conn.cursor()

    # see if user already exists in db
    cursor.execute('''SELECT 1 FROM Users WHERE Username=?''', (username,))
    if cursor.fetchone() is not None:
        return -1
    hashed_pw = hash_password(password)

    cursor.execute('''
    INSERT INTO Users (Username, Password)
    VALUES (?, ?)
    ''', (username, hashed_pw))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def authenticate_user(username: str, password: str):
    # authenticate a user and return UserID
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute('''
    SELECT UserID 
    FROM Users 
    WHERE Username = ? AND Password = ?
    ''', (username, hashed_pw))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def add_question(question_type, question_string):
    # add a question to the database
    # type is either 'text', 'image', or 'video'

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Questions (QuestionType, QuestionString)
    VALUES (?, ?)
    ''', (question_type, question_string))
    conn.commit()
    return cursor.lastrowid


def add_answer(question_id, correct, answer_string, feedback):
    # add an answer to the database
    # answer_string: either text answer or path to media
    # feedback: Explanation why answer is correct/incorrect or why media is deepfake or not

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Answers (QuestionID, Correct, AnswerString, Feedback)
    VALUES (?, ?, ?, ?)
    ''', (question_id, correct, answer_string, feedback))
    conn.commit()
    return cursor.lastrowid


def update_leaderboard(user_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Leaderboard (UserID, Score)
    VALUES (?, ?)
    ''', (user_id, score))

    # update user's high score if higher
    cursor.execute('''
    UPDATE Users 
    SET HighScore = CASE 
        WHEN HighScore < ? THEN ? 
        ELSE HighScore 
    END 
    WHERE UserID = ?
    ''', (score, score, user_id))

    conn.commit()
    return cursor.lastrowid


def get_user_highscore(user_id):
    # get user's high score
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT HighScore FROM Users WHERE UserID = ?', (user_id,))
    return cursor.fetchone()[0]


def get_question_with_answers(question_id):
    # get a question and return and its answers
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT 
        q.QuestionString,
        q.QuestionType,
        a.AnswerString,
        a.Correct,
        a.Feedback
    FROM Questions q
    LEFT JOIN Answers a ON q.QuestionID = a.QuestionID
    WHERE q.QuestionID = ?
    ''', (question_id,))
    return cursor.fetchall()


def get_media_question_count():
    # get count of image and video questions
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT QuestionType, COUNT(*) 
    FROM Questions 
    WHERE QuestionType IN ('image', 'video')
    GROUP BY QuestionType
    ''')
    return cursor.fetchall()


def get_questions_by_type(question_type):
    # get all questions of a specific type
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT QuestionID, QuestionString
    FROM Questions
    WHERE QuestionType = ?
    ''', (question_type,))
    return cursor.fetchall()


def get_leaderboard(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT u.Username, l.Score, l.ScoreDate
    FROM Leaderboard l
    JOIN Users u ON l.UserID = u.UserID
    ORDER BY l.Score DESC
    LIMIT ?
    ''', (limit,))
    return cursor.fetchall()


def examples():
    # create db
    init_db()
    # adding a user
    uid = add_user("bloop", 1)
    if uid != -1:
        print("user added to db")
    else:
        print("user already exists")

    # adding question & answers
    qid = add_question('text', 'example question')
    add_answer(qid, True, "Answer1", "feedback1")
    add_answer(qid, False, "Answer2", "feedback2")

    # displaying questions and answers
    answers = get_question_with_answers(qid)
    print(answers[0][0]) # print the question itself
    for answer in answers:
        print(answer[2])


# example api call for backend
#@app.route('/api/question/<int:question_id>', methods=['GET'])
#def api_get_question(question_id):
   # return jsonify(get_question_with_answers(question_id)), 200  return jsonified list of answers
