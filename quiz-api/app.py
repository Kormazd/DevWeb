<<<<<<< HEAD
from flask import Flask, render_template
=======
from flask import Flask, request, jsonify, send_from_directory, make_response
>>>>>>> 34dd0b3fc39932bdcd7fd85cda5ba46ffff7c6d6
from flask_cors import CORS
import sqlite3, hashlib, os
from dataclasses import dataclass
from jwt_utils import build_token, decode_token, JwtError

# --- Configuration ---
app = Flask(__name__)
CORS(app)

DB_PATH = 'DB_Browser_for_SQLite.db'
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'quiz-ui', 'public', 'images')
MDP_HASH = 'd278077bbfe7285a144d4b5b11adb9cf'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS Question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT,
            position INTEGER NOT NULL UNIQUE,
            image TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS Answer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            isCorrect BOOLEAN NOT NULL DEFAULT 0,
            position INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES Question(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TRIGGER IF NOT EXISTS update_question_timestamp
        AFTER UPDATE ON Question
        FOR EACH ROW
        BEGIN
            UPDATE Question SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
        ''')
        conn.commit()


# --- Dataclasses ---
@dataclass
class Answer:
    text: str
    isCorrect: bool
    position: int
    question_id: int | None = None
    id: int | None = None


@dataclass
class Question:
    title: str
    text: str | None = None
    position: int | None = None
    image: str | None = None
    id: int | None = None
    answers: list[Answer] | None = None


# --- Utils ---
def require_auth():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1]
    try:
        decode_token(token)
        return token
    except JwtError:
        return None


def question_from_dict(data: dict) -> Question:
    answers = [Answer(a.get('text', ''), a.get('isCorrect', False), i + 1)
               for i, a in enumerate(data.get('answers', []))]
    return Question(
        title=(data.get('title') or '').strip(),
        text=data.get('text'),
        position=data.get('position'),
        image=data.get('image'),
        answers=answers
    )


def to_dict_question(q: Question):
    return {
        "id": q.id,
        "title": q.title,
        "text": q.text,
        "position": q.position,
        "image": q.image,
        "image_url": f"/assets/{q.image}" if q.image else None,
        "answers": [to_dict_answer(a) for a in (q.answers or [])]
    }


def to_dict_answer(a: Answer):
    return {"id": a.id, "text": a.text, "isCorrect": a.isCorrect, "position": a.position}


def insert_question(q: Question) -> Question:
    with get_db_connection() as conn:
        cur = conn.cursor()
        if q.position is None:
            q.position = cur.execute('SELECT COALESCE(MAX(position),0)+1 FROM Question').fetchone()[0]
        cur.execute('INSERT INTO Question (title, text, position, image) VALUES (?, ?, ?, ?)',
                    (q.title, q.text, q.position, q.image))
        q.id = cur.lastrowid
        if q.answers:
            cur.executemany(
                'INSERT INTO Answer (question_id, text, isCorrect, position) VALUES (?, ?, ?, ?)',
                [(q.id, a.text, a.isCorrect, a.position) for a in q.answers]
            )
        conn.commit()
        return q


# --- Routes ---
@app.route('/')
<<<<<<< HEAD
def index():
    """Page d'accueil du quiz Supercell"""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
=======
def home():
    return "Quiz API - Clash Royale & Clash of Clans"


@app.route('/assets/<path:filename>')
def serve_asset(filename):
    if not os.path.exists(os.path.join(ASSETS_DIR, filename)):
        return jsonify({"error": "Asset not found"}), 404
    return send_from_directory(ASSETS_DIR, filename)


@app.post('/login')
def login():
    pwd = (request.get_json(silent=True) or {}).get("password", "")
    if hashlib.md5(pwd.encode()).hexdigest() != MDP_HASH:
        return jsonify(error="Unauthorized"), 401
    return jsonify(token=build_token()), 200


@app.post('/rebuild-db')
def rebuild_db():
    if not require_auth():
        return 'Unauthorized', 401
    with get_db_connection() as conn:
        conn.executescript('DELETE FROM Answer; DELETE FROM Question; DELETE FROM Score; DELETE FROM sqlite_sequence;')
        conn.commit()
    init_db()
    return make_response("Ok", 200)


@app.post('/questions')
def post_question():
    if not require_auth():
        return 'Unauthorized', 401
    try:
        q = insert_question(question_from_dict(request.get_json() or {}))
        return jsonify(to_dict_question(q)), 201
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.get('/questions')
def get_questions():
    with get_db_connection() as conn:
        rows = conn.execute('SELECT * FROM Question ORDER BY position').fetchall()
        result = []
        for r in rows:
            answers = conn.execute('SELECT * FROM Answer WHERE question_id=? ORDER BY position', (r['id'],)).fetchall()
            q = Question(r['title'], r['text'], r['position'], r['image'], r['id'],
                         [Answer(a['text'], bool(a['isCorrect']), a['position'], a['question_id'], a['id']) for a in answers])
            result.append(to_dict_question(q))
    return jsonify(result)


@app.delete('/questions/<int:id>')
def delete_question(id):
    if not require_auth():
        return 'Unauthorized', 401
    with get_db_connection() as conn:
        cur = conn.execute('DELETE FROM Question WHERE id=?', (id,))
        conn.commit()
        return ('', 204) if cur.rowcount else (jsonify(error="Not found"), 404)


@app.get('/quiz-info')
def quiz_info():
    with get_db_connection() as conn:
        size = conn.execute('SELECT COUNT(*) FROM Question').fetchone()[0]
    return jsonify({"size": size})


@app.get('/scores')
def get_scores():
    limit = max(1, min(request.args.get('limit', 10, type=int), 100))
    with get_db_connection() as conn:
        rows = conn.execute('SELECT player, score, total, created_at FROM Score ORDER BY score DESC LIMIT ?', (limit,)).fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
>>>>>>> 34dd0b3fc39932bdcd7fd85cda5ba46ffff7c6d6
