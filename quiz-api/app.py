from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import sqlite3, hashlib, os, json
from dataclasses import dataclass
from werkzeug.utils import secure_filename
from jwt_utils import build_token, decode_token, JwtError

# --- Configuration ---
app = Flask(__name__)
# Cache static files by default (7 days)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60 * 60 * 24 * 7
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

def ensure_schema():
    """Ensure optional columns exist (game, published) on Question."""
    with get_db_connection() as conn:
        cols = {r[1] for r in conn.execute('PRAGMA table_info(Question)').fetchall()}
        if 'game' not in cols:
            conn.execute("ALTER TABLE Question ADD COLUMN game TEXT")
        if 'published' not in cols:
            conn.execute("ALTER TABLE Question ADD COLUMN published BOOLEAN NOT NULL DEFAULT 1")
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
    game: str | None = None
    published: bool | None = True
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
        game=data.get('game'),
        published=bool(data.get('published', True)),
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
        "game": q.game,
        "published": bool(q.published) if q.published is not None else True,
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
        cur.execute('INSERT INTO Question (title, text, position, image, game, published) VALUES (?, ?, ?, ?, ?, ?)',
                    (q.title, q.text, q.position, q.image, q.game, int(bool(q.published))))
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
    """Sert les fichiers statiques (images) avec mise en cache côté client."""
    if not os.path.exists(os.path.join(ASSETS_DIR, filename)):
        return jsonify({"error": "Asset not found"}), 404
    # 7 jours de cache côté client
    resp = send_from_directory(ASSETS_DIR, filename, cache_timeout=60 * 60 * 24 * 7)
    resp.headers['Cache-Control'] = 'public, max-age=604800'
    return resp

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

@app.get('/health')
def health():
    """Basic healthcheck with versions."""
    return jsonify({
        "status": "ok",
        "api_version": "1.0.0"
    })

@app.get('/scores')
def get_scores():
    """Récupère la liste des meilleurs scores."""
    limit = max(1, min(request.args.get('limit', 10, type=int), 100))
    with get_db_connection() as conn:
        rows = conn.execute('SELECT player, score, total, created_at FROM Score ORDER BY score DESC LIMIT ?', (limit,)).fetchall()
    return jsonify([dict(r) for r in rows])

@app.get('/participations')
def list_participations():
    """Admin: list participations based on Score table (player, score, date).
    Optional filters: from=YYYY-MM-DD, to=YYYY-MM-DD
    """
    if not require_auth():
        return 'Unauthorized', 401
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    with get_db_connection() as conn:
        query = 'SELECT player, score, total, created_at FROM Score'
        params = []
        if date_from and date_to:
            query += ' WHERE datetime(created_at) BETWEEN datetime(?) AND datetime(?)'
            params += [date_from, date_to]
        elif date_from:
            query += ' WHERE datetime(created_at) >= datetime(?)'
            params += [date_from]
        elif date_to:
            query += ' WHERE datetime(created_at) <= datetime(?)'
            params += [date_to]
        query += ' ORDER BY datetime(created_at) DESC'
        rows = conn.execute(query, params).fetchall()
        result = [{
            "playerName": r['player'],
            "score": r['score'],
            "total": r['total'],
            "date": r['created_at'],
            "game": None
        } for r in rows]
    return jsonify(result)

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
            q = Question(
                title=r['title'],
                text=r['text'],
                position=r['position'],
                image=r['image'],
                game=r['game'] if 'game' in r.keys() else None,
                published=bool(r['published']) if 'published' in r.keys() else True,
                id=r['id'],
                answers=[Answer(a['text'], bool(a['isCorrect']), a['position'], a['question_id'], a['id']) for a in answers]
            )
            result.append(to_dict_question(q))
    return jsonify(result)

