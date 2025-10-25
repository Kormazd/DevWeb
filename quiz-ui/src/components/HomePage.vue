<script setup>
import { onMounted, ref } from 'vue'
import QuizApi from '@/services/QuizApiService'
import megaUrl from '@/assets/Mega_Knight_03.png'
import princeUrl from '@/assets/Prince_03.png'
import reineUrl from '@/assets/Reine_archer_pekka.png'

const quizSize = ref(null)
const loading = ref(true)
const leftImg = ref('')
const rightImg = ref('')

const assetFiles = [megaUrl, princeUrl, reineUrl]
function setRandomSides() {
  const pick = () => assetFiles[Math.floor(Math.random() * assetFiles.length)]
  let l = pick(); let r = pick(); let guard = 0
  while (r === l && guard < 5) { r = pick(); guard++ }
  leftImg.value = l
  rightImg.value = r
}

onMounted(async () => {
  const info = await QuizApi.getQuizInfo()
  quizSize.value = info?.data?.size ?? null
  loading.value = false
  setRandomSides()
})
</script>

<template>
  <section class="page">
    
    <div class="hero-sides">
      <img class="side-image left" :src="leftImg" alt="illustration gauche" />
      <div class="header">
      <h1>🏰 Quiz Clash Royale & Clash of Clans</h1>
      <p>Teste tes connaissances sur les jeux Supercell !</p>
      <div class="quiz-info" v-if="!loading && quizSize !== null">
        <p>📊 {{ quizSize }} questions t'attendent</p>
      </div>
      <router-link to="/new-quiz" class="btn-start">🎮 Commencer le quiz</router-link>
    </div>
      <img class="side-image right" :src="rightImg" alt="illustration droite" />
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
  max-width: none; 
  width: 100%; 
  margin: 0; 
  padding: 2rem 0; 
}

/* Images latérales accueil */
.hero-sides { width: min(1700px, 98vw); margin: 0 auto 2rem; display: grid; grid-template-columns: minmax(260px, 1fr) minmax(780px, 880px) minmax(260px, 1fr); column-gap: 2rem; align-items: start; }
.side-image { width: 100%; max-width: 560px; height: auto; object-fit: contain; filter: drop-shadow(0 12px 30px rgba(0,0,0,0.4)); opacity: 0.98; transition: transform .25s ease, opacity .25s ease; margin-top: 24px; }
.side-image.left { justify-self: end; margin-right: 0; }
.side-image.right { justify-self: start; margin-left: 0; }
.side-image:hover { transform: translateY(-4px) scale(1.02); opacity: 1; }
@media (max-width: 1000px) { .side-image { max-width: 360px; } }
@media (max-width: 860px) { .hero-sides { grid-template-columns: 1fr; } .side-image { display: none; } }

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
