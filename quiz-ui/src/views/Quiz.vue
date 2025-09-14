<template>
  <div class="quiz">
    <div v-if="loading" class="loading">
      <p>Chargement du quiz...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <h2>Erreur</h2>
      <p>{{ error }}</p>
      <button @click="loadQuestions" class="btn btn-primary">Réessayer</button>
    </div>
    
    <div v-else-if="questions.length === 0" class="no-questions">
      <h2>Aucune question disponible</h2>
      <p>Le quiz ne contient pas encore de questions.</p>
      <router-link to="/" class="btn btn-primary">Retour à l'accueil</router-link>
    </div>
    
    <div v-else class="quiz-container">
      <div class="quiz-header">
        <h1>Quiz</h1>
        <div class="progress">
          <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <p>Question {{ currentQuestionIndex + 1 }} sur {{ questions.length }}</p>
      </div>
      
      <div class="question-container">
        <div class="question">
          <h2>{{ currentQuestion.title }}</h2>
          <p v-if="currentQuestion.text">{{ currentQuestion.text }}</p>
          <img v-if="currentQuestion.image" :src="currentQuestion.image" :alt="currentQuestion.title" class="question-image">
        </div>
        
        <div class="answers">
          <div 
            v-for="(answer, index) in currentAnswers" 
            :key="answer.id || index"
            class="answer-option"
            :class="{ selected: selectedAnswer === index }"
            @click="selectAnswer(index)"
          >
            {{ answer.text }}
          </div>
        </div>
        
        <div class="quiz-actions">
          <button 
            v-if="currentQuestionIndex > 0" 
            @click="previousQuestion" 
            class="btn btn-secondary"
          >
            Précédent
          </button>
          
          <button 
            v-if="currentQuestionIndex < questions.length - 1" 
            @click="nextQuestion" 
            class="btn btn-primary"
            :disabled="selectedAnswer === null"
          >
            Suivant
          </button>
          
          <button 
            v-else 
            @click="finishQuiz" 
            class="btn btn-success"
            :disabled="selectedAnswer === null"
          >
            Terminer le Quiz
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const questions = ref([])
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const answers = ref([])
const loading = ref(true)
const error = ref(null)

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || {})
const currentAnswers = computed(() => {
  return currentQuestion.value.answers || []
})
const progressPercentage = computed(() => 
  ((currentQuestionIndex.value + 1) / questions.value.length) * 100
)

const loadQuestions = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await fetch('http://localhost:5001/questions')
    if (response.ok) {
      questions.value = await response.json()
    } else {
      error.value = 'Erreur lors du chargement des questions'
    }
  } catch {
    error.value = 'Impossible de se connecter au serveur'
  } finally {
    loading.value = false
  }
}

const selectAnswer = (index) => {
  selectedAnswer.value = index
}

const nextQuestion = () => {
  if (selectedAnswer.value !== null) {
    answers.value.push({
      questionId: currentQuestion.value.id,
      answer: selectedAnswer.value
    })
    currentQuestionIndex.value++
    selectedAnswer.value = null
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedAnswer.value = answers.value[currentQuestionIndex.value]?.answer || null
  }
}

const finishQuiz = () => {
  if (selectedAnswer.value !== null) {
    answers.value.push({
      questionId: currentQuestion.value.id,
      answer: selectedAnswer.value
    })
  }
  
  // Ici on pourrait envoyer les réponses au serveur
  console.log('Réponses:', answers.value)
  alert('Quiz terminé ! Merci d\'avoir participé.')
  router.push('/')
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.quiz {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.loading, .error, .no-questions {
  text-align: center;
  padding: 3rem;
}

.error h2, .no-questions h2 {
  color: #e74c3c;
  margin-bottom: 1rem;
}

.quiz-container {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.quiz-header {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  padding: 2rem;
  text-align: center;
}

.quiz-header h1 {
  margin: 0 0 1rem 0;
  font-size: 2.5rem;
}

.progress {
  background: rgba(255, 255, 255, 0.3);
  height: 8px;
  border-radius: 4px;
  margin: 1rem 0;
  overflow: hidden;
}

.progress-bar {
  background: white;
  height: 100%;
  transition: width 0.3s ease;
}

.question-container {
  padding: 2rem;
}

.question h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.question p {
  color: #7f8c8d;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.question-image {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin: 1rem 0;
}

.answers {
  margin: 2rem 0;
}

.answer-option {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 0.5rem 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.answer-option:hover {
  background: #e9ecef;
  border-color: #3498db;
}

.answer-option.selected {
  background: #3498db;
  color: white;
  border-color: #2980b9;
}

.quiz-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
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
</style>
