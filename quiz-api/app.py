from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from jwt_utils import build_token, decode_token, JwtError
from questions import (
    Question,
    question_from_dict,
    question_to_dict,
    insert_question,
    count_questions,
    list_questions,
    delete_question,
    get_question_by_id,
    get_question_by_position,
    list_answers_for_question,
    update_question,
    delete_all_questions,
    delete_all_participations,
    rebuild_db,
    create_participation,
    list_scores,
    get_db_connection,
)

# ===============================================================
# ====================== CONFIGURATION ==========================
# ===============================================================

app = Flask(__name__)
# Enable global CORS for all routes; allow credentials for Authorization headers
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

ADMIN_PASSWORD = "iloveflask"
LEGACY_ADMIN_PASSWORD_MD5 = "d278077bbfe7285a144d4b5b11adb9cf"


# ===============================================================
# ============================ GET ==============================
# ===============================================================

@app.get("/")
def home():
    return "Quiz API - Version Flask"


@app.get("/quiz-info")
def get_quiz_info():
    """Retourne la taille du quiz et le classement."""
    n_questions = count_questions()

    # Si aucune question, Postman attend un leaderboard vide
    if n_questions == 0:
        return {"size": 0, "scores": []}, 200

    mode = request.args.get("mode")
    return {"size": n_questions, "scores": list_scores(10, mode)}, 200


@app.get("/questions")
def get_questions():
    """Récupère toutes les questions, ou une seule par position."""
    position = request.args.get("position", type=int)

    if position:
        q = get_question_by_position(position)
        if not q:
            return {}, 404
        data = question_to_dict(q)
        data["possibleAnswers"] = list_answers_for_question(q.id)
        return data, 200

    questions = []
    for q in list_questions():
        item = question_to_dict(q)
        item["possibleAnswers"] = list_answers_for_question(q.id)
        questions.append(item)

    return {"items": questions}, 200


@app.get("/questions/<int:qid>")
def get_question_by_id_route(qid: int):
    """Récupère une question par son ID."""
    q = get_question_by_id(qid)
    if not q:
        return {}, 404
    data = question_to_dict(q)
    data["possibleAnswers"] = list_answers_for_question(q.id)
    return data, 200

@app.get("/questions/admin")
def get_questions_admin():
    """
    Version pour l'interface d'admin du site.
    Renvoie directement un tableau de questions (array),
    pas un objet { items: [...] }.
    """
    result = []
    for q in list_questions():
        q_dict = question_to_dict(q)
        q_dict["possibleAnswers"] = list_answers_for_question(q.id)
        result.append(q_dict)
    return result, 200


@app.route("/questions/export", methods=["GET", "OPTIONS"])
def export_stub():
    """
    Stub endpoint to satisfy frontend export calls.
    """
    return ("", 204)

# ===============================================================
# ============================ POST =============================
# ===============================================================

@app.post("/login")
def login():
    """Authentifie l’administrateur et renvoie un token JWT."""
    payload = request.get_json() or {}
    password = str(payload.get("password", ""))

    provided_hash = hashlib.md5(password.encode()).hexdigest()
    if password != ADMIN_PASSWORD and provided_hash != LEGACY_ADMIN_PASSWORD_MD5:
        return "Unauthorized", 401

    return {"token": build_token()}, 200


