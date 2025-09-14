<template>
  <div class="admin">
    <div v-if="!isAuthenticated" class="login-form">
      <h2>Connexion Administrateur</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="password">Mot de passe :</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            class="form-control"
          >
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
        <div v-if="loginError" class="error-message">
          {{ loginError }}
        </div>
      </form>
    </div>
    
    <div v-else class="admin-dashboard">
      <div class="admin-header">
        <h1>Administration du Quiz</h1>
        <button @click="logout" class="btn btn-secondary">Déconnexion</button>
      </div>
      
      <div class="admin-content">
        <div class="quiz-stats">
          <h3>Statistiques</h3>
          <p>Nombre de questions : <strong>{{ questions.length }}</strong></p>
        </div>
        
        <div class="questions-management">
          <div class="section-header">
            <h3>Gestion des Questions</h3>
            <button @click="showAddForm = true" class="btn btn-primary">
              Ajouter une Question
            </button>
          </div>
          
          <div v-if="showAddForm" class="add-question-form">
            <h4>Nouvelle Question</h4>
            <form @submit.prevent="addQuestion">
              <div class="form-group">
                <label for="title">Titre :</label>
                <input type="text" id="title" v-model="newQuestion.title" required class="form-control">
              </div>
              
              <div class="form-group">
                <label for="text">Texte :</label>
                <textarea id="text" v-model="newQuestion.text" class="form-control" rows="3"></textarea>
              </div>
              
              <div class="form-group">
                <label for="position">Position :</label>
                <input type="number" id="position" v-model="newQuestion.position" required class="form-control">
              </div>
              
              <div class="form-group">
                <label for="image">Image (URL) :</label>
                <input type="url" id="image" v-model="newQuestion.image" class="form-control">
              </div>
              
              <div class="form-group">
                <label>Réponses possibles :</label>
                <div v-for="(answer, index) in newQuestion.answers" :key="index" class="answer-input">
                  <div class="answer-row">
                    <input 
                      type="text" 
                      v-model="answer.text" 
                      :placeholder="`Réponse ${index + 1}`"
                      class="form-control answer-text"
                    >
                    <label class="checkbox-label">
                      <input 
                        type="checkbox" 
                        v-model="answer.isCorrect"
                        class="answer-checkbox"
                      >
                      Correcte
                    </label>
                    <button 
                      type="button" 
                      @click="removeAnswer(index)" 
                      class="btn btn-danger btn-sm"
                      v-if="newQuestion.answers.length > 1"
                    >
                      ×
                    </button>
                  </div>
                </div>
                <button 
                  type="button" 
                  @click="addAnswer" 
                  class="btn btn-secondary btn-sm"
                >
                  + Ajouter une réponse
                </button>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-success" :disabled="loading">
                  {{ loading ? 'Ajout...' : 'Ajouter' }}
                </button>
                <button type="button" @click="cancelAdd" class="btn btn-secondary">
                  Annuler
                </button>
              </div>
            </form>
          </div>
          
          <div class="questions-list">
            <div v-if="questions.length === 0" class="no-questions">
              <p>Aucune question disponible</p>
            </div>
            
            <div v-else>
              <div v-for="question in questions" :key="question.id" class="question-item">
                <div class="question-content">
                  <h4>{{ question.title }}</h4>
                  <p v-if="question.text">{{ question.text }}</p>
                  <p class="question-meta">
                    Position: {{ question.position }} | ID: {{ question.id }}
                  </p>
                </div>
                <div class="question-actions">
                  <button @click="deleteQuestion(question.id)" class="btn btn-danger btn-sm">
                    Supprimer
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isAuthenticated = ref(false)
const token = ref('')
const password = ref('')
const loading = ref(false)
const loginError = ref('')
const questions = ref([])
const showAddForm = ref(false)
const newQuestion = ref({
  title: '',
  text: '',
  position: 1,
  image: '',
  answers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false }
  ]
})

const login = async () => {
  try {
    loading.value = true
    loginError.value = ''
    
    const response = await fetch('http://localhost:5001/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ password: password.value })
    })
    
    if (response.ok) {
      const data = await response.json()
      token.value = data.token
      isAuthenticated.value = true
      password.value = ''
      loadQuestions()
    } else {
      loginError.value = 'Mot de passe incorrect'
    }
  } catch {
    loginError.value = 'Erreur de connexion'
  } finally {
    loading.value = false
  }
}

const logout = () => {
  isAuthenticated.value = false
  token.value = ''
  questions.value = []
}

const loadQuestions = async () => {
  try {
    const response = await fetch('http://localhost:5001/questions')
    if (response.ok) {
      questions.value = await response.json()
    }
  } catch {
    console.error('Erreur lors du chargement des questions')
  }
}

const addQuestion = async () => {
  try {
    loading.value = true
    
    const response = await fetch('http://localhost:5001/questions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token.value}`
      },
      body: JSON.stringify(newQuestion.value)
    })
    
    if (response.ok) {
      await loadQuestions()
      cancelAdd()
    } else {
      const error = await response.json()
      alert('Erreur lors de l\'ajout: ' + (error.error || 'Erreur inconnue'))
    }
  } catch {
    alert('Erreur de connexion')
  } finally {
    loading.value = false
  }
}

const deleteQuestion = async (questionId) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cette question ?')) {
    return
  }
  
  try {
    const response = await fetch(`http://localhost:5001/questions/${questionId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })
    
    if (response.ok) {
      await loadQuestions()
    } else {
      alert('Erreur lors de la suppression')
    }
  } catch {
    alert('Erreur de connexion')
  }
}

const addAnswer = () => {
  newQuestion.value.answers.push({ text: '', isCorrect: false })
}

const removeAnswer = (index) => {
  if (newQuestion.value.answers.length > 1) {
    newQuestion.value.answers.splice(index, 1)
  }
}

const cancelAdd = () => {
  showAddForm.value = false
  newQuestion.value = {
    title: '',
    text: '',
    position: 1,
    image: '',
    answers: [
      { text: '', isCorrect: false },
      { text: '', isCorrect: false }
    ]
  }
}

onMounted(() => {
  // Vérifier si on a déjà un token en session
  const savedToken = localStorage.getItem('adminToken')
  if (savedToken) {
    token.value = savedToken
    isAuthenticated.value = true
    loadQuestions()
  }
})
</script>

<style scoped>
.admin {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.login-form {
  max-width: 400px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-form h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.admin-dashboard {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.admin-header {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-header h1 {
  margin: 0;
}

.admin-content {
  padding: 2rem;
}

.quiz-stats {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.quiz-stats h3 {
  margin-top: 0;
  color: #2c3e50;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h3 {
  margin: 0;
  color: #2c3e50;
}

.add-question-form {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.add-question-form h4 {
  margin-top: 0;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.questions-list {
  margin-top: 2rem;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  background: white;
}

.question-content h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.question-content p {
  margin: 0.5rem 0;
  color: #7f8c8d;
}

.question-meta {
  font-size: 0.9rem;
  color: #95a5a6;
}

.question-actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-success {
  background: #27ae60;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #229954;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.error-message {
  color: #e74c3c;
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fdf2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
}

.no-questions {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.answer-input {
  margin-bottom: 1rem;
}

.answer-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.answer-text {
  flex: 1;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  margin: 0;
}

.answer-checkbox {
  margin: 0;
}
</style>
