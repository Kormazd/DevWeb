#!/usr/bin/env python3
"""
Script de validation finale pour vérifier que tous les assets et questions sont correctement servis
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5001"

def validate_api():
    """Valide que l'API fonctionne correctement"""
    
    print("🔍 VALIDATION FINALE DE L'API QUIZ")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: Endpoints de base
    print("\n1️⃣  Test des endpoints de base")
    endpoints = [
        ("/", "Page d'accueil"),
        ("/quiz-info", "Informations du quiz"),
        ("/assets", "Liste des assets"),
        ("/quiz-complete", "Données complètes")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {description}: OK")
            else:
                print(f"   ❌ {description}: Erreur {response.status_code}")
                all_tests_passed = False
        except Exception as e:
            print(f"   ❌ {description}: {e}")
            all_tests_passed = False
    
    # Test 2: Assets individuels
    print("\n2️⃣  Test des assets individuels")
    assets = ["mega-knight.png", "prince.png", "dark-prince.png", "golem.png"]
    
    for asset in assets:
        try:
            response = requests.get(f"{BASE_URL}/assets/{asset}", timeout=10)
            if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('image/'):
                print(f"   ✅ {asset}: OK ({response.headers.get('Content-Length')} bytes)")
            else:
                print(f"   ❌ {asset}: Erreur {response.status_code}")
                all_tests_passed = False
        except Exception as e:
            print(f"   ❌ {asset}: {e}")
            all_tests_passed = False
    
    # Test 3: Questions avec images
    print("\n3️⃣  Test des questions avec images")
    try:
        response = requests.get(f"{BASE_URL}/questions", timeout=10)
        if response.status_code == 200:
            questions = response.json()
            questions_with_images = 0
            
            for question in questions:
                if question.get('image_url'):
                    questions_with_images += 1
            
            print(f"   ✅ Questions totales: {len(questions)}")
            print(f"   ✅ Questions avec images: {questions_with_images}")
            
            if questions_with_images == len(questions):
                print("   ✅ Toutes les questions ont des images")
            else:
                print(f"   ⚠️  {len(questions) - questions_with_images} questions sans images")
                all_tests_passed = False
        else:
            print(f"   ❌ Erreur lors de la récupération des questions: {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        all_tests_passed = False
    
    # Test 4: Données complètes
    print("\n4️⃣  Test des données complètes")
    try:
        response = requests.get(f"{BASE_URL}/quiz-complete", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            quiz_info = data.get('quiz', {})
            assets_info = data.get('assets', {})
            
            print(f"   ✅ Questions: {quiz_info.get('total_questions', 0)}")
            print(f"   ✅ Assets: {assets_info.get('total_assets', 0)}")
            print(f"   ✅ Version API: {data.get('api_info', {}).get('version', 'N/A')}")
            
            if quiz_info.get('total_questions', 0) >= 20 and assets_info.get('total_assets', 0) >= 4:
                print("   ✅ Données complètes disponibles")
            else:
                print("   ⚠️  Données incomplètes")
                all_tests_passed = False
        else:
            print(f"   ❌ Erreur lors de la récupération des données complètes: {response.status_code}")
            all_tests_passed = False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        all_tests_passed = False
    
    # Résumé final
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 VALIDATION RÉUSSIE!")
        print("   Tous les assets et questions sont correctement servis")
        print("   L'API est prête à être utilisée")
    else:
        print("❌ VALIDATION ÉCHOUÉE!")
        print("   Certains tests ont échoué")
        print("   Vérifiez les erreurs ci-dessus")
    
    return all_tests_passed

def main():
    validate_api()

if __name__ == "__main__":
    main()


