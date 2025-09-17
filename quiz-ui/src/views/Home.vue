<template>
  <div class="home">
    <BackgroundScene :questionIndex="0" />
    
    <div class="container">
      <div class="hero">
        <h1 class="h-royal h-royal--gold">Quiz Royale</h1>
        <p class="hero-subtitle">Testez vos connaissances sur Clash Royale et Clash of Clans !</p>
        <div class="actions">
          <router-link to="/quiz" class="btn btn--gold">Commencer le Quiz</router-link>
          <router-link to="/admin" class="btn btn--ghost">Administration</router-link>
        </div>
      </div>
      
      <div class="quiz-info card" v-if="quizInfo">
        <h2 class="h-royal">Informations du Quiz</h2>
        <div class="parchment">
          Nombre de questions : <strong>{{ quizInfo.size }}</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BackgroundScene from '@/components/BackgroundScene.vue'

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
</style>
