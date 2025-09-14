from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
from dataclasses import dataclass
from jwt_utils import build_token, decode_token, JwtError

app = Flask(__name__)
CORS(app)

DB_PATH = 'quiz.db'
mdp_hash = 'd278077bbfe7285a144d4b5b11adb9cf'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialise la base de données avec la table Question"""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                text TEXT,
                position INTEGER NOT NULL UNIQUE,
                image TEXT,
                possibleAnswers TEXT
            )
        ''')
        conn.commit()

init_db()

@dataclass
class Question:
    title: str
    text: str | None = None
    position: int | None = None
    image: str | None = None
    possibleAnswers: str | None = None
    id: int | None = None

def question_from_dict(data: dict) -> Question:
    return Question(
        title=(data.get('title') or '').strip(),
        text=data.get('text'),
        position=data.get('position'),
        image=data.get('image'),
        possibleAnswers=data.get('possibleAnswers')
    )

def question_to_dict(q: Question) -> dict:
    return {
        'id': q.id,
        'title': q.title,
        'text': q.text,
        'position': q.position,
        'image': q.image,
        'possibleAnswers': q.possibleAnswers
    }

def insert_question(q: Question) -> Question:
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Question (title, text, position, image, possibleAnswers)
            VALUES (?, ?, ?, ?, ?)
            """,
            (q.title, q.text, q.position, q.image, q.possibleAnswers)
        )
        qid = cur.lastrowid
        row = conn.execute('SELECT * FROM Question WHERE id = ?', (qid,)).fetchone()
        created = Question(
            title=row['title'],
            text=row['text'],
            position=row['position'],
            image=row['image'],
            possibleAnswers=row['possibleAnswers'],
            id=row['id']
        )
        return created

@app.route('/')
def root():
    return "Hello, world"

@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    try:
        with get_db_connection() as conn:
            size = conn.execute('SELECT COUNT(*) FROM Question').fetchone()[0]
        return jsonify({"size": size}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    pwd = str(payload.get('password', ''))
    if hashlib.md5(pwd.encode()).hexdigest() != mdp_hash:
        return jsonify(error='Unauthorized'), 401
    return jsonify(token=build_token()), 200

@app.route('/questions', methods=['POST'])
def post_question():
    # Récupérer le token envoyé en paramètre
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return 'Unauthorized', 401
    token = auth_header.split(' ', 1)[1]
    try:
        decode_token(token)
    except JwtError:
        return 'Unauthorized', 401
    # Récupérer l'objet json envoyé dans le body de la requête
    payload = request.get_json() or {}
    try:
        q = question_from_dict(payload)
    except Exception:
        return {"error": "Invalid payload"}, 400
    # Insert into DB
    created = insert_question(q)
    # Simulate answers in response (hard-coded for now)
    response_body = {
        "question": question_to_dict(created),
        "answers": [
            {"id": 1, "title": "Answer A", "isCorrect": False},
            {"id": 2, "title": "Answer B", "isCorrect": True}
        ]
    }
    return response_body, 201

@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        with get_db_connection() as conn:
            questions = conn.execute('SELECT * FROM Question ORDER BY position').fetchall()
            result = []
            for q in questions:
                result.append(question_to_dict(Question(
                    id=q['id'],
                    title=q['title'],
                    text=q['text'],
                    position=q['position'],
                    image=q['image'],
                    possibleAnswers=q['possibleAnswers']
                )))
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        with get_db_connection() as conn:
            question = conn.execute('SELECT * FROM Question WHERE id = ?', (question_id,)).fetchone()
            if not question:
                return jsonify({"error": "Question not found"}), 404
            
            return jsonify(question_to_dict(Question(
                id=question['id'],
                title=question['title'],
                text=question['text'],
                position=question['position'],
                image=question['image'],
                possibleAnswers=question['possibleAnswers']
            ))), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.execute('DELETE FROM Question WHERE id = ?', (question_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": "Question not found"}), 404
            conn.commit()
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)