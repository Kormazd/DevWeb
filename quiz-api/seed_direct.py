#!/usr/bin/env python3
# seed_direct.py
# Script pour insérer directement les questions dans la base de données SQLite

import sqlite3
import json
from typing import List, Dict, Any

def make_q(position: int, title: str, text: str, options: List[str], correct_index: int, image: str = "") -> Dict[str, Any]:
    """
    Construit un dictionnaire question compatible avec la base de données
    """
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

def insert_questions_direct():
    """Insère directement les questions dans la base de données SQLite"""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    # Vider les tables existantes
    cursor.execute('DELETE FROM Answer')
    cursor.execute('DELETE FROM Question')
    conn.commit()
    
    questions = build_questions()
    created = 0
    
    for question in questions:
        try:
            # Insérer la question
            cursor.execute('''
                INSERT INTO Question (title, text, position, image)
                VALUES (?, ?, ?, ?)
            ''', (question['title'], question['text'], question['position'], question['image']))
            
            question_id = cursor.lastrowid
            
            # Insérer les réponses
            for answer in question['answers']:
                cursor.execute('''
                    INSERT INTO Answer (question_id, text, isCorrect, position)
                    VALUES (?, ?, ?, ?)
                ''', (question_id, answer['text'], answer['isCorrect'], answer['position']))
            
            created += 1
            print(f"✓ Question {question['position']}: {question['title']}")
            
        except Exception as e:
            print(f"✗ Erreur pour question {question['position']}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Terminé ! {created} questions créées dans la base de données.")

if __name__ == "__main__":
    insert_questions_direct()


