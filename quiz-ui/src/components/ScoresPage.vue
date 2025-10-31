<script setup>
import { onMounted, ref } from 'vue'
import Storage from '@/services/ParticipationStorageService'
import QuizApi from '@/services/QuizApiService'
import { pickTwoRandom } from '@/data/sideImages'

const topLocalScore = ref(0)
const quizSize = ref(null)
const topScores = ref([])
const loading = ref(true)

const leftSide = ref('')
const rightSide = ref('')
function setRandomSides() {
  const [l, r] = pickTwoRandom(leftSide.value, rightSide.value)
  leftSide.value = l
  rightSide.value = r
}

onMounted(async () => {
  topLocalScore.value = Math.max(Number(Storage.getScore() || 0), 0)
  
  // Un seul appel API au lieu de deux
  const info = await QuizApi.getQuizInfo()
  quizSize.value = info?.data?.size ?? null
  topScores.value = Array.isArray(info?.data?.scores) ? info.data.scores : []
  loading.value = false
  setRandomSides()
})
</script>

<template>
  <section class="page">
    <div class="hero-sides">
      <img v-if="leftSide" class="side-image left" :src="leftSide" alt="illustration gauche" />
      <div class="scores-center">
        <div class="header">
          <h1>Classements</h1>
          <p>Découvre les meilleurs scores des joueurs !</p>
        </div>

        <!-- Bloc séparé: Nombre de questions -->
        <div class="quiz-info" v-if="!loading && quizSize !== null">
          <span class="quiz-info__label">Nombre de questions</span>
          <strong class="quiz-info__value">{{ quizSize }}</strong>
        </div>

        <!-- Bloc séparé: Meilleur score local -->
        <div class="my-score" v-if="!loading">
          <span class="my-score__label">Ton meilleur score local</span>
          <strong class="my-score__value">{{ topLocalScore }}</strong>
        </div>

        <div class="scores" v-if="!loading">
          <h2>Top scores</h2>

          <div class="score-item" v-for="(s, idx) in topScores" :key="idx" :class="{ 'top-score': idx === 0 }">
            <span>
              #{{ idx + 1 }} {{ s.playerName }}
            </span>
            <strong>{{ s.score }}</strong>
          </div>
          <div v-if="topScores.length === 0" class="no-scores">
            <p>Aucun score enregistré pour le moment. Sois le premier !</p>
          </div>
        </div>

        <div v-else class="loading">
          <p>Chargement des scores...</p>
        </div>
      </div>
      <img v-if="rightSide" class="side-image right" :src="rightSide" alt="illustration droite" />
    </div>
  </section>
</template>

<style scoped>
.page { color: #fff; max-width: none; width: 100%; margin: 0; padding: 2rem 0; }

/* Héro + images latérales */
.hero-sides { width: min(1800px, 98vw); margin: 0 auto; display: grid; grid-template-columns: minmax(240px, 1fr) minmax(760px, 920px) minmax(240px, 1fr); column-gap: 2rem; align-items: start; }
.scores-center { grid-column: 2; display: grid; gap: 1rem; }
.side-image { width: 100%; max-width: 520px; height: auto; object-fit: contain; filter: drop-shadow(0 12px 30px rgba(0,0,0,0.4)); opacity: 0.98; transition: transform .25s ease, opacity .25s ease; margin-top: 24px; }
.side-image.left { justify-self: end; }
.side-image.right { justify-self: start; }
.side-image:hover { transform: translateY(-4px) scale(1.02); opacity: 1; }
@media (max-width: 1000px) { .side-image { max-width: 340px; } }
@media (max-width: 860px) { .hero-sides { grid-template-columns: 1fr; } .side-image { display: none; } }

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
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.scores { position: relative; z-index: 3; background: rgba(0,0,0,0.35); border-radius: 8px; padding: 1rem 1.25rem; }

.scores h2 { 
  margin: 0 0 0.75rem; 
  color: #d4af37;
  text-align: center;
}

/* Bloc séparé: Nombre de questions */
.quiz-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.quiz-info__label { 
  opacity: 0.95; 
  font-size: 1.05rem;
}
.quiz-info__value { 
  color: #d4af37; 
  font-size: 1.5rem;
}

/* Bloc séparé: Ton meilleur score local */
.my-score {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.my-score__label { 
  opacity: 0.95; 
  font-size: 1.05rem;
  color: #fff;
}
.my-score__value { 
  color: #d4af37; 
  font-size: 1.5rem;
}

.score-item { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 0.75rem; 
  margin: 0 -0.75rem;
  border-top: 1px solid rgba(255,255,255,0.15); 
  border-radius: 6px;
  transition: all 0.2s ease;
}

.score-item:first-of-type { 
  border-top: 0; 
}

.score-item:hover {
  background-color: rgba(255,255,255,0.05);
}

.top-score {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(241, 196, 15, 0.15)) !important;
  border: 2px solid rgba(212, 175, 55, 0.4) !important;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
  position: relative;
}

.top-score::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(241, 196, 15, 0.1));
  border-radius: 6px;
  z-index: -1;
}

.top-score span,
.top-score strong {
  color: #f5d36b;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.top-score strong {
  background: linear-gradient(135deg, #f5d36b, #d4af37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.4em;
}

.top-score:hover {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.25), rgba(241, 196, 15, 0.25)) !important;
  border-color: rgba(212, 175, 55, 0.6) !important;
  box-shadow: 0 6px 16px rgba(212, 175, 55, 0.4);
  transform: translateY(-2px);
}

.no-scores {
  text-align: center;
  padding: 2rem;
  opacity: 0.8;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #d4af37;
}

/* Responsive ScoresPage */
@media (max-width: 1024px) {
  .hero-sides {
    grid-template-columns: minmax(180px, 0.8fr) 1fr minmax(180px, 0.8fr);
    column-gap: 1rem;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .header p {
    font-size: 1rem;
  }
}

@media (max-width: 860px) {
  .page {
    padding: 1rem 0;
  }
  
  .hero-sides {
    grid-template-columns: 1fr;
    padding: 0 1rem;
  }
  
  .side-image {
    display: none;
  }
  
  .header {
    padding: 1.5rem 1rem;
    margin-bottom: 1.5rem;
  }
  
  .header h1 {
    font-size: 1.8rem;
  }
  
  .scores {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.5rem;
  }
  
  .header p {
    font-size: 0.95rem;
  }
  
  .score-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
    padding: 0.6rem 0;
  }
  
  .score-item strong {
    font-size: 1.2rem;
  }
}
</style>
