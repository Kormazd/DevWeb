<template>
  <div class="home">
    <BackgroundScene :questionIndex="0" />
    
    <div class="container">
      <div class="hero">
        <h1 class="h-royal h-royal--gold">Quiz Royale</h1>
        <p class="hero-subtitle">Testez vos connaissances sur Clash Royale et Clash of Clans !</p>
        <div class="actions">
          <router-link to="/quiz" class="btn btn--gold">Lancer le Quiz</router-link>
          <router-link to="/admin" class="btn btn--ghost">Administration</router-link>
        </div>
      </div>
      
      <div class="leaderboard card" v-if="scores.length">
        <h2 class="h-royal">Meilleurs Scores</h2>
        <ol class="scores-list">
          <li v-for="s in scores" :key="s.id" class="score-item">
            <span class="player">{{ s.player }}</span>
            <span class="dots" />
            <span class="value">{{ s.score }} / {{ s.total }}</span>
          </li>
        </ol>
      </div>

      <div class="quiz-info card" v-if="quizInfo">
        <h2 class="h-royal">Informations du Quiz</h2>
        <div class="parchment">
          Nombre de questions : <strong>{{ quizInfo.size }}</strong>
        </div>
      </div>

      <div class="questions-preview card" v-if="questions.length">
        <h2 class="h-royal">Aperçu des questions</h2>
        <ul class="preview-list">
          <li v-for="q in questions.slice(0, 5)" :key="q.id" class="preview-item">
            <span class="preview-position">#{{ q.position }}</span>
            <span class="preview-title">{{ q.title }}</span>
          </li>
        </ul>
        <router-link to="/quiz" class="btn btn--gold btn--sm">Voir tout le quiz</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BackgroundScene from '@/components/BackgroundScene.vue'

const quizInfo = ref(null)
const questions = ref([])
const scores = ref([])

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

const fetchQuestions = async () => {
  try {
    const response = await fetch('http://localhost:5001/questions')
    if (response.ok) {
      questions.value = await response.json()
    }
  } catch (error) {
    console.error('Erreur lors du chargement des questions:', error)
  }
}

const fetchScores = async () => {
  try {
    const response = await fetch('http://localhost:5001/scores?limit=10')
    if (response.ok) {
      scores.value = await response.json()
    }
  } catch (error) {
    console.error('Erreur lors du chargement des scores:', error)
  }
}

onMounted(() => {
  fetchQuizInfo()
  fetchQuestions()
  fetchScores()
})
</script>

<style scoped>
.home {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero {
  margin-bottom: 3rem;
  z-index: 2;
  position: relative;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: #ecf0f1;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  font-family: 'Cinzel', serif;
}

.actions {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.quiz-info {
  margin-top: 2rem;
  z-index: 2;
  position: relative;
}

.quiz-info .h-royal {
  color: #d4af37;
  margin-bottom: 1rem;
}

.questions-preview {
  margin-top: 1.5rem;
}

.leaderboard {
  margin-top: 1.5rem;
}

.scores-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.score-item {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.score-item .player {
  font-weight: 700;
  color: #ecf0f1;
}

.score-item .value {
  color: #d4af37;
}

.preview-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.preview-position {
  font-weight: 700;
  color: #d4af37;
}

.preview-title {
  color: #ecf0f1;
}

.btn--sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}
</style>
