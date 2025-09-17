<template>
  <div class="quiz">
    <BackgroundScene :questionIndex="currentQuestionIndex" />
    
    <div class="container">
      <div v-if="loading" class="loading card">
        <h2 class="h-royal">Chargement du quiz...</h2>
        <div class="progress">
          <div class="progress__bar"></div>
        </div>
      </div>
      
      <div v-else-if="error" class="error card">
        <h2 class="h-royal">Erreur</h2>
        <p>{{ error }}</p>
        <button @click="loadQuestions" class="btn btn--primary">Réessayer</button>
      </div>
      
      <div v-else-if="questions.length === 0" class="no-questions card">
        <h2 class="h-royal">Aucune question disponible</h2>
        <p>Le quiz ne contient pas encore de questions.</p>
        <router-link to="/" class="btn btn--primary">Retour à l'accueil</router-link>
      </div>
      
      <div v-else class="quiz-container card">
        <div class="quiz-header">
          <h1 class="h-royal h-royal--gold">Quiz Royale</h1>
          <div class="progress">
            <div class="progress__bar" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          <div class="parchment">
            Question {{ currentQuestionIndex + 1 }} sur {{ questions.length }}
          </div>
        </div>
        
        <div class="question-container">
          <div class="question">
            <h2 class="h-royal">{{ currentQuestion.title }}</h2>
            <p v-if="currentQuestion.text" class="question-text">{{ currentQuestion.text }}</p>
            <img v-if="currentQuestion.image" :src="currentQuestion.image" :alt="currentQuestion.title" class="question-image">
          </div>
          
          <div class="list-answers">
            <div 
              v-for="(answer, index) in currentAnswers" 
              :key="answer.id || index"
              class="answer"
              :class="{ 'answer--correct': selectedAnswer === index }"
              @click="selectAnswer(index)"
            >
              <div class="answer__index">{{ index + 1 }}</div>
              {{ answer.text }}
            </div>
          </div>
          
          <div class="quiz-actions">
            <button 
              v-if="currentQuestionIndex > 0" 
              @click="previousQuestion" 
              class="btn btn--ghost"
            >
              Précédent
            </button>
            
            <button 
              v-if="currentQuestionIndex < questions.length - 1" 
              @click="nextQuestion" 
              class="btn btn--gold"
              :disabled="selectedAnswer === null"
            >
              Suivant
            </button>
            
            <button 
              v-else 
              @click="finishQuiz" 
              class="btn btn--gold"
              :disabled="selectedAnswer === null"
            >
              Terminer le Quiz
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BackgroundScene from '@/components/BackgroundScene.vue'

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
  position: relative;
  min-height: 100vh;
  padding: 2rem 0;
}

.loading, .error, .no-questions {
  text-align: center;
  padding: 3rem;
  z-index: 2;
  position: relative;
}

.error h2, .no-questions h2 {
  color: #e74c3c;
  margin-bottom: 1rem;
}

.quiz-container {
  z-index: 2;
  position: relative;
}

.quiz-header {
  background: linear-gradient(135deg, #2c3e50, #34495e);
  color: white;
  padding: 2rem;
  text-align: center;
  border-radius: 15px 15px 0 0;
}

.quiz-header h1 {
  margin: 0 0 1rem 0;
}

.question-container {
  padding: 2rem;
}

.question h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.question-text {
  color: #7f8c8d;
  margin-bottom: 1rem;
  line-height: 1.6;
  font-family: 'Cinzel', serif;
}

.question-image {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin: 1rem 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.quiz-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  gap: 1rem;
}

.quiz-actions .btn {
  flex: 1;
  max-width: 200px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
