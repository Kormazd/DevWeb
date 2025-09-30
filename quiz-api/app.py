from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sqlite3
import hashlib
import os
from dataclasses import dataclass
from jwt_utils import build_token, decode_token, JwtError

app = Flask(__name__)
CORS(app)

# Configuration pour les assets statiques
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'quiz-ui', 'public', 'images')

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
        
        # Table des scores
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Score (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
    # Construire l'URL complète de l'image si elle existe
    image_url = None
    if q.image:
        image_url = f"/assets/{q.image}"
    
    return {
        'id': q.id,
        'title': q.title,
        'text': q.text,
        'position': q.position,
        'image': q.image,
        'image_url': image_url,
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
    return "Quiz API - Clash Royale & Clash of Clans"

# Endpoint pour servir les assets statiques (images)
@app.route('/assets/<path:filename>')
def serve_asset(filename):
    """Sert les assets statiques (images des personnages)"""
    try:
        return send_from_directory(ASSETS_DIR, filename)
    except FileNotFoundError:
        return jsonify({"error": "Asset not found"}), 404

# Endpoint pour lister tous les assets disponibles
@app.route('/assets', methods=['GET'])
def list_assets():
    """Liste tous les assets disponibles"""
    try:
        if not os.path.exists(ASSETS_DIR):
            return jsonify({"error": "Assets directory not found"}), 404
        
        assets = []
        for filename in os.listdir(ASSETS_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                assets.append({
                    "filename": filename,
                    "url": f"/assets/{filename}",
                    "name": os.path.splitext(filename)[0]
                })
        
        return jsonify({
            "assets": assets,
            "count": len(assets)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    try:
        with get_db_connection() as conn:
            size = conn.execute('SELECT COUNT(*) FROM Question').fetchone()[0]
        return jsonify({"size": size}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint pour obtenir des informations complètes sur le quiz
@app.route('/quiz-complete', methods=['GET'])
def get_quiz_complete():
    """Retourne toutes les informations du quiz : questions, assets, et métadonnées"""
    try:
        # Récupérer les questions
        with get_db_connection() as conn:
            questions = conn.execute('SELECT * FROM Question ORDER BY position').fetchall()
            questions_data = []
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
                questions_data.append(question_to_dict(question))
        
        # Récupérer les assets
        assets_data = []
        if os.path.exists(ASSETS_DIR):
            for filename in os.listdir(ASSETS_DIR):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    assets_data.append({
                        "filename": filename,
                        "url": f"/assets/{filename}",
                        "name": os.path.splitext(filename)[0]
                    })
        
        return jsonify({
            "quiz": {
                "questions": questions_data,
                "total_questions": len(questions_data)
            },
            "assets": {
                "images": assets_data,
                "total_assets": len(assets_data)
            },
            "api_info": {
                "version": "1.0.0",
                "endpoints": [
                    "/quiz-info",
                    "/questions",
                    "/questions/<id>",
                    "/assets",
                    "/assets/<filename>",
                    "/quiz-complete"
                ]
            }
        }), 200
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

@app.route('/scores', methods=['GET'])
def get_scores():
    """Retourne le classement des meilleurs scores (limite via ?limit=10)"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        limit = max(1, min(limit or 10, 100))
        with get_db_connection() as conn:
            rows = conn.execute(
                'SELECT id, player, score, total, created_at FROM Score ORDER BY score DESC, created_at ASC LIMIT ?',
                (limit,)
            ).fetchall()
            scores = [{
                'id': r['id'],
                'player': r['player'],
                'score': r['score'],
                'total': r['total'],
                'created_at': r['created_at']
            } for r in rows]
        return jsonify(scores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit_quiz():
    """Calcule le score à partir des réponses et enregistre le résultat."""
    try:
        payload = request.get_json(silent=True) or {}
        player = (payload.get('player') or 'Anonyme').strip() or 'Anonyme'
        answers = payload.get('answers') or []
        if not isinstance(answers, list) or not answers:
            return jsonify({"error": "answers must be a non-empty list"}), 400

        # answers: [{questionId: int, answer: int}] où answer est l'index 0-based
        question_ids = [a.get('questionId') for a in answers if isinstance(a, dict) and isinstance(a.get('questionId'), int)]
        if not question_ids:
            return jsonify({"error": "invalid answers payload"}), 400

        correct_by_qid = {}
        with get_db_connection() as conn:
            placeholders = ','.join('?' for _ in question_ids)
            # Récupérer pour chaque question la position (1-based) de la bonne réponse
            query = f"""
                SELECT question_id, position 
                FROM Answer 
                WHERE isCorrect = 1 AND question_id IN ({placeholders})
            """
            rows = conn.execute(query, question_ids).fetchall()
            for r in rows:
                correct_by_qid[r['question_id']] = int(r['position'])  # 1-based

        total = len(answers)
        score = 0
        for a in answers:
            qid = a.get('questionId')
            idx0 = a.get('answer')  # 0-based index de l'UI
            if isinstance(qid, int) and isinstance(idx0, int):
                expected_pos = correct_by_qid.get(qid)
                if expected_pos is not None and (idx0 + 1) == expected_pos:
                    score += 1

        # Enregistrer le score
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO Score (player, score, total) VALUES (?, ?, ?)',
                (player, score, total)
            )
            inserted_id = cur.lastrowid
            row = conn.execute('SELECT id, player, score, total, created_at FROM Score WHERE id = ?', (inserted_id,)).fetchone()

        return jsonify({
            'player': row['player'],
            'score': row['score'],
            'total': row['total'],
            'created_at': row['created_at']
        }), 201
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
    # Authentification requise
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return 'Unauthorized', 401
    token = auth_header.split(' ', 1)[1]
    try:
        decode_token(token)
    except JwtError:
        return 'Unauthorized', 401

    try:
        with get_db_connection() as conn:
            cursor = conn.execute('DELETE FROM Question WHERE id = ?', (question_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": "Question not found"}), 404
            conn.commit()
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    # Authentification requise
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return 'Unauthorized', 401
    token = auth_header.split(' ', 1)[1]
    try:
        decode_token(token)
    except JwtError:
        return 'Unauthorized', 401

    payload = request.get_json(silent=True) or {}
    try:
        with get_db_connection() as conn:
            # Vérifier l'existence
            existing = conn.execute('SELECT * FROM Question WHERE id = ?', (question_id,)).fetchone()
            if not existing:
                return jsonify({"error": "Question not found"}), 404

            # Mettre à jour la question
            new_title = (payload.get('title') or existing['title']).strip()
            new_text = payload.get('text') if 'text' in payload else existing['text']
            new_position = payload.get('position') if 'position' in payload else existing['position']
            new_image = payload.get('image') if 'image' in payload else existing['image']

            conn.execute(
                'UPDATE Question SET title = ?, text = ?, position = ?, image = ? WHERE id = ?',
                (new_title, new_text, new_position, new_image, question_id)
            )

            # Mettre à jour les réponses si fournies
            if isinstance(payload.get('answers'), list):
                conn.execute('DELETE FROM Answer WHERE question_id = ?', (question_id,))
                for idx, answer_data in enumerate(payload['answers'], start=1):
                    conn.execute(
                        'INSERT INTO Answer (question_id, text, isCorrect, position) VALUES (?, ?, ?, ?)',
                        (
                            question_id,
                            str(answer_data.get('text', '')),
                            bool(answer_data.get('isCorrect', False)),
                            int(answer_data.get('position') or idx)
                        )
                    )

            conn.commit()

            # Renvoyer la question mise à jour
            row = conn.execute('SELECT * FROM Question WHERE id = ?', (question_id,)).fetchone()
            answers = conn.execute(
                'SELECT * FROM Answer WHERE question_id = ? ORDER BY position',
                (question_id,)
            ).fetchall()

            updated = Question(
                id=row['id'],
                title=row['title'],
                text=row['text'],
                position=row['position'],
                image=row['image'],
                answers=[Answer(
                    id=a['id'],
                    text=a['text'],
                    isCorrect=bool(a['isCorrect']),
                    position=a['position'],
                    question_id=a['question_id']
                ) for a in answers]
            )
            return jsonify(question_to_dict(updated)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)