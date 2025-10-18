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
  const [info, scores] = await Promise.all([
    QuizApi.getQuizInfo(),
    QuizApi.getScores(5),
  ])
  quizSize.value = info?.data?.size ?? null
  topScores.value = Array.isArray(scores?.data) ? scores.data : []
  loading.value = false
})
</script>

<template>
  <section class="page">
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
        <span>{{ s.player }}</span>
        <strong>{{ s.score }} / {{ s.total }}</strong>
      </div>
    </div>
  </section>
</template>

<style scoped>

.page { color: #fff; }
.scores { position: relative; z-index: 3; max-width: 960px; margin: 2rem auto; background: rgba(0,0,0,0.35); border-radius: 8px; padding: 1rem 1.25rem; }
.scores h2 { margin: 0 0 0.75rem; }
.score-item { display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 0; border-top: 1px solid rgba(255,255,255,0.15); }
.score-item:first-of-type { border-top: 0; }

h1 {
  margin-bottom: 0.5rem;
}

p {
  opacity: 0.9;
}
</style>


