<script setup>
import { onMounted, ref } from 'vue'
import Storage from '@/services/ParticipationStorageService'
import QuizApi from '@/services/QuizApiService'

const topLocalScore = ref(0)
const quizSize = ref(null)
const topScores = ref([])
const loading = ref(true)

onMounted(async () => {
  topLocalScore.value = Math.max(Number(Storage.getScore() || 0), 0)
  
  // Un seul appel API au lieu de deux
  const info = await QuizApi.getQuizInfo()
  quizSize.value = info?.data?.size ?? null
  topScores.value = Array.isArray(info?.data?.scores) ? info.data.scores : []
  loading.value = false
})
</script>

<template>
  <section class="page">
    <div class="header">
      <h1>🏰 Quiz Clash Royale & Clash of Clans</h1>
      <p>Teste tes connaissances sur les jeux Supercell !</p>
      <router-link to="/new-quiz" class="btn-start">🎮 Commencer le quiz</router-link>
    </div>
    
    <div class="scores">
      <h2>Top scores</h2>
      <div class="score-item">
        <span>Meilleur score local</span>
        <strong>{{ topLocalScore }}</strong>
      </div>
      <div class="score-item" v-if="quizSize !== null">
        <span>Nombre de questions</span>
        <strong>{{ quizSize }}</strong>
      </div>
      <div class="score-item" v-for="(s, idx) in topScores" :key="idx">
        <span>{{ s.playerName }}</span>
        <strong>{{ s.score }} / {{ s.total }}</strong>
      </div>
    </div>
  </section>
</template>

<style scoped>
.page { 
  color: #fff; 
  max-width: 960px; 
  margin: 0 auto; 
  padding: 2rem 1rem; 
}

.header {
  text-align: center;
  margin-bottom: 2rem;
  background: rgba(0,0,0,0.35);
  border-radius: 8px;
  padding: 2rem 1.5rem;
}

.header h1 {
  margin: 0 0 0.5rem;
  font-size: 2.5rem;
  color: #d4af37;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.header p {
  margin: 0 0 1.5rem;
  opacity: 0.9;
  font-size: 1.1rem;
}

.btn-start {
  display: inline-block;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  color: #222;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-start:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

.scores { 
  position: relative; 
  z-index: 3; 
  background: rgba(0,0,0,0.35); 
  border-radius: 8px; 
  padding: 1rem 1.25rem; 
}

.scores h2 { 
  margin: 0 0 0.75rem; 
  color: #d4af37;
}

.score-item { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 0.5rem 0; 
  border-top: 1px solid rgba(255,255,255,0.15); 
}

.score-item:first-of-type { 
  border-top: 0; 
}
</style>


