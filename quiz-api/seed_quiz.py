#!/usr/bin/env python3
# seed_quiz.py
# Script de seed pour un quiz Clash Royale / Clash of Clans.
# - Par défaut: imprime le JSON complet (à copier-coller si besoin).
# - Optionnel: envoi direct à l'API via POST /questions (une par une).
#
# Exemple:
#   python seed_quiz.py                          # imprime le JSON
#   python seed_quiz.py --post                   # POST vers http://127.0.0.1:5001
#   python seed_quiz.py --post --base-url http://localhost:5001 --token "Bearer x.y.z"

import json
import argparse
from typing import List, Dict, Any

try:
    import requests  # seulement nécessaire si tu utilises --post
except ImportError:
    requests = None

def make_q(position: int, title: str, text: str, options: List[str], correct_index: int, image: str = "") -> Dict[str, Any]:
    """
    Construit un dictionnaire question compatible avec l'API.
    Valide que l'index de la bonne réponse est dans les bornes.
    """
    assert 0 <= correct_index < len(options), "correct_index hors bornes"
    answers = []
    for i, opt in enumerate(options, start=1):
        answers.append({
            "text": opt,
            "position": i,
            "isCorrect": (i - 1) == correct_index
        })
    return {
        "title": title,
        "text": text,
        "image": image,
        "position": position,
        "answers": answers
    }

def build_questions() -> List[Dict[str, Any]]:
    q: List[Dict[str, Any]] = []
    pos = 1

    # -------- Clash Royale (10) --------
    q.append(make_q(pos, "Clash Royale — Ressource principale",
                    "Quelle est la ressource utilisée pour poser des cartes ?",
                    ["Or", "Élixir", "Gemmes", "Mana"], correct_index=1)); pos += 1

    q.append(make_q(pos, "Clash Royale — Nombre de tours",
                    "Combien de tours possède chaque joueur au début d'une partie ?",
                    ["1", "2", "3", "4"], correct_index=2)); pos += 1

    q.append(make_q(pos, "Clash Royale — Carte légendaire",
                    "Quelle carte légendaire saute et écrase les troupes en zone ?",
                    ["Méga chevalier", "Prince", "Golem", "Chevaucheur de cochon"], correct_index=0)); pos += 1

    q.append(make_q(pos, "Clash Royale — Première arène",
                    "Quelle arène est débloquée en premier dans le jeu ?",
                    ["Arène légendaire", "Arène gobeline", "Camp d'entraînement", "Arène royale"], correct_index=2)); pos += 1

    q.append(make_q(pos, "Clash Royale — Ladder",
                    "Combien de trophées gagne-t-on typiquement par victoire en ladder (hors ligues) ?",
                    ["10", "20", "30", "50"], correct_index=2)); pos += 1

    q.append(make_q(pos, "Clash Royale — Sort",
                    "Laquelle de ces cartes est un sort ?",
                    ["Mousquetaire", "Boule de feu", "Géant", "Prince ténébreux"], correct_index=1)); pos += 1

    q.append(make_q(pos, "Clash Royale — Rareté",
                    "Quelle rareté est la plus élevée dans Clash Royale ?",
                    ["Commune", "Rare", "Épique", "Légendaire"], correct_index=3)); pos += 1

    q.append(make_q(pos, "Clash Royale — Guerre de clans",
                    "Combien de joueurs participent à une guerre de clans (maximum) ?",
                    ["10", "20", "30", "50"], correct_index=3)); pos += 1

    q.append(make_q(pos, "Clash Royale — Charge",
                    "Quelle troupe charge et inflige des dégâts doublés sur sa première attaque ?",
                    ["Prince", "Arbalète", "Sorcier", "Chevalier"], correct_index=0)); pos += 1

    q.append(make_q(pos, "Clash Royale — Bâtiment squelette",
                    "Quelle carte invoque des squelettes en continu jusqu'à destruction ?",
                    ["Armée de squelettes", "Cimetière", "Cabane de gobelins", "Tombeau"], correct_index=3)); pos += 1

    # -------- Clash of Clans (10) --------
    q.append(make_q(pos, "Clash of Clans — Ressource d'entraînement",
                    "Quelle ressource permet d'entraîner des troupes ?",
                    ["Élixir", "Or", "Gemmes", "Pierre"], correct_index=0)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Défense de base",
                    "Quel bâtiment défensif tire des flèches sur les ennemis ?",
                    ["Cabane", "Tour de l'archer", "Hôtel de ville", "Mine"], correct_index=1)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Priorité",
                    "Quel bâtiment est le plus important à protéger ?",
                    ["Caserne", "Hôtel de ville", "Camp militaire", "Laboratoire"], correct_index=1)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Ressources principales",
                    "Combien de ressources principales existent (hors gemmes) ?",
                    ["2", "3", "4", "5"], correct_index=1)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Troupe de base",
                    "Quelle troupe de base est disponible dès le début ?",
                    ["Barbare", "Dragon", "P.E.K.K.A", "Guérisseuse"], correct_index=0)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Étoiles",
                    "Que se passe-t-il si ton Hôtel de ville est détruit ?",
                    ["Rien", "Tu gagnes", "Tu perds une étoile", "Tu obtiens un bonus"], correct_index=2)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Cible prioritaire",
                    "Quelle troupe attaque les défenses en priorité ?",
                    ["Barbares", "Archers", "Géants", "Sorciers"], correct_index=2)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Ligue",
                    "Quelle ligue est la plus prestigieuse ?",
                    ["Argent", "Or", "Cristal", "Légende"], correct_index=3)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Vitesse",
                    "Quel sort rend tes troupes plus rapides (et plus offensives) ?",
                    ["Sort de soin", "Sort de rage", "Sort de gel", "Sort de foudre"], correct_index=1)); pos += 1

    q.append(make_q(pos, "Clash of Clans — Vol",
                    "Quelle troupe peut voler au-dessus des murs ?",
                    ["Barbare", "Dragon", "Géant", "Golem"], correct_index=1)); pos += 1

    return q

