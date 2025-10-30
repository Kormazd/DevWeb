import sqlite3
import json
import os
from dataclasses import dataclass

# Use an absolute path to ensure consistent DB location regardless of CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'DB_Browser_for_SQLite.db')


# ========================
# Base de données
# ========================

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rebuild_db():
    """
    Réinitialise complètement la base :
    - drop + recreate toutes les tables
    - structure cohérente avec le code
    """
    with get_db_connection() as conn:
        cur = conn.cursor()

        cur.executescript("""
        DROP TABLE IF EXISTS Answer;
        DROP TABLE IF EXISTS Question;
        DROP TABLE IF EXISTS Score;
        DROP TABLE IF EXISTS Participation;

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
            answers TEXT,
            mode TEXT,
            time_taken INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TRIGGER IF NOT EXISTS update_question_timestamp
        AFTER UPDATE ON Question
        FOR EACH ROW
        BEGIN
            UPDATE Question SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
        """)

        conn.commit()


# ========================
# Dataclass utilitaire
# ========================

@dataclass
class Question:
    id: int
    title: str
    text: str
    position: int
    image: str


def _row_to_question(row):
    return Question(
        id=row["id"],
        title=row["title"],
        text=row["text"],
        position=row["position"],
        image=row["image"],
    )


# ========================
# Lecture (READ)
# ========================

def count_questions():
    with get_db_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM Question").fetchone()
        return row["n"] if row else 0


def list_questions():
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM Question ORDER BY position ASC"
        ).fetchall()
        return [_row_to_question(r) for r in rows]


def get_question_by_id(qid: int):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM Question WHERE id=?",
            (qid,)
        ).fetchone()
        return _row_to_question(row) if row else None


def get_question_by_position(pos: int):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM Question WHERE position=?",
            (pos,)
        ).fetchone()
        return _row_to_question(row) if row else None


