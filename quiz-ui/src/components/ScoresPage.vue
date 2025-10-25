<script setup>
import { onMounted, ref } from 'vue'
import Storage from '@/services/ParticipationStorageService'
import QuizApi from '@/services/QuizApiService'
import megaUrl from '@/assets/Mega_Knight_03.png'
import princeUrl from '@/assets/Prince_03.png'
import reineUrl from '@/assets/Reine_archer_pekka.png'

const topLocalScore = ref(0)
const quizSize = ref(null)
const topScores = ref([])
const loading = ref(true)

// Images latérales aléatoires
const assetFiles = [megaUrl, princeUrl, reineUrl]
const leftSide = ref('')
const rightSide = ref('')
function setRandomSides() {
  if (!assetFiles.length) return
  const pick = () => assetFiles[Math.floor(Math.random() * assetFiles.length)]
  let l = pick(); let r = pick(); let guard = 0
  while (r === l && guard < 5) { r = pick(); guard++ }
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
          <h1>🏆 Classements</h1>
          <p>Découvre les meilleurs scores des joueurs !</p>
        </div>

        <div class="scores" v-if="!loading">
          <h2>Top scores</h2>
          <div class="score-item local-score">
            <span>🛡️ Ton meilleur score local</span>
            <strong>{{ topLocalScore }}</strong>
          </div>
          <div class="score-item" v-if="quizSize !== null">
            <span>📚 Nombre de questions</span>
            <strong>{{ quizSize }}</strong>
          </div>
          <div class="score-item" v-for="(s, idx) in topScores" :key="idx" :class="{ 'top-score': idx === 0 }">
            <span>
              <span v-if="idx === 0">👑</span>
              <span v-else-if="idx === 1">🥈</span>
              <span v-else-if="idx === 2">🥉</span>
              <span v-else>#{{ idx + 1 }}</span>
              {{ s.playerName }}
            </span>
            <strong>{{ s.score }} / {{ s.total }}</strong>
          </div>
          <div v-if="topScores.length === 0" class="no-scores">
            <p>💬 Aucun score enregistré pour le moment. Sois le premier !</p>
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

.score-item { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 0.75rem 0; 
  border-top: 1px solid rgba(255,255,255,0.15); 
  transition: background-color 0.2s ease;
}

.score-item:first-of-type { 
  border-top: 0; 
}

.score-item:hover {
  background-color: rgba(255,255,255,0.05);
}

.local-score {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), rgba(241, 196, 15, 0.1));
  border-radius: 6px;
  margin-bottom: 0.5rem;
  padding: 0.75rem 1rem;
}

.top-score {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 193, 7, 0.1));
  border-radius: 6px;
  margin-bottom: 0.5rem;
  padding: 0.75rem 1rem;
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
</style>
