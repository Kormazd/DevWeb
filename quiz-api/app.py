from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import sqlite3, hashlib, os, json
from dataclasses import dataclass
from jwt_utils import build_token, decode_token, JwtError

# --- Configuration ---
app = Flask(__name__)
CORS(app)

DB_PATH = 'DB_Browser_for_SQLite.db'
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'quiz-ui', 'public', 'images')
MDP_HASH = 'd278077bbfe7285a144d4b5b11adb9cf'


# --- Connexion et Initialisation de la BDD ---
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
        CREATE TABLE IF NOT EXISTS Participation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL UNIQUE,
            answers TEXT
        );
        CREATE TRIGGER IF NOT EXISTS update_question_timestamp
        AFTER UPDATE ON Question
        FOR EACH ROW
        BEGIN
            UPDATE Question SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
        ''')
        conn.commit()


# --- Modèles de Données (Dataclasses) ---
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

@dataclass
class Participation:
    player_name: str
    answers: dict
    id: int | None = None


# --- Fonctions Utilitaires ---
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

def to_dict_participation(p: Participation):
    return {"id": p.id, "player_name": p.player_name, "answers": p.answers}

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


# --- Routes de l'API (ordonnées GET, POST, PUT, DELETE) ---

# --- METHODES GET ---
@app.get('/')
def home():
    """Affiche la page d'accueil de l'API."""
    return "Quiz API - Clash Royale & Clash of Clans"

@app.get('/assets/<path:filename>')
def serve_asset(filename):
    """Sert les fichiers statiques (images)."""
    if not os.path.exists(os.path.join(ASSETS_DIR, filename)):
        return jsonify({"error": "Asset not found"}), 404
    return send_from_directory(ASSETS_DIR, filename)

@app.get('/quiz-info')
def quiz_info():
    """Récupère les informations de base du quiz (nombre de questions et de scores)."""
    with get_db_connection() as conn:
        questions_count = conn.execute('SELECT COUNT(*) FROM Question').fetchone()[0]
        scores_rows = conn.execute('''
            SELECT player, score, total, created_at 
            FROM Score 
            ORDER BY score DESC, created_at ASC 
            LIMIT 10
        ''').fetchall()
        scores = []
        for row in scores_rows:
            scores.append({
                "playerName": row['player'],
                "score": row['score'],
                "date": row['created_at']
            })
    return jsonify({"size": questions_count, "scores": scores})

@app.get('/scores')
def get_scores():
    """Récupère la liste des meilleurs scores."""
    limit = max(1, min(request.args.get('limit', 10, type=int), 100))
    with get_db_connection() as conn:
        rows = conn.execute('SELECT player, score, total, created_at FROM Score ORDER BY score DESC LIMIT ?', (limit,)).fetchall()
    return jsonify([dict(r) for r in rows])

@app.get('/questions')
def get_questions():
    """Récupère la liste des questions. Peut être filtrée par `?position=X`."""
    position_filter = request.args.get('position', default=None, type=int)
    with get_db_connection() as conn:
        query = 'SELECT * FROM Question'
        params = []
        if position_filter is not None:
            query += ' WHERE position = ?'
            params.append(position_filter)
        query += ' ORDER BY position'
        rows = conn.execute(query, params).fetchall()
        result = []
        for r in rows:
            answers = conn.execute('SELECT * FROM Answer WHERE question_id=? ORDER BY position', (r['id'],)).fetchall()
            q = Question(r['title'], r['text'], r['position'], r['image'], r['id'],
                         [Answer(a['text'], bool(a['isCorrect']), a['position'], a['question_id'], a['id']) for a in answers])
            result.append(to_dict_question(q))
    return jsonify(result)

@app.get('/questions/<int:id>')
def get_question(id):
    """Récupère une seule question par son ID."""
    with get_db_connection() as conn:
        row = conn.execute('SELECT * FROM Question WHERE id=?', (id,)).fetchone()
        if not row:
            return jsonify(error="Not found"), 404
        answers = conn.execute('SELECT * FROM Answer WHERE question_id=?', (id,)).fetchall()
        q = Question(row['title'], row['text'], row['position'], row['image'], row['id'],
                     [Answer(a['text'], bool(a['isCorrect']), a['position'], a['question_id'], a['id']) for a in answers])
        return jsonify(to_dict_question(q))

@app.get('/participations/<string:player_name>')
def get_participation(player_name):
    """Récupère une participation en cours pour un joueur donné."""
    with get_db_connection() as conn:
        row = conn.execute('SELECT * FROM Participation WHERE player_name=?', (player_name,)).fetchone()
        if not row:
            return jsonify(error="No active participation found for this player"), 404
        answers_dict = json.loads(row['answers']) if row['answers'] else {}
        p = Participation(player_name=row['player_name'], answers=answers_dict, id=row['id'])
        return jsonify(to_dict_participation(p))

# --- METHODES POST ---
@app.post('/login')
def login():
    """Connecte l'administrateur et renvoie un token JWT."""
    pwd = (request.get_json(silent=True) or {}).get("password", "")
    if hashlib.md5(pwd.encode()).hexdigest() != MDP_HASH:
        return jsonify(error="Unauthorized"), 401
    return jsonify(token=build_token()), 200

@app.post('/rebuild-db')
def rebuild_db():
    """(Protégé) Vide et réinitialise complètement la base de données."""
    if not require_auth():
        return 'Unauthorized', 401
    with get_db_connection() as conn:
        conn.executescript('DELETE FROM Answer; DELETE FROM Question; DELETE FROM Score; DELETE FROM Participation; DELETE FROM sqlite_sequence;')
        conn.commit()
    init_db()
    return make_response("Ok", 200)

@app.post('/questions')
def post_question():
    """(Protégé) Crée une nouvelle question."""
    if not require_auth():
        return 'Unauthorized', 401
    data = request.get_json()
    if not data:
        return jsonify(error="Request body must be a valid JSON"), 400
    try:
        q = insert_question(question_from_dict(data))
        return jsonify(to_dict_question(q)), 201
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify(error="This position is already taken."), 409
        return jsonify(error=f"Database integrity error: {str(e)}"), 500
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

@app.post('/scores')
def post_score():
    """Enregistre le score d'un joueur à la fin d'une partie."""
    data = request.get_json()
    if not data or 'player' not in data or 'score' not in data or 'total' not in data:
        return jsonify(error="Données manquantes ou invalides"), 400
    player_name = data.get('player')
    player_score = data.get('score')
    total_questions = data.get('total')
    with get_db_connection() as conn:
        conn.execute('INSERT INTO Score (player, score, total) VALUES (?, ?, ?)',
                     (player_name, player_score, total_questions))
        conn.commit()
    return jsonify(message="Score enregistré avec succès"), 201

@app.post('/participations')
def post_participation():
    """Crée ou met à jour la participation d'un joueur."""
    data = request.get_json()
    if not data or 'playerName' not in data or 'answers' not in data:
        return jsonify(error="player_name and answers are required"), 400
    player_name = data['playerName']
    answers = json.dumps(data['answers'])
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO Participation (player_name, answers) VALUES (?, ?)
            ON CONFLICT(player_name) DO UPDATE SET answers=excluded.answers;
        ''', (player_name, answers))
        conn.commit()
    return jsonify(message=f"Participation for {player_name} saved."), 200