def list_answers_for_question(qid: int):
    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT text, isCorrect, position
            FROM Answer
            WHERE question_id=?
            ORDER BY position ASC
            """,
            (qid,)
        ).fetchall()

        return [
            {
                "text": r["text"],
                "isCorrect": bool(r["isCorrect"])
            }
            for r in rows
        ]


# ========================
# Ecriture (WRITE)
# ========================

def question_from_dict(payload: dict) -> Question:
    """
    Transforme le JSON reçu en Question "pré-insert".
    (id = -1 car pas encore en DB)
    """
    return Question(
        id=-1,
        title=str(payload.get("title", "")).strip(),
        text=str(payload.get("text", "")).strip(),
        position=payload.get("position"),
        image=payload.get("image"),
    )


def question_to_dict(q: Question) -> dict:
    """
    Transforme Question (dataclass) -> JSON renvoyé à Postman.
    """
    return {
        "id": q.id,
        "title": q.title,
        "text": q.text,
        "position": q.position,
        "image": q.image,
        "image_url": f"/assets/{q.image}" if q.image else None,
    }


def _shift_questions_down_from(target_pos: int, cur):
    """
    Déplace vers le bas (+1) toutes les questions
    à partir de target_pos, en respectant UNIQUE(position).
    Technique : tampon 1_000_000 puis réécriture.
    """
    rows_to_shift = cur.execute(
        """
        SELECT id, position
        FROM Question
        WHERE position >= ?
        ORDER BY position DESC
        """,
        (target_pos,)
    ).fetchall()

    # Phase tampon
    for r in rows_to_shift:
        cur.execute(
            "UPDATE Question SET position=? WHERE id=?",
            (1_000_000 + r["position"], r["id"])
        )

    # Phase finale (+1)
    for r in rows_to_shift:
        cur.execute(
            "UPDATE Question SET position=? WHERE id=?",
            (r["position"] + 1, r["id"])
        )


def insert_question(q: Question, possible_answers=None) -> Question:
    """
    Insère une nouvelle question.
    - si q.position est None -> append à la fin
    - si q.position existe déjà -> on pousse toutes les suivantes vers le bas
      (reordering façon insertion)
    - insère aussi possibleAnswers[]
    - renvoie la Question créée (avec son id réel)
    """
    with get_db_connection() as conn:
        cur = conn.cursor()

        # détermine position finale
        if q.position is None:
            max_row = cur.execute(
                "SELECT COALESCE(MAX(position), 0) AS m FROM Question"
            ).fetchone()
            target_pos = max_row["m"] + 1
        else:
            try:
                target_pos = int(q.position)
            except (TypeError, ValueError):
                max_row = cur.execute(
                    "SELECT COALESCE(MAX(position), 0) AS m FROM Question"
                ).fetchone()
                target_pos = max_row["m"] + 1

        # pousse les questions à partir de target_pos vers le bas
        _shift_questions_down_from(target_pos, cur)

        # crée la question avec une position tampon, puis fixe sa vraie position
        cur.execute(
            """
            INSERT INTO Question (title, text, position, image)
            VALUES (?, ?, ?, ?)
            """,
            (q.title, q.text, 999_999, q.image)
        )
        new_id = cur.lastrowid

        cur.execute(
            "UPDATE Question SET position=? WHERE id=?",
            (target_pos, new_id)
        )

        # insère les réponses possibles
        if isinstance(possible_answers, list):
            for idx, ans in enumerate(possible_answers, start=1):
                ans_text = str(ans.get("text", "")).strip()
                ans_correct = bool(ans.get("isCorrect", False))
                cur.execute(
                    """
                    INSERT INTO Answer (question_id, text, isCorrect, position)
                    VALUES (?, ?, ?, ?)
                    """,
                    (new_id, ans_text, int(ans_correct), idx)
                )

        conn.commit()

        # relit la version finale pour renvoyer la dataclass "clean"
        row_back = cur.execute(
            "SELECT * FROM Question WHERE id=?",
            (new_id,)
        ).fetchone()

        return _row_to_question(row_back)


def _reorder_all_questions(cur, ordered_ids):
    """
    Rebuild des positions 1..n pour les IDs donnés dans l'ordre.
    Utilisé après un move ou un delete.
    """
    final_map = [(qid, pos) for pos, qid in enumerate(ordered_ids, start=1)]

    # Phase tampon
    for qid, newpos in final_map:
        cur.execute(
            "UPDATE Question SET position=? WHERE id=?",
            (1_000_000 + newpos, qid)
        )

    # Phase finale
    for qid, newpos in final_map:
        cur.execute(
            "UPDATE Question SET position=? WHERE id=?",
            (newpos, qid)
        )


def update_question(qid: int, payload: dict) -> bool:
    """
    Met à jour :
      - la position (reorder global style drag & drop)
      - le contenu texte / image
      - les possibleAnswers
    Renvoie False si la question n'existe pas.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()

        row = cur.execute(
            "SELECT id, title, text, position, image FROM Question WHERE id=?",
            (qid,)
        ).fetchone()
        if not row:
            return False

        current_id = row["id"]
        current_pos = row["position"]

        new_title = payload.get("title", row["title"])
        new_text = payload.get("text", row["text"])
        new_image = payload.get("image", row["image"])

        # Gestion du déplacement de position
        target_pos = payload.get("position", current_pos)
        try:
            target_pos = int(target_pos)
        except (TypeError, ValueError):
            target_pos = current_pos

        if target_pos != current_pos:
            # lire tout l'ordre actuel
            rows_all = cur.execute(
                "SELECT id FROM Question ORDER BY position ASC"
            ).fetchall()
            ordered_ids = [r["id"] for r in rows_all]

            # retirer la question courante
            ordered_ids.remove(current_id)

            # insérer à la nouvelle position (1-based)
            insert_index = max(0, min(len(ordered_ids), target_pos - 1))
            ordered_ids.insert(insert_index, current_id)

            # reconstruire positions compactes
            _reorder_all_questions(cur, ordered_ids)

        # mise à jour des champs de contenu
        cur.execute(
            "UPDATE Question SET title=?, text=?, image=? WHERE id=?",
            (new_title, new_text, new_image, current_id)
        )

        # remplacement des réponses si fourni
        if "possibleAnswers" in payload and isinstance(payload["possibleAnswers"], list):
            cur.execute("DELETE FROM Answer WHERE question_id=?", (current_id,))
            for idx, ans in enumerate(payload["possibleAnswers"], start=1):
                a_text = str(ans.get("text", "")).strip()
                a_correct = bool(ans.get("isCorrect", False))
                cur.execute(
                    """
                    INSERT INTO Answer (question_id, text, isCorrect, position)
                    VALUES (?, ?, ?, ?)
                    """,
                    (current_id, a_text, int(a_correct), idx)
                )

        conn.commit()
        return True


