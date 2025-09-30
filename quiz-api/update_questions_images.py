#!/usr/bin/env python3
"""
Script pour mettre à jour les questions avec des images directement dans la base de données
"""

import sqlite3
import os

DB_PATH = 'quiz.db'

def update_questions_with_images():
    """Met à jour les questions avec des images correspondantes"""
    
    # Mapping des questions vers les images
    question_image_mapping = {
        1: "mega-knight.png",      # Ressource principale
        2: "prince.png",           # Nombre de tours
        3: "mega-knight.png",      # Carte légendaire (Méga chevalier)
        4: "golem.png",            # Première arène
        5: "prince.png",           # Ladder
        6: "mega-knight.png",      # Sort
        7: "dark-prince.png",      # Rareté
        8: "golem.png",            # Guerre de clans
        9: "prince.png",           # Charge (Prince)
        10: "dark-prince.png",     # Bâtiment squelette
        11: "mega-knight.png",     # Ressource d'entraînement
        12: "prince.png",          # Défense de base
        13: "golem.png",           # Priorité
        14: "dark-prince.png",     # Ressources principales
        15: "mega-knight.png",     # Troupe de base
        16: "prince.png",          # Étoiles
        17: "golem.png",           # Cible prioritaire
        18: "dark-prince.png",     # Ligue
        19: "mega-knight.png",     # Vitesse
        20: "prince.png"           # Vol
    }
    
    print("🖼️  MISE À JOUR DES QUESTIONS AVEC DES IMAGES")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        updated_count = 0
        
        for question_id, image_filename in question_image_mapping.items():
            # Récupérer le titre de la question
            cursor.execute('SELECT title FROM Question WHERE id = ?', (question_id,))
            result = cursor.fetchone()
            
            if result:
                title = result[0]
                
                # Mettre à jour l'image
                cursor.execute(
                    'UPDATE Question SET image = ? WHERE id = ?',
                    (image_filename, question_id)
                )
                
                print(f"✅ Question {question_id}: {title}")
                print(f"   Image assignée: {image_filename}")
                updated_count += 1
            else:
                print(f"❌ Question {question_id} non trouvée")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Mise à jour terminée!")
        print(f"   Questions mises à jour: {updated_count}/{len(question_image_mapping)}")
        
        # Afficher le résumé
        print(f"\n📊 RÉSUMÉ DES ASSIGNATIONS D'IMAGES")
        print("-" * 40)
        
        character_counts = {}
        for question_id, image_filename in question_image_mapping.items():
            character = image_filename.replace('.png', '')
            character_counts[character] = character_counts.get(character, 0) + 1
        
        for character, count in character_counts.items():
            print(f"   {character}: {count} questions")
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")

if __name__ == "__main__":
    update_questions_with_images()