def post_questions(base_url: str, token: str = "") -> None:
    if requests is None:
        raise RuntimeError("Le module 'requests' n'est pas installé. Fais: pip install requests")

    questions = build_questions()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = token  # ex: "Bearer <ton_token>"

    # Suppose un endpoint POST /questions qui accepte une question à la fois.
    # Adapte si ton API attend un bulk (/questions/bulk).
    created, failed = 0, 0
    for item in questions:
        url = f"{base_url.rstrip('/')}/questions"
        try:
            resp = requests.post(url, headers=headers, json=item, timeout=10)
            if resp.status_code in (200, 201):
                created += 1
            else:
                failed += 1
                print(f"[!] {resp.status_code} position={item['position']} body={resp.text}")
        except requests.RequestException as e:
            failed += 1
            print(f"[!] network error position={item['position']} err={e}")

    print(f"Terminé. Créées: {created}, Échecs: {failed}")

def main():
    parser = argparse.ArgumentParser(description="Seeder de questions Clash Royale / Clash of Clans")
    parser.add_argument("--post", action="store_true",
                        help="Envoi direct à l'API via POST /questions")
    parser.add_argument("--base-url", default="http://127.0.0.1:5001",
                        help="Base URL de l'API (défaut: http://127.0.0.1:5001)")
    parser.add_argument("--token", default="",
                        help="Chaîne Authorization (ex: 'Bearer x.y.z') si ton API est protégée")
    parser.add_argument("--pretty", action="store_true",
                        help="Imprimer un JSON formaté (si pas de --post)")
    args = parser.parse_args()

    if args.post:
        post_questions(args.base_url, args.token)
    else:
        payload = build_questions()
        if args.pretty:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(payload, ensure_ascii=False))

if __name__ == "__main__":
    main()