@app.get('/questions/export')
def export_questions():
    """(Protégé) Export all questions with answers as JSON."""
    if not require_auth():
        return 'Unauthorized', 401
    with get_db_connection() as conn:
        rows = conn.execute('SELECT * FROM Question ORDER BY position').fetchall()
        out = []
        for r in rows:
            answers = conn.execute('SELECT * FROM Answer WHERE question_id=? ORDER BY position', (r['id'],)).fetchall()
            out.append({
                "id": r['id'],
                "title": r['title'],
                "text": r['text'],
                "position": r['position'],
                "image": r['image'],
                "answers": [{
                    "text": a['text'],
                    "isCorrect": bool(a['isCorrect']),
                    "position": a['position']
                } for a in answers]
            })
    return jsonify({"questions": out})

@app.post('/questions/import')
def import_questions():
    """(Protégé) Import questions from JSON. Optional ?override=true to purge first."""
    if not require_auth():
        return 'Unauthorized', 401
    override = request.args.get('override', 'false').lower() == 'true'
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify(error="Body must be JSON"), 400
    data = payload.get('questions') if isinstance(payload, dict) else payload
    if not isinstance(data, list):
        return jsonify(error="Expected a list of questions or {questions:[...]}") ,400
    try:
        ensure_schema()
        with get_db_connection() as conn:
            if override:
                conn.executescript('DELETE FROM Answer; DELETE FROM Question; DELETE FROM sqlite_sequence;')
            position_used = set()
            for idx, q in enumerate(data):
                title = (q.get('title') or '').strip()
                text = q.get('text')
                image = q.get('image')
                pos = q.get('position') or (idx + 1)
                while pos in position_used:
                    pos += 1
                position_used.add(pos)
                qid = None
                if 'id' in q and q['id'] is not None:
                    row = conn.execute('SELECT id FROM Question WHERE id=?', (q['id'],)).fetchone()
                    if row:
                        conn.execute('UPDATE Question SET title=?, text=?, position=?, image=? WHERE id=?',
                                     (title, text, pos, image, q['id']))
                        qid = q['id']
                    else:
                        conn.execute('INSERT INTO Question (id, title, text, position, image) VALUES (?, ?, ?, ?, ?)',
                                     (q['id'], title, text, pos, image))
                        qid = q['id']
                else:
                    row = conn.execute('SELECT id FROM Question WHERE position=?', (pos,)).fetchone()
                    if row:
                        conn.execute('UPDATE Question SET title=?, text=?, image=? WHERE id=?',
                                     (title, text, image, row['id']))
                        qid = row['id']
                    else:
                        cur = conn.execute('INSERT INTO Question (title, text, position, image) VALUES (?, ?, ?, ?)',
                                           (title, text, pos, image))
                        qid = cur.lastrowid
                conn.execute('DELETE FROM Answer WHERE question_id=?', (qid,))
                answers = q.get('answers') or []
                to_insert = [(qid, a.get('text',''), bool(a.get('isCorrect', False)), i+1) for i, a in enumerate(answers)]
                if to_insert:
                    conn.executemany('INSERT INTO Answer (question_id, text, isCorrect, position) VALUES (?, ?, ?, ?)', to_insert)
            conn.commit()
        return jsonify(message="Import completed", count=len(data)), 200
    except Exception as e:
        return jsonify(error=f"Import failed: {str(e)}"), 500

@app.put('/questions/<int:id>/publish')
def set_publish(id: int):
    """(Protégé) Set published flag for a question."""
    if not require_auth():
        return 'Unauthorized', 401
    payload = request.get_json(silent=True) or {}
    if 'published' not in payload:
        return jsonify(error='published is required'), 400
    ensure_schema()
    with get_db_connection() as conn:
        cur = conn.execute('UPDATE Question SET published=? WHERE id=?', (1 if payload['published'] else 0, id))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify(error='Not found'), 404
    return ('', 204)