@app.post("/questions")
def post_question():
    """Crée une nouvelle question protégée par JWT."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "Unauthorized", 401

    token = auth_header.split(" ", 1)[1]
    decode_token(token)

    payload = request.get_json() or {}
    q = question_from_dict(payload)
    possible_answers = payload.get("possibleAnswers")

    created = insert_question(q, possible_answers)

    data = question_to_dict(created)
    data["possibleAnswers"] = list_answers_for_question(created.id)
    return data, 200


@app.post("/participations")
def create_participation_route():
    """Enregistre une participation et calcule le score."""
    payload = request.get_json() or {}

    player_name = str(payload.get("playerName", "")).strip()
    answers = payload.get("answers", [])
    question_ids = payload.get("questionIds", [])
    mode = str(payload.get("mode", "classique"))
    time_taken = payload.get("timeTaken")

    if not player_name or not isinstance(answers, list):
        return {"error": "Invalid payload"}, 400

    try:
        selected = [int(a) for a in answers]
    except Exception:
        return {"error": "Invalid answers"}, 400

    if len(selected) == 0:
        return {"error": "No answers provided"}, 400
    if any(a < 1 or a > 4 for a in selected):
        return {"error": "Invalid answer index"}, 400

    # Récupération des questions
    with get_db_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute("SELECT id FROM Question ORDER BY position ASC").fetchall()
        all_ids = [r["id"] for r in rows]

    total_questions = len(all_ids)
    if total_questions == 0:
        return {"error": "No questions in quiz"}, 400

    # Cas 1 : questionIds présents
    if isinstance(question_ids, list) and len(question_ids) > 0:
        if len(question_ids) != len(selected):
            return {"error": "answers/questionIds length mismatch"}, 400

        try:
            cleaned_ids = [int(q) for q in question_ids]
        except Exception:
            return {"error": "Invalid question id"}, 400

        if len(cleaned_ids) != len(set(cleaned_ids)):
            return {"error": "Duplicate question ids"}, 400

        if set(cleaned_ids) != set(all_ids):
            return {"error": "Invalid answers count"}, 400

        score = 0
        for i, qid in enumerate(cleaned_ids):
            chosen = selected[i] - 1
            answers_for_q = list_answers_for_question(qid)
            if 0 <= chosen < len(answers_for_q) and answers_for_q[chosen]["isCorrect"]:
                score += 1

        create_participation(player_name, selected, mode, time_taken)
        return {"playerName": player_name, "score": score, "total": total_questions}, 200

    # Cas 2 : pas de questionIds
    if len(selected) != total_questions:
        return {"error": f"Invalid answers count: expected {total_questions}, got {len(selected)}"}, 400

    score = 0
    for i, qid in enumerate(all_ids):
        chosen = selected[i] - 1
        answers_for_q = list_answers_for_question(qid)
        if 0 <= chosen < len(answers_for_q) and answers_for_q[chosen]["isCorrect"]:
            score += 1

    create_participation(player_name, selected, mode, time_taken)
    return {"playerName": player_name, "score": score, "total": total_questions}, 200


@app.post("/rebuild-db")
def rebuild_db_route():
    """Réinitialise complètement la base de données."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "Unauthorized", 401

    token = auth_header.split(" ", 1)[1]
    decode_token(token)

    rebuild_db()
    return "Ok", 200


# ===============================================================
# ============================= PUT =============================
# ===============================================================

@app.put("/questions/<int:qid>")
def put_question(qid: int):
    """Met à jour une question par son ID."""
    payload = request.get_json() or {}
    updated = update_question(qid, payload)
    if not updated:
        return "", 404
    return "", 204


@app.put("/questions")
def put_question_by_position():
    """Déplace une question d’une position à une autre."""
    payload = request.get_json() or {}

    from_pos = (
        payload.get("fromPosition")
        or payload.get("from")
        or payload.get("position")
        or payload.get("oldPosition")
        or payload.get("currentPosition")
    )
    to_pos = (
        payload.get("toPosition")
        or payload.get("to")
        or payload.get("newPosition")
        or payload.get("targetPosition")
        or payload.get("new")
    )

    try:
        from_pos = int(from_pos)
        to_pos = int(to_pos)
    except Exception:
        return {"error": "Invalid positions"}, 400

    q = get_question_by_position(from_pos)
    if not q:
        return "", 404

    moved = update_question(q.id, {"position": to_pos})
    if not moved:
        return "", 404

    return "", 204


# ===============================================================
# ============================ DELETE ===========================
# ===============================================================

@app.delete("/questions/<int:qid>")
def delete_question_route(qid: int):
    """Supprime une question par ID."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "Unauthorized", 401

    token = auth_header.split(" ", 1)[1]
    decode_token(token)

    existed = delete_question(qid)
    if not existed:
        return "", 404
    return "", 204


@app.delete("/questions")
def delete_question_by_position():
    """Supprime une question par sa position."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "Unauthorized", 401

    token = auth_header.split(" ", 1)[1]
    decode_token(token)

    position = request.args.get("position", type=int)
    if not position:
        return {"error": "Missing position"}, 400

    q = get_question_by_position(position)
    if not q:
        return "", 404

    delete_question(q.id)
    return "", 204


@app.delete("/questions/all")
def delete_all_questions_route():
    """Supprime toutes les questions."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "Unauthorized", 401

    token = auth_header.split(" ", 1)[1]
    decode_token(token)

    delete_all_questions()
    return "", 204


@app.delete("/participations/all")
def delete_all_participations_route():
    """Supprime toutes les participations."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return "Unauthorized", 401

    token = auth_header.split(" ", 1)[1]
    decode_token(token)

    delete_all_participations()
    return "", 204


# ===============================================================
# ============================= MAIN ============================
# ===============================================================

if __name__ == "__main__":
    rebuild_db()
    app.run(port=5001, debug=True)