def delete_question(qid: int) -> bool:
    """
    Supprime une question et recompacte les positions restantes.
    Renvoie False si l'ID n'existe pas.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()

        row = cur.execute(
            "SELECT id FROM Question WHERE id=?",
            (qid,)
        ).fetchone()
        if not row:
            return False

        # supprimer toutes les réponses d'abord (ON DELETE CASCADE serait suffisant
        # si la contrainte FK est active, mais on le fait explicitement)
        cur.execute("DELETE FROM Answer WHERE question_id=?", (qid,))
        cur.execute("DELETE FROM Question WHERE id=?", (qid,))

        # relire les questions restantes
        rows_left = cur.execute(
            "SELECT id FROM Question ORDER BY position ASC"
        ).fetchall()
        ordered_ids = [r["id"] for r in rows_left]

        # re-compacter les positions 1..n
        _reorder_all_questions(cur, ordered_ids)

        conn.commit()
        return True


def delete_all_questions():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.executescript("DELETE FROM Answer; DELETE FROM Question;")
        conn.commit()


# ========================
# Participations / Scores
# ========================

def create_participation(player_name, answers, mode, time_taken):
    """
    Calcule le score du joueur à partir des réponses,
    enregistre sa participation et son score.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()

        questions = cur.execute(
            "SELECT id FROM Question ORDER BY position ASC"
        ).fetchall()
        total = len(questions)
        score = 0

        # On suppose answers[i] = choix pour question i dans l'ordre du quiz
        for i, q in enumerate(questions):
            if i >= len(answers):
                break
            chosen_position = int(answers[i])  # 1..4
            ans_row = cur.execute(
                """
                SELECT isCorrect
                FROM Answer
                WHERE question_id = ?
                AND position = ?
                """,
                (q["id"], chosen_position)
            ).fetchone()
            if ans_row and ans_row["isCorrect"]:
                score += 1

        # upsert Participation
        cur.execute(
            """
            INSERT INTO Participation (player_name, answers, mode, time_taken)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(player_name)
            DO UPDATE SET
                answers=excluded.answers,
                mode=excluded.mode,
                time_taken=excluded.time_taken
            """,
            (player_name, json.dumps(answers), mode, time_taken)
        )

        # log du score dans Score
        cur.execute(
            "INSERT INTO Score (player, score, total) VALUES (?, ?, ?)",
            (player_name, score, total)
        )

        conn.commit()
        return cur.lastrowid, score


def list_scores(limit=10, mode=None):
    """
    Retourne le classement :
    trié par meilleur score DESC puis created_at ASC.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()
        rows = cur.execute(
            """
            SELECT player, score, total, created_at
            FROM Score
            ORDER BY score DESC, created_at ASC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        return [
            {
                "playerName": r["player"],
                "score": r["score"],
                "date": r["created_at"],
            }
            for r in rows
        ]


def delete_all_participations():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Participation")
        conn.commit()