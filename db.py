import sqlite3
import hashlib

from datetime import datetime, timezone
datetime.now(timezone.utc)

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
        FirstName TEXT,
        LastName TEXT,
        Email TEXT,
        HighScore INTEGER DEFAULT 0,
        LastEmailUpdate TEXT
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

    # create PasswordResetTokens table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PasswordResetTokens (
        Email TEXT PRIMARY KEY,
        Token TEXT NOT NULL,
        Expiry TIMESTAMP NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


    # add user to database
def add_user(username: str, password: str, first_name: str, last_name: str, email: str):
    # add user to database, return userID
    conn = get_connection()
    cursor = conn.cursor()

    # see if user already exists in db
    cursor.execute('''SELECT 1 FROM Users WHERE Username=?''', (username,))
    if cursor.fetchone() is not None:
        return -1
    hashed_pw = hash_password(password)

    # see if the email already exists in db
    cursor.execute('''SELECT 1 FROM Users WHERE Email=?''', (email,))
    if cursor.fetchone() is not None:
        return -2 

    cursor.execute('''
    INSERT INTO Users (Username, Password, FirstName, LastName, Email)
    VALUES (?, ?, ?, ?, ?)
    ''', (username, hashed_pw, first_name, last_name, email))
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
    conn.close()
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
    ORDER BY l.Score DESC, l.ScoreDate ASC
    LIMIT ?
    ''', (limit,))
    result = cursor.fetchall()
    conn.close()
    return [{"username": row[0], "score": row[1], "date": row[2]} for row in result]


def get_media(question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
       SELECT 
           a.AnswerString
       FROM Questions q
       LEFT JOIN Answers a ON q.QuestionID = a.QuestionID
       WHERE q.QuestionID = ?
       ''', (question_id,))
    return cursor.fetchall()

def examples():
    init_db()
    # adding question & answers
    qid = add_question('text', 'example question')
    add_answer(qid, True, "Answer1", "feedback1")
    add_answer(qid, False, "Answer2", "feedback2")


    qid2 = add_question('image', 'Select the Deepfake')
    add_answer(qid2, True, r"floridapoly_fulllogo_rgb_fc.jpg", "feedback1")
    add_answer(qid2, False, r"floridapoly_markonlylogo_rgb_fc.jpg", "feedback2")



#examples()


# Setting db
# Example: store in a tokens table with columns: email, token, expires_at

def get_user_by_email(email: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT UserID, Username, Email
    FROM Users
    WHERE Email = ?
    ''', (email,))
    result = cursor.fetchone()
    conn.close()
    return result  # will be None if not found

def update_username(user_id, new_username):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if username exists
    cursor.execute('''SELECT 1 FROM Users WHERE Username=?''', (new_username,))
    if cursor.fetchone() is not None:
        conn.close()
        return -1  # Username already exists
        
    cursor.execute('''
    UPDATE Users SET Username = ? WHERE UserID = ?
    ''', (new_username, user_id))
    conn.commit()
    conn.close()
    return 1  # Succes

def update_email(user_id, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()
    
    # Check if email exists
    cursor.execute('''SELECT 1 FROM Users WHERE Email=?''', (new_email,))
    if cursor.fetchone() is not None:
        conn.close()
        return -1  # Email already exists
        
    cursor.execute('''
    UPDATE Users SET Email = ?, LastEmailUpdate = ? WHERE UserID = ?
    ''', (new_email, now, user_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated  # Success

def update_password(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed_pw = hash_password(new_password)
    cursor.execute('''
    UPDATE Users SET Password = ? WHERE UserID = ?
    ''', (hashed_pw, user_id))
    conn.commit()
    conn.close()
    return 1  # Success

def authenticate_user_by_id(user_id, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute('''
    SELECT UserID 
    FROM Users 
    WHERE UserID = ? AND Password = ?
    ''', (user_id, hashed_pw))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def delete_user_by_username(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First, check if the user exists
        cursor.execute('SELECT 1 FROM Users WHERE Username = ?', (username,))
        if not cursor.fetchone():
            conn.close()
            return 0  # User not found
            
        # Then delete the user
        cursor.execute('DELETE FROM Users WHERE Username = ?', (username,))
        rows_deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_deleted
    except Exception as e:
        print(f"Error deleting user {username}: {str(e)}")
        # Try to rollback if possible
        try:
            if conn:
                conn.rollback()
                conn.close()
        except:
            pass
        return 0  # Return 0 to indicate failure   


def delete_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users WHERE Email = ?', (email,))
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_deleted

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT UserID, Username, FirstName, LastName, Email, HighScore
    FROM Users
    WHERE UserID = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result    

def get_email(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''

    Select Email
    FROM Users
    WHERE UserID = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_user_email(username, password, current_email, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.datetime.utcnow().isoformat()

    cursor.execute("""
        UPDATE Users 
        SET Email = ?, LastEmailUpdate = ? 
        WHERE Username = ? AND Email = ?""",
        (new_email, now, username, current_email))
    
    updated = cursor.rowcount
    conn.commit()
    conn.close()
    return updated
