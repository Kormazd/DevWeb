<script setup>
import { onMounted, ref } from 'vue'
import QuizApi from '@/services/QuizApiService'

const quizSize = ref(null)
const loading = ref(true)

onMounted(async () => {
  const info = await QuizApi.getQuizInfo()
  quizSize.value = info?.data?.size ?? null
  loading.value = false
})
</script>

<template>
  <section class="page">
    <div class="header">
      <h1>🏰 Quiz Clash Royale & Clash of Clans</h1>
      <p>Teste tes connaissances sur les jeux Supercell !</p>
      <div class="quiz-info" v-if="!loading && quizSize !== null">
        <p>📊 {{ quizSize }} questions t'attendent</p>
      </div>
      <router-link to="/new-quiz" class="btn-start">🎮 Commencer le quiz</router-link>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <h3>🎯 Questions variées</h3>
        <p>Clash Royale et Clash of Clans</p>
      </div>
      <div class="feature-card">
        <h3>🏆 Classements</h3>
        <p>Compare tes scores avec les autres</p>
      </div>
      <div class="feature-card">
        <h3>🎨 Design immersif</h3>
        <p>Interface médiévale et animations</p>
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
  margin-bottom: 3rem;
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
  margin: 0 0 1rem;
  opacity: 0.9;
  font-size: 1.1rem;
}

.quiz-info {
  margin: 1rem 0;
  padding: 0.75rem 1rem;
  background: rgba(212, 175, 55, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(212, 175, 55, 0.3);
}

.quiz-info p {
  margin: 0;
  color: #d4af37;
  font-weight: 600;
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

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.feature-card {
  background: rgba(0,0,0,0.35);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.feature-card h3 {
  margin: 0 0 0.5rem;
  color: #d4af37;
  font-size: 1.2rem;
}

.feature-card p {
  margin: 0;
  opacity: 0.9;
  font-size: 0.95rem;
}
</style>


