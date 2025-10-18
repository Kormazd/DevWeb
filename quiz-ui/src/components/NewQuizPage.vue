<script setup>
import { computed, onMounted, ref } from 'vue'
import QuizApi from '@/services/QuizApiService'
import Storage from '@/services/ParticipationStorageService'

const loading = ref(true)
const error = ref('')
const started = ref(false)
const finished = ref(false)
const playerName = ref('')

const questions = ref([])
const currentIndex = ref(0)
const selectedIndex = ref(null)
const answersByQuestionId = ref({})
const score = ref(0)

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const total = computed(() => questions.value.length)

async function load() {
  loading.value = true
  error.value = ''
  const { status, data } = await QuizApi.getQuestions()
  if (status >= 200 && status < 300 && Array.isArray(data)) {
    questions.value = data
  } else {
    error.value = data?.error || 'Impossible de charger les questions'
  }
  loading.value = false
}

function startQuiz() {
  if (!playerName.value.trim()) {
    error.value = 'Entre un nom de joueur'
    return
  }
  Storage.savePlayerName(playerName.value.trim())
  started.value = true
  currentIndex.value = 0
  selectedIndex.value = null
  score.value = 0
}

async function nextQuestion() {
  if (selectedIndex.value == null) return
  const q = currentQuestion.value
  const selected = q?.answers?.[selectedIndex.value]
  const isCorrect = Boolean(selected?.isCorrect)
  if (isCorrect) score.value += 1

  answersByQuestionId.value[q.id] = { selectedIndex: selectedIndex.value }
  selectedIndex.value = null

  if (currentIndex.value < total.value - 1) {
    currentIndex.value += 1
  } else {
    await finishQuiz()
  }
}

async function finishQuiz() {
  finished.value = true
  started.value = false
  Storage.saveScore(score.value)
  try {
    if (playerName.value) {
      await QuizApi.saveParticipation(playerName.value, answersByQuestionId.value)
      await QuizApi.postScore(playerName.value, score.value, total.value)
    }
  } catch (e) {
    /* network errors are non-fatal for UX here */
  }
}

onMounted(() => {
  playerName.value = Storage.getPlayerName()
  load()
})
</script>

<template>
  <section class="page">
    <h1>Nouveau quiz</h1>

    <p v-if="loading">Chargement…</p>
    <p v-else-if="error" class="err">{{ error }}</p>

    <template v-else>
      <!-- Start screen -->
      <div v-if="!started && !finished" class="start">
        <label for="player">Nom du joueur</label>
        <input id="player" v-model="playerName" placeholder="Ton nom" />
        <button class="btn" :disabled="!questions.length" @click="startQuiz">Commencer</button>
      </div>

      <!-- Quiz screen -->
      <div v-if="started" class="quiz">
        <div class="meta">
          <span>Question {{ currentIndex + 1 }} / {{ total }}</span>
          <span>Score: {{ score }}</span>
        </div>
        <div v-if="currentQuestion" class="qc">
          <div class="qc__header">
            <h2 class="h-royal">{{ currentQuestion.title }}</h2>
            <p v-if="currentQuestion.text" class="qc__subtitle">{{ currentQuestion.text }}</p>
            <img v-if="currentQuestion.image_url" :src="currentQuestion.image_url" :alt="currentQuestion.title" class="qc__image" />
          </div>
          <div class="qc__answers">
            <button
              v-for="(a, idx) in currentQuestion.answers || []"
              :key="a.id || idx"
              class="qc__answer"
              :class="{ 'qc__answer--selected': selectedIndex === idx }"
              type="button"
              @click="selectedIndex = idx"
            >
              <span class="qc__badge">{{ idx + 1 }}</span>
              <span class="qc__text">{{ a.text }}</span>
            </button>
          </div>
        </div>
        <div class="actions">
          <button class="btn" :disabled="selectedIndex === null" @click="nextQuestion">
            {{ currentIndex < total - 1 ? 'Suivant' : 'Terminer' }}
          </button>
        </div>
      </div>

      <!-- Result screen -->
      <div v-if="finished" class="result">
        <h2>Terminé !</h2>
        <p>Score: <strong>{{ score }}</strong> / {{ total }}</p>
        <button class="btn" @click="started = false; finished = false; score = 0; answersByQuestionId = {}; selectedIndex = null; currentIndex = 0">Rejouer</button>
      </div>
    </template>
  </section>
</template>

<style scoped>
.page {
  max-width: 960px;
  margin: 0 auto;
  padding: 1rem 2rem;
  color: #fff;
}
.err { color: #ffb3b3; }
.start, .quiz, .result { background: rgba(0,0,0,0.35); padding: 1rem 1.25rem; border-radius: 8px; }
.start { display: grid; gap: 0.75rem; max-width: 480px; }
label { font-weight: 600; }
input { padding: 0.6rem 0.75rem; border-radius: 6px; border: 1px solid rgba(255,255,255,0.35); background: rgba(255,255,255,0.9); color: #222; }
.btn { padding: 0.6rem 0.9rem; border: none; border-radius: 6px; background: #d4af37; color: #222; font-weight: 700; cursor: pointer; }
.meta { display: flex; justify-content: space-between; margin-bottom: 0.75rem; }
.actions { margin-top: 1rem; }
.qc { display: grid; gap: 1.25rem; }
.qc__header { text-align: left; }
.qc__subtitle { color: #7f8c8d; margin: 0.25rem 0 0.5rem 0; line-height: 1.5; }
.qc__image { max-width: 100%; border-radius: 8px; margin-top: 0.5rem; box-shadow: 0 4px 8px rgba(0,0,0,0.08); }
.qc__answers { display: grid; gap: 0.75rem; }
.qc__answer { display: flex; align-items: center; gap: 0.75rem; width: 100%; text-align: left; background: #fff; border: 1px solid #e6e8eb; border-radius: 10px; padding: 0.85rem 1rem; cursor: pointer; transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease; }
.qc__answer:hover { transform: translateY(-1px); box-shadow: 0 6px 12px rgba(0,0,0,0.06); }
.qc__answer--selected { border-color: #f1c40f; box-shadow: 0 0 0 3px rgba(241, 196, 15, 0.25); }
.qc__badge { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; background: #2c3e50; color: #fff; font-weight: 700; flex-shrink: 0; }
.qc__text { color: #2c3e50; }
</style>


