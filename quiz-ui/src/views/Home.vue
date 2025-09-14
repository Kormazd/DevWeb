<template>
  <div class="home">
    <div class="hero">
      <h1>Quiz Application</h1>
      <p>Testez vos connaissances avec notre quiz interactif !</p>
      <div class="actions">
        <router-link to="/quiz" class="btn btn-primary">Commencer le Quiz</router-link>
        <router-link to="/admin" class="btn btn-secondary">Administration</router-link>
      </div>
    </div>
    
    <div class="quiz-info" v-if="quizInfo">
      <h2>Informations du Quiz</h2>
      <p>Nombre de questions : <strong>{{ quizInfo.size }}</strong></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const quizInfo = ref(null)

const fetchQuizInfo = async () => {
  try {
    const response = await fetch('http://localhost:5001/quiz-info')
    if (response.ok) {
      quizInfo.value = await response.json()
    }
  } catch (error) {
    console.error('Erreur lors du chargement des informations du quiz:', error)
  }
}

onMounted(() => {
  fetchQuizInfo()
})
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.hero {
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
  display: inline-block;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
  transform: translateY(-2px);
}

.quiz-info {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border-left: 4px solid #3498db;
}

.quiz-info h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.quiz-info p {
  color: #7f8c8d;
  font-size: 1.1rem;
}
</style>
