# Corrections du Quiz - Images et Réponses

## 🎯 Objectifs atteints

✅ Les images des questions s'affichent correctement dans le quiz  
✅ Les 4 propositions de réponses apparaissent sous forme de boutons cliquables  
✅ Support de plusieurs chemins d'images (`/assets/`, `/uploads/`)

---

## 🔧 Modifications Backend (Flask)

### 1. Endpoint `/questions` - Ajout du champ `answers`

**Fichier**: `quiz-api/app.py`

Les endpoints suivants ont été modifiés pour renvoyer à la fois `possibleAnswers` (pour l'admin) et `answers` (pour le quiz) :

- `GET /questions` - Liste toutes les questions
- `GET /questions/<int:qid>` - Récupère une question par ID
- `GET /questions/admin` - Version admin

```python
@app.get("/questions")
def get_questions():
    # ...
    for q in list_questions():
        item = question_to_dict(q)
        item["possibleAnswers"] = list_answers_for_question(q.id)
        item["answers"] = list_answers_for_question(q.id)  # ✅ AJOUTÉ
        questions.append(item)
    
    return {"items": questions}, 200
```

### 2. Nouvel endpoint `/uploads/` pour servir les images

**Fichier**: `quiz-api/app.py`

Ajout d'un endpoint supplémentaire pour servir les fichiers uploadés :

```python
@app.get("/uploads/<path:filename>")
def serve_upload(filename):
    """Sert les fichiers uploadés (alias pour /assets/)."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
```

**Endpoints disponibles pour les images** :
- `/assets/<filename>` - Endpoint principal
- `/uploads/<filename>` - Alias pour compatibilité

---

## 🎨 Modifications Frontend (Vue 3)

### 1. QuizPage.vue - Gestion des URLs d'images

**Fichier**: `quiz-ui/src/components/QuizPage.vue`

Ajout d'une fonction helper pour construire automatiquement les URLs complètes des images :

```javascript
// Helper pour construire l'URL complète de l'image
function getImageUrl(imagePath) {
  if (!imagePath) return null
  // Si c'est déjà une URL complète, la retourner telle quelle
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath
  }
  // Construire l'URL à partir de l'API base URL
  const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5001'
  // Si le chemin commence par /, l'utiliser tel quel, sinon ajouter /assets/
  if (imagePath.startsWith('/')) {
    return `${baseURL}${imagePath}`
  }
  return `${baseURL}/assets/${imagePath}`
}
```

### 2. Mise à jour de la fonction `load()`

La fonction `load()` mappe maintenant les questions pour s'assurer que `image_url` est toujours définie :

```javascript
async function load() {
  loading.value = true
  error.value = ''
  const { status, data } = await QuizApi.getQuestions()
  if (status >= 200 && status < 300 && Array.isArray(data)) {
    // S'assurer que les URLs d'images sont complètes
    questions.value = data.map(q => ({
      ...q,
      image_url: q.image_url || (q.image ? getImageUrl(q.image) : null)
    }))
  } else {
    error.value = data?.error || 'Impossible de charger les questions'
  }
  loading.value = false
}
```

### 3. Affichage dans le template

**Le template affiche déjà correctement** :
- ✅ L'image de la question : `<img v-if="currentQuestion.image_url" :src="currentQuestion.image_url" />`
- ✅ Les 4 réponses sous forme de boutons cliquables avec feedback visuel
- ✅ Gestion du clic pour sélectionner une réponse
- ✅ Affichage de la bonne réponse (vert) et mauvaise (rouge) après validation

---

## 📊 Structure des données

### Réponse API `/questions`

```json
{
  "items": [
    {
      "id": 1,
      "title": "Question titre",
      "text": "Description de la question",
      "position": 1,
      "image": "abc123.jpg",
      "image_url": "/assets/abc123.jpg",
      "possibleAnswers": [
        { "text": "Réponse 1", "isCorrect": false },
        { "text": "Réponse 2", "isCorrect": true },
        { "text": "Réponse 3", "isCorrect": false },
        { "text": "Réponse 4", "isCorrect": false }
      ],
      "answers": [
        { "text": "Réponse 1", "isCorrect": false },
        { "text": "Réponse 2", "isCorrect": true },
        { "text": "Réponse 3", "isCorrect": false },
        { "text": "Réponse 4", "isCorrect": false }
      ]
    }
  ]
}
```

---

## 🎮 Fonctionnalités du Quiz

### Affichage des questions

1. **Titre de la question** : `currentQuestion.title`
2. **Description** : `currentQuestion.text` (si présente)
3. **Image** : `currentQuestion.image_url` (si présente)
4. **4 réponses** : Boutons numérotés de 1 à 4

### Interaction utilisateur

- Clic sur une réponse pour la sélectionner
- La réponse sélectionnée est mise en surbrillance (bordure jaune)
- Après validation :
  - ✅ Bonne réponse → fond vert avec animation
  - ❌ Mauvaise réponse → fond rouge avec animation
- Délai d'1 seconde avant de passer à la question suivante

### Fonctionnalités spéciales

- **Easter egg "SUPERCELL"** : Affiche un indicateur ★ sur la bonne réponse
- **Pause** : Met le quiz en pause
- **Partager** : Partage la progression
- **Arrêter** : Arrête le quiz avec confirmation

---

## 🚀 Pour tester

1. **Créer une question avec image dans l'admin**
   - Aller sur `/admin`
   - Se connecter
   - Créer une nouvelle question
   - Uploader une image
   - Ajouter 4 réponses

2. **Lancer le quiz**
   - Aller sur `/new-quiz`
   - Entrer un nom
   - Commencer le quiz
   - Vérifier que l'image s'affiche
   - Vérifier que les 4 réponses sont cliquables

3. **Vérifier les URLs**
   - Les images avec `/assets/` fonctionnent
   - Les images avec `/uploads/` fonctionnent
   - Les URLs complètes (http://) fonctionnent

---

## 📝 Variables d'environnement

Assurez-vous que `VITE_API_URL` est définie correctement :

```env
# .env (frontend)
VITE_API_URL=http://localhost:5001
```

---

## ✅ Checklist finale

- [x] Backend renvoie `answers` avec `isCorrect`
- [x] Endpoint `/uploads/` ajouté
- [x] Endpoint `/assets/` existe déjà
- [x] Frontend construit les URLs complètes
- [x] Images s'affichent dans le quiz
- [x] 4 réponses affichées sous forme de boutons
- [x] Sélection des réponses fonctionne
- [x] Feedback visuel (vert/rouge) fonctionne
- [x] Pas d'erreurs de linting

---

## 🐛 Dépannage

### L'image ne s'affiche pas

1. Vérifier que le fichier existe dans `quiz-api/uploads/`
2. Vérifier les logs Flask pour voir si l'endpoint est appelé
3. Vérifier la console du navigateur pour les erreurs 404
4. Vérifier que `VITE_API_URL` est correct

### Les réponses ne s'affichent pas

1. Vérifier que le backend renvoie bien `answers` dans la réponse
2. Vérifier dans l'onglet Network du navigateur
3. Vérifier que chaque réponse a `text` et `isCorrect`

### Erreur CORS

Si vous avez des erreurs CORS, vérifiez que Flask CORS est bien configuré dans `app.py` :

```python
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
```

