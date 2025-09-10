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

## 📁 Structure du projet

```
DevWeb/
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
