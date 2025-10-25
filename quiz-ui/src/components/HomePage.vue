<script setup>
import { onMounted, ref } from 'vue'
import QuizApi from '@/services/QuizApiService'

const quizSize = ref(null)
const loading = ref(true)
const leftImg = ref('')
const rightImg = ref('')

// Prefer optimized assets when available, fallback to originals
const optimizedModules = import.meta.glob('@/assets-optimized/*.{webp}', { eager: true, import: 'default' })
const baseModules = import.meta.glob('@/assets/*.{png,jpg,jpeg,webp,svg}', { eager: true, import: 'default' })
const assetFiles = Object.values(Object.keys(optimizedModules).length ? optimizedModules : baseModules)
function setRandomSides() {
  if (!assetFiles || assetFiles.length === 0) return

  const lastLeft = localStorage.getItem('home_left_img')
  const lastRight = localStorage.getItem('home_right_img')

  let pool = assetFiles.filter(u => u !== lastLeft && u !== lastRight)
  if (pool.length < 2) {
    pool = [...assetFiles]
  }

  const randIndex = (max) => Math.floor(Math.random() * max)
  let l = pool[randIndex(pool.length)]

  let remaining = pool.filter(u => u !== l)
  if (remaining.length === 0) {
    remaining = assetFiles.filter(u => u !== l)
  }
  let r = remaining[randIndex(remaining.length)]

  leftImg.value = l
  rightImg.value = r
  localStorage.setItem('home_left_img', l)
  localStorage.setItem('home_right_img', r)
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
      <img class="side-image left" :src="leftImg" alt="illustration gauche" loading="lazy" decoding="async" fetchpriority="low"/>
      <div class="header">
      <h1>🏰 Quiz Clash Royale & Clash of Clans</h1>
      <p>Teste tes connaissances sur les jeux Supercell !</p>
      <div class="quiz-info" v-if="!loading && quizSize !== null">
        <p>📊 {{ quizSize }} questions t'attendent</p>
      </div>
      <router-link to="/new-quiz" class="btn-start">🎮 Commencer le quiz</router-link>
    </div>
      <img class="side-image right" :src="rightImg" alt="illustration droite" loading="lazy" decoding="async" fetchpriority="low"/>
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
.side-image { width: 100%; max-width: 560px; height: clamp(300px, 36vw, 520px); object-fit: contain; filter: drop-shadow(0 12px 30px rgba(0,0,0,0.4)); opacity: 0.98; transition: transform .25s ease, opacity .25s ease; margin-top: 24px; }
.side-image.left { justify-self: end; margin-right: 0; }
.side-image.right { justify-self: start; margin-left: 0; }
.side-image:hover { transform: translateY(-4px) scale(1.02); opacity: 1; }
@media (max-width: 1000px) { .side-image { max-width: 360px; height: clamp(220px, 40vw, 360px); } }
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
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 15px;
  font-family: var(--font-body);
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: var(--transition-medium);
  box-shadow: var(--shadow-button);
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--primary-purple), var(--primary-blue));
  color: var(--text-primary);
  text-decoration: none;
}

.btn-start::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: var(--transition-medium);
}

.btn-start:hover::before {
  left: 100%;
}

.btn-start:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
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