@app.post('/upload-image')
def upload_image():
    """(Protégé) Upload image to assets dir and return filename & url."""
    if not require_auth():
        return 'Unauthorized', 401
    if 'file' not in request.files:
        return jsonify(error='file is required'), 400
    file = request.files['file']
    if not file.filename:
        return jsonify(error='empty filename'), 400
    name = secure_filename(file.filename)
    ext = os.path.splitext(name)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.webp', '.svg'):
        return jsonify(error='unsupported extension'), 400
    os.makedirs(ASSETS_DIR, exist_ok=True)
    # ensure unique
    base, _ = os.path.splitext(name)
    candidate = name
    i = 1
    while os.path.exists(os.path.join(ASSETS_DIR, candidate)):
        candidate = f"{base}_{i}{ext}"
        i += 1
    filepath = os.path.join(ASSETS_DIR, candidate)
    file.save(filepath)
    return jsonify(filename=candidate, url=f"/assets/{candidate}")

@app.get('/questions/<int:id>')
def get_question(id):
    """Récupère une seule question par son ID."""
    with get_db_connection() as conn:
        row = conn.execute('SELECT * FROM Question WHERE id=?', (id,)).fetchone()
        if not row:
            return jsonify(error="Not found"), 404
        answers = conn.execute('SELECT * FROM Answer WHERE question_id=?', (id,)).fetchall()
        q = Question(
            title=row['title'],
            text=row['text'],
            position=row['position'],
            image=row['image'],
            game=row['game'] if 'game' in row.keys() else None,
            published=bool(row['published']) if 'published' in row.keys() else True,
            id=row['id'],
            answers=[Answer(a['text'], bool(a['isCorrect']), a['position'], a['question_id'], a['id']) for a in answers]
        )
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
        ensure_schema()
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
                conn.execute('UPDATE Question SET title=?, text=?, position=?, image=?, game=?, published=? WHERE id=?',
                             (q.title, q.text, q.position, q.image, q.game, int(bool(q.published)), id))
                conn.execute('DELETE FROM Answer WHERE question_id=?', (id,))
            else:
                # La question n'existe pas -> on la crée
                conn.execute('INSERT INTO Question (id, title, text, position, image, game, published) VALUES (?, ?, ?, ?, ?, ?, ?)',
                             (id, q.title, q.text, q.position, q.image, q.game, int(bool(q.published))))
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

@app.post('/questions/reorder')
def reorder_questions():
    """(Protégé) Réordonne les questions selon une liste d'IDs.
    Body: { "ids": [id1, id2, ...] }
    Met à jour atomiquement les positions pour éviter les collisions de contrainte UNIQUE.
    """
    if not require_auth():
        return 'Unauthorized', 401
    data = request.get_json(silent=True) or {}
    ids = data.get('ids')
    if not isinstance(ids, list) or not all(isinstance(x, int) for x in ids):
        return jsonify(error='Body must include integer array "ids"'), 400
    try:
        with get_db_connection() as conn:
            # Décale toutes les positions pour éviter les collisions UNIQUE
            conn.execute('UPDATE Question SET position = position + 1000')
            # Applique les nouvelles positions pour les IDs fournis
            for idx, qid in enumerate(ids, start=1):
                conn.execute('UPDATE Question SET position=? WHERE id=?', (idx, qid))
            # Place les questions restantes (non listées) après
            placeholders = ','.join('?' for _ in ids) or 'NULL'
            remaining = conn.execute(
                f'SELECT id FROM Question WHERE id NOT IN ({placeholders}) ORDER BY position',
                ids if ids else []
            ).fetchall()
            next_pos = len(ids) + 1
            for r in remaining:
                conn.execute('UPDATE Question SET position=? WHERE id=?', (next_pos, r['id']))
                next_pos += 1
            conn.commit()
        return jsonify(message='Reordered', count=len(ids)), 200
    except Exception as e:
        return jsonify(error=f'Reorder failed: {str(e)}'), 500


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
    ensure_schema()
    app.run(port=5001, debug=True)
