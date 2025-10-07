# 🎮 Quiz API - Clash Royale & Clash of Clans

## 📋 Vue d'ensemble

Cette API fournit un quiz complet sur les jeux Clash Royale et Clash of Clans, avec des questions, des réponses, et des assets visuels (images des personnages).

## 🚀 Endpoints disponibles

### Informations générales
- `GET /` - Page d'accueil de l'API
- `GET /quiz-info` - Informations de base sur le quiz (nombre de questions)
- `GET /quiz-complete` - Toutes les données du quiz (questions + assets + métadonnées)

### Questions
- `GET /questions` - Liste de toutes les questions avec réponses
- `GET /questions/<id>` - Question spécifique par ID
- `POST /questions` - Créer une nouvelle question (authentification requise)
- `DELETE /questions/<id>` - Supprimer une question (authentification requise)

### Assets (Images)
- `GET /assets` - Liste de tous les assets disponibles
- `GET /assets/<filename>` - Récupérer un asset spécifique

### Authentification
- `POST /login` - Se connecter et obtenir un token

## 📊 Données disponibles

### Questions (20 au total)
- **Clash Royale** : 10 questions
- **Clash of Clans** : 10 questions
- Chaque question a :
  - Un titre
  - Une description
  - 4 réponses (une correcte)
  - Une image associée

### Assets (4 images)
- `mega-knight.png` - Méga Chevalier
- `prince.png` - Prince
- `dark-prince.png` - Prince Ténébreux
- `golem.png` - Golem

## 🔧 Utilisation

### Démarrer l'API
```bash
cd quiz-api
python3 app.py
```

### Tester l'API
```bash
# Informations du quiz
curl http://localhost:5001/quiz-info

# Toutes les questions
curl http://localhost:5001/questions

# Tous les assets
curl http://localhost:5001/assets

# Données complètes
curl http://localhost:5001/quiz-complete
```

### Accéder aux images
```bash
# Image du Méga Chevalier
curl http://localhost:5001/assets/mega-knight.png

# Image du Prince
curl http://localhost:5001/assets/prince.png
```

## 📝 Structure des données

### Question
```json
{
  "id": 1,
  "title": "Clash Royale — Ressource principale",
  "text": "Quelle est la ressource utilisée pour poser des cartes ?",
  "position": 1,
  "image": "mega-knight.png",
  "image_url": "/assets/mega-knight.png",
  "answers": [
    {
      "id": 1,
      "text": "Or",
      "isCorrect": false,
      "position": 1
    },
    {
      "id": 2,
      "text": "Élixir",
      "isCorrect": true,
      "position": 2
    }
  ]
}
```

### Asset
```json
{
  "filename": "mega-knight.png",
  "name": "mega-knight",
  "url": "/assets/mega-knight.png"
}
```

## 🛠️ Scripts utilitaires

- `test_api.py` - Test complet de l'API
- `display_quiz.py` - Affichage organisé de toutes les données
- `final_validation.py` - Validation finale de l'API
- `update_questions_images.py` - Mise à jour des images des questions

## ✅ Statut

- ✅ API fonctionnelle
- ✅ 20 questions avec images
- ✅ 4 assets visuels
- ✅ Tous les endpoints opérationnels
- ✅ Validation complète réussie

## 🎯 Prochaines étapes

1. Intégration avec le frontend Vue.js
2. Ajout de nouvelles questions
3. Système de scoring
4. Statistiques de jeu


