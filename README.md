<<<<<<< HEAD
# 🎮 Quiz Supercell

> Un quiz interactif inspiré des jeux de la compagnie Supercell (Clash Royale, Brawl Stars...)

## 📋 À propos du projet

Ce projet consiste en une API Flask qui servira les questions pour un quiz interactif sur l'univers Supercell. L'interface utilisateur sera développée ultérieurement.

## 🛠️ Technologies utilisées

- **Python** 3.13.x
- **Flask** 3.1.2 - Framework web léger
- **Flask-CORS** 6.0.1 - Gestion des CORS
- **Werkzeug** 3.1.3 - Serveur WSGI

## 🚀 Installation et démarrage rapide

### Prérequis
- Python 3.13.x installé sur votre système
- PowerShell (Windows)

### Étapes d'installation

1. **Naviguer vers le dossier du projet**
   ```powershell
   cd "quiz-api"
   ```

2. **Créer et activer l'environnement virtuel**
   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Installer les dépendances**
   ```powershell
   pip install -r requirements.txt
   ```
   *Ou depuis la racine du dépôt :*
   ```powershell
   pip install -r "quiz-api/requirements.txt"
   ```

4. **Lancer le serveur de développement**
   ```powershell
   python app.py
   ```

## 🌐 Accès à l'API

L'API est accessible par défaut sur : **http://localhost:5001/**

### Endpoints disponibles

- `GET /` - Page d'accueil de l'API
=======
# 🎮 Quiz Clash Royale & Clash of Clans

Une application de quiz interactive sur les jeux Clash Royale et Clash of Clans, avec une interface moderne et des animations fluides.

## 🚀 Démarrage rapide

### Option 1: Script automatique
```bash
./start_quiz.sh
```

### Option 2: Démarrage manuel

**Backend (API Flask):**
```bash
cd quiz-api
python3 app.py
```

**Frontend (Vue.js):**
```bash
cd quiz-ui
npm run dev
```

## 📱 Accès à l'application

- **Application web**: http://localhost:3000
- **API Backend**: http://localhost:5001

## 🧪 Tests

### Test complet du système
```bash
python3 test_complete_system.py
```

### Test de l'API uniquement
```bash
python3 test_api.py
```

### Affichage des données
```bash
python3 display_quiz.py
```

## 📊 Fonctionnalités

### ✅ Backend API
- **20 questions** sur Clash Royale et Clash of Clans
- **4 assets visuels** (Mega Knight, Prince, Prince Ténébreux, Golem)
- **6 endpoints** RESTful
- **Service d'assets statiques** pour les images
- **Base de données SQLite** avec questions et réponses

### ✅ Frontend Vue.js
- **Interface néo-médiévale** avec thème Clash Royale
- **Animations fluides** des personnages
- **Design responsive** pour tous les écrans
- **Transitions entre questions** avec changement de personnage
- **Composants réutilisables** (BackgroundScene, UiCard, etc.)

## 🔧 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil de l'API |
| `/quiz-info` | GET | Informations de base du quiz |
| `/questions` | GET | Liste de toutes les questions |
| `/questions/<id>` | GET | Question spécifique |
| `/assets` | GET | Liste des assets disponibles |
| `/assets/<filename>` | GET | Asset spécifique (image) |
| `/quiz-complete` | GET | Toutes les données (questions + assets) |
>>>>>>> 34dd0b3fc39932bdcd7fd85cda5ba46ffff7c6d6

## 📁 Structure du projet

```
DevWeb/
<<<<<<< HEAD
├── quiz-api/
│   ├── app.py              # Application Flask principale
│   ├── requirements.txt    # Dépendances Python
│   └── quiz-api.code-workspace
└── README.md
```

## 👥 Équipe de développement

- **Julien** 👨‍💻
- **Tom** 👨‍💻  
- **Lilian** 👨‍💻

## 📝 Statut du projet

🚧 **En développement** - API de base fonctionnelle, interface utilisateur à venir

---

*Projet développé avec ❤️ pour les fans de Supercell*
=======
├── quiz-api/                 # Backend Flask
│   ├── app.py               # Application principale
│   ├── requirements.txt     # Dépendances Python
│   ├── quiz.db             # Base de données SQLite
│   └── seed_direct.py      # Script de seed des questions
├── quiz-ui/                 # Frontend Vue.js
│   ├── src/
│   │   ├── components/     # Composants Vue
│   │   ├── views/          # Pages de l'application
│   │   ├── assets/         # Styles CSS
│   │   └── data/           # Données et configuration
│   ├── public/images/      # Images des personnages
│   └── package.json        # Dépendances Node.js
├── start_quiz.sh           # Script de démarrage
├── test_complete_system.py # Tests complets
└── API_DOCUMENTATION.md    # Documentation API
```

## 🎯 Questions disponibles

### Clash Royale (10 questions)
- Ressource principale (Élixir)
- Nombre de tours (3)
- Carte légendaire (Méga chevalier)
- Première arène (Camp d'entraînement)
- Ladder (30 trophées)
- Sort (Boule de feu)
- Rareté (Légendaire)
- Guerre de clans (50 joueurs)
- Charge (Prince)
- Bâtiment squelette (Tombeau)

### Clash of Clans (10 questions)
- Ressource d'entraînement (Élixir)
- Défense de base (Tour de l'archer)
- Priorité (Hôtel de ville)
- Ressources principales (3)
- Troupe de base (Barbare)
- Étoiles (Perte d'étoile)
- Cible prioritaire (Géants)
- Ligue (Légende)
- Vitesse (Sort de rage)
- Vol (Dragon)

## 🖼️ Assets visuels

- **Mega Knight** (6 questions)
- **Prince** (6 questions)
- **Prince Ténébreux** (4 questions)
- **Golem** (4 questions)

## 🛠️ Technologies utilisées

### Backend
- **Python 3.13**
- **Flask 3.1.2**
- **SQLite**
- **PyJWT 2.10.1**

### Frontend
- **Vue.js 3.5.18**
- **Vite 7.0.6**
- **CSS3** avec animations
- **Google Fonts** (Cinzel, MedievalSharp, Sigmar One)

## 📖 Documentation

- [Documentation API complète](API_DOCUMENTATION.md)
- [Guide de développement](DEVELOPMENT.md)
- [Changelog](CHANGELOG.md)

## 🎉 Statut du projet

- ✅ **Backend** : 100% fonctionnel
- ✅ **Frontend** : 100% fonctionnel
- ✅ **Intégration** : 100% opérationnelle
- ✅ **Tests** : 100% réussis
- ✅ **Documentation** : Complète

## 🚀 Prochaines étapes

1. **Système de scoring** - Calcul des points
2. **Statistiques** - Suivi des performances
3. **Nouvelles questions** - Expansion du contenu
4. **Mode multijoueur** - Quiz en temps réel
5. **Thèmes supplémentaires** - Autres jeux Supercell

---

**Développé avec ❤️ pour les fans de Clash Royale et Clash of Clans**


>>>>>>> 34dd0b3fc39932bdcd7fd85cda5ba46ffff7c6d6