# --- METHODES PUT ---
@app.put('/questions/<int:id>')
def update_question(id):
    """(Protégé) Met à jour une question existante ou la crée si elle n'existe pas (Upsert)."""
    if not require_auth():
        return 'Unauthorized', 401
    
    data = request.get_json()
    if not data:
        return jsonify(error="Request body must be a valid JSON"), 400

    q = question_from_dict(data)

    try:
        with get_db_connection() as conn:
            existing_question = conn.execute('SELECT id FROM Question WHERE id=?', (id,)).fetchone()
            status_code = 204 # Par défaut: No Content (pour une mise à jour)

            if existing_question:
                # La question existe -> on la met à jour
                conn.execute('UPDATE Question SET title=?, text=?, position=?, image=? WHERE id=?',
                             (q.title, q.text, q.position, q.image, id))
                conn.execute('DELETE FROM Answer WHERE question_id=?', (id,))
            else:
                # La question n'existe pas -> on la crée
                conn.execute('INSERT INTO Question (id, title, text, position, image) VALUES (?, ?, ?, ?, ?)',
                             (id, q.title, q.text, q.position, q.image))
                status_code = 201 # Created (pour une création)

            # Dans les deux cas, on insère les nouvelles réponses
            if q.answers:
                answers_to_insert = [(id, a.text, a.isCorrect, a.position) for a in q.answers]
                conn.executemany(
                    'INSERT INTO Answer (question_id, text, isCorrect, position) VALUES (?, ?, ?, ?)',
                    answers_to_insert
                )
            
            conn.commit()
            
            return ('', status_code)
            
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: Question.position' in str(e):
            return jsonify(error="This position is already taken by another question."), 409
        else:
            return jsonify(error=f"Database integrity error: {str(e)}"), 500
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

# --- METHODES DELETE ---
@app.delete('/questions/<int:id>')
def delete_question(id):
    """(Protégé) Supprime une question par son ID."""
    if not require_auth():
        return 'Unauthorized', 401
    with get_db_connection() as conn:
        cur = conn.execute('DELETE FROM Question WHERE id=?', (id,))
        conn.commit()
        return ('', 204) if cur.rowcount else (jsonify(error="Not found"), 404)

@app.delete('/questions/all')
def delete_all_questions():
    """(Protégé) Supprime toutes les questions."""
    if not require_auth():
        return 'Unauthorized', 401
    with get_db_connection() as conn:
        conn.execute('DELETE FROM Question')
        conn.commit()
        return ('', 204)


@app.delete('/participations/all')
def delete_all_participations():
    """(Protégé) Supprime toutes les participations."""
    if not require_auth():
        return 'Unauthorized', 401
    with get_db_connection() as conn:
        conn.execute('DELETE FROM Participation')
        conn.commit()
        return ('', 204)

# --- Démarrage de l'application ---
if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
