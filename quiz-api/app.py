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
    """Initialise la base de données avec les tables Question et Answer"""
    with get_db_connection() as conn:
        # Table des questions
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                text TEXT,
                position INTEGER NOT NULL UNIQUE,
                image TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des réponses
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Answer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                isCorrect BOOLEAN NOT NULL DEFAULT 0,
                position INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE CASCADE
            )
        ''')
        
        # Index pour améliorer les performances
        conn.execute('CREATE INDEX IF NOT EXISTS idx_question_position ON Question(position)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_answer_question_id ON Answer(question_id)')
        
        # Trigger pour mettre à jour updated_at
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_question_timestamp 
            AFTER UPDATE ON Question
            FOR EACH ROW
            BEGIN
                UPDATE Question SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        conn.commit()

init_db()

@dataclass
class Question:
    title: str
    text: str | None = None
    position: int | None = None
    image: str | None = None
    id: int | None = None
    answers: list = None

@dataclass
class Answer:
    text: str
    isCorrect: bool
    position: int
    question_id: int | None = None
    id: int | None = None

def question_from_dict(data: dict) -> Question:
    answers = []
    if 'answers' in data and isinstance(data['answers'], list):
        for i, answer_data in enumerate(data['answers']):
            answers.append(Answer(
                text=answer_data.get('text', ''),
                isCorrect=answer_data.get('isCorrect', False),
                position=i + 1
            ))
    
    return Question(
        title=(data.get('title') or '').strip(),
        text=data.get('text'),
        position=data.get('position'),
        image=data.get('image'),
        answers=answers
    )

def question_to_dict(q: Question) -> dict:
    return {
        'id': q.id,
        'title': q.title,
        'text': q.text,
        'position': q.position,
        'image': q.image,
        'answers': [answer_to_dict(a) for a in (q.answers or [])]
    }

def answer_to_dict(a: Answer) -> dict:
    return {
        'id': a.id,
        'text': a.text,
        'isCorrect': a.isCorrect,
        'position': a.position
    }

def insert_question(q: Question) -> Question:
    with get_db_connection() as conn:
        cur = conn.cursor()
        # Insérer la question
        cur.execute(
            """
            INSERT INTO Question (title, text, position, image)
            VALUES (?, ?, ?, ?)
            """,
            (q.title, q.text, q.position, q.image)
        )
        question_id = cur.lastrowid
        
        # Insérer les réponses si elles existent
        if q.answers:
            for answer in q.answers:
                cur.execute(
                    """
                    INSERT INTO Answer (question_id, text, isCorrect, position)
                    VALUES (?, ?, ?, ?)
                    """,
                    (question_id, answer.text, answer.isCorrect, answer.position)
                )
        
        # Récupérer la question complète avec ses réponses
        row = conn.execute('SELECT * FROM Question WHERE id = ?', (question_id,)).fetchone()
        answers = conn.execute(
            'SELECT * FROM Answer WHERE question_id = ? ORDER BY position', 
            (question_id,)
        ).fetchall()
        
        created = Question(
            title=row['title'],
            text=row['text'],
            position=row['position'],
            image=row['image'],
            id=row['id'],
            answers=[Answer(
                id=a['id'],
                text=a['text'],
                isCorrect=bool(a['isCorrect']),
                position=a['position'],
                question_id=a['question_id']
            ) for a in answers]
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
    # Retourner la question avec ses réponses
    response_body = {
        "question": question_to_dict(created),
        "answers": [answer_to_dict(a) for a in created.answers]
    }
    return response_body, 201

@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        with get_db_connection() as conn:
            questions = conn.execute('SELECT * FROM Question ORDER BY position').fetchall()
            result = []
            for q in questions:
                # Récupérer les réponses pour chaque question
                answers = conn.execute(
                    'SELECT * FROM Answer WHERE question_id = ? ORDER BY position', 
                    (q['id'],)
                ).fetchall()
                
                question = Question(
                    id=q['id'],
                    title=q['title'],
                    text=q['text'],
                    position=q['position'],
                    image=q['image'],
                    answers=[Answer(
                        id=a['id'],
                        text=a['text'],
                        isCorrect=bool(a['isCorrect']),
                        position=a['position'],
                        question_id=a['question_id']
                    ) for a in answers]
                )
                result.append(question_to_dict(question))
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
            
            # Récupérer les réponses
            answers = conn.execute(
                'SELECT * FROM Answer WHERE question_id = ? ORDER BY position', 
                (question_id,)
            ).fetchall()
            
            q = Question(
                id=question['id'],
                title=question['title'],
                text=question['text'],
                position=question['position'],
                image=question['image'],
                answers=[Answer(
                    id=a['id'],
                    text=a['text'],
                    isCorrect=bool(a['isCorrect']),
                    position=a['position'],
                    question_id=a['question_id']
                ) for a in answers]
            )
            
            return jsonify(question_to_dict(q)), 200
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