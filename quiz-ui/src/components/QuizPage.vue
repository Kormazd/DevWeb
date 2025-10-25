<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import QuizApi from '@/services/QuizApiService'
import Storage from '@/services/ParticipationStorageService'
import megaUrl from '@/assets/Mega_Knight_03.png'
import princeUrl from '@/assets/Prince_03.png'
import reineUrl from '@/assets/Reine_archer_pekka.png'

const router = useRouter()

const loading = ref(true)
const error = ref('')
const finished = ref(false)
const paused = ref(false)
const questions = ref([])
const currentIndex = ref(0)
const selectedIndex = ref(null)
const answersByQuestionId = ref({})
const score = ref(0)

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const total = computed(() => questions.value.length)

// Images latérales aléatoires (packagées par Vite)
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

// Conseils/astuces Supercell
const tips = [
  'Astuce Clash Royale: Gérez votre élixir, n’attaquez pas à sec !',
  'Astuce Clash Royale: Placez vos troupes derrière un tank pour maximiser les dégâts.',
  'Astuce Clash Royale: Conservez un sort pour contrer un push surprise.',
  'Astuce Clash of Clans: Lisez les pièges possibles avant d’attaquer (scout visuel).',
  'Astuce Clash of Clans: Utilisez les sorts de guérison pendant les gros combats.',
  'Astuce Clash of Clans: Diversifiez vos troupes pour contourner les défenses.',
]
const currentTip = ref('')
function pickTip() {
  currentTip.value = tips[Math.floor(Math.random() * tips.length)]
}

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
  Storage.saveScore(score.value)
  try {
    const playerName = Storage.getPlayerName()
    if (playerName) {
      await QuizApi.saveParticipation(playerName, answersByQuestionId.value)
      await QuizApi.postScore(playerName, score.value, total.value)
    }
  } catch (e) {
    /* non fatal */
  }
}

onMounted(async () => {
  // Guard: si pas de nom, retourne sur /new-quiz
  const name = Storage.getPlayerName()
  if (!name) {
    router.replace({ name: 'NewQuizPage' })
    return
  }
  await load()
  setRandomSides()
  pickTip()
})

watch(currentIndex, () => { setRandomSides(); pickTip() })

function togglePause() { paused.value = !paused.value }
function shareProgress() {
  const answered = currentIndex.value
  const acc = Math.round((score.value / Math.max(1, answered)) * 100)
  const text = `Mon quiz en cours: ${score.value}/${answered} corrects (précision ${acc}%).` 
  if (navigator.share) {
    navigator.share({ title: 'Mon progrès Quiz', text, url: location.href }).catch(() => {})
  } else if (navigator.clipboard) {
    navigator.clipboard.writeText(text).catch(() => {})
  }
}
</script>

<template>
  <section class="page">
    <template v-if="loading">
      <p class="loading-txt">Chargement…</p>
    </template>
    <template v-else-if="error">
      <p class="err">{{ error }}</p>
    </template>
    <template v-else>
      <div v-if="!finished" class="quiz">
        <div class="quiz-sides">
          <img v-if="leftSide" class="side-image left" :src="leftSide" alt="illustration gauche" />
          <div class="quiz-center">
            <div class="question-panel">
              <div class="panel-top">
                <button class="btn btn-small" @click="togglePause">{{ paused ? 'Reprendre' : 'Pause' }}</button>
                <button class="btn btn-small btn-secondary" @click="shareProgress">Partager</button>
              </div>
              <div class="meta">
                <span>Question {{ currentIndex + 1 }} / {{ total }}</span>
                <span>Score: {{ score }}</span>
              </div>
              <div v-if="currentQuestion" class="qc">
                <div class="qc__header">
                  <h2 class="qc__title">{{ currentQuestion.title }}</h2>
                  <p v-if="currentQuestion.text" class="qc__subtitle">{{ currentQuestion.text }}</p>
                  <img v-if="currentQuestion.image_url" :src="currentQuestion.image_url" :alt="currentQuestion.title" class="qc__image" />
                </div>
                <div class="qc__answers qc__answers--grid">
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
                <div class="actions">
                  <button class="btn" :disabled="selectedIndex === null || paused" @click="nextQuestion">
                    {{ currentIndex < total - 1 ? 'Suivant' : 'Terminer' }}
                  </button>
                </div>
              </div>
              <div class="tip" v-if="currentTip">💡 {{ currentTip }}</div>
              <div class="progress-area">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: ((currentIndex/Math.max(1,total))*100)+'%' }"></div>
                </div>
                <div class="legend">
                  <span>Correct: {{ score }}</span>
                  <span>Restant: {{ Math.max(0, total - (currentIndex+1)) }}</span>
                  <span>Précision: {{ Math.round((score/Math.max(1,currentIndex))*100) }}%</span>
                </div>
              </div>
              <div class="paused-overlay" v-if="paused">Pause</div>
            </div>
          </div>
          <img v-if="rightSide" class="side-image right" :src="rightSide" alt="illustration droite" />
        </div>
      </div>

      <div v-else class="result">
        <div class="question-panel">
          <h2>Terminé !</h2>
          <p>Score: <strong>{{ score }}</strong> / {{ total }}</p>
          <router-link class="btn" :to="{ name: 'HomePage' }">Retour accueil</router-link>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
.page { max-width: none; width: 100%; margin: 0; padding: 1.5rem 0; color: #fff; }
.loading-txt { text-align: center; opacity: 0.9; }
.err { color: #ffb3b3; text-align: center; }
.quiz, .result { background: rgba(0,0,0,0.0); }
.meta { display: flex; justify-content: space-between; margin-bottom: 0.75rem; }
.actions { margin-top: 1rem; }
.qc { display: grid; gap: 1.25rem; }
.qc__header { text-align: left; }
.qc__title { font-size: 1.75rem; margin: 0; color: #f5d36b; text-shadow: 0 1px 0 rgba(0,0,0,0.2); }
.qc__subtitle { color: #7f8c8d; margin: 0.25rem 0 0.5rem 0; line-height: 1.5; }
.qc__image { max-width: 100%; border-radius: 8px; margin-top: 0.5rem; box-shadow: 0 4px 8px rgba(0,0,0,0.08); }
.qc__answers { display: grid; gap: 0.75rem; }
.qc__answers--grid { grid-template-columns: 1fr; }
@media (min-width: 820px) { .qc__answers--grid { grid-template-columns: 1fr 1fr; gap: 1rem; } }
.qc__answer { display: flex; align-items: center; gap: 0.75rem; width: 100%; text-align: left; background: #fff; border: 1px solid #e6e8eb; border-radius: 10px; padding: 0.85rem 1rem; cursor: pointer; transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease; }
.qc__answer:hover { transform: translateY(-1px); box-shadow: 0 6px 12px rgba(0,0,0,0.06); }
.qc__answer--selected { border-color: #f1c40f; box-shadow: 0 0 0 3px rgba(241, 196, 15, 0.25); }
.qc__badge { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; background: #2c3e50; color: #fff; font-weight: 700; flex-shrink: 0; }
.qc__text { color: #2c3e50; }

/* Layout images latérales */
.quiz-sides { width: min(1900px, 98vw); margin: 0 auto; display: grid; grid-template-columns: minmax(260px, 1fr) minmax(860px, 1040px) minmax(260px, 1fr); align-items: start; column-gap: 1.5rem; }
.quiz-center { grid-column: 2; }
.question-panel { background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 1rem 1.25rem; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
.side-image { width: 100%; max-width: 600px; height: auto; object-fit: contain; filter: drop-shadow(0 12px 30px rgba(0,0,0,0.4)); opacity: 0.98; transition: transform .25s ease, opacity .25s ease; margin-top: 24px; }
.side-image.left { justify-self: end; }
.side-image.right { justify-self: start; }
.side-image:hover { transform: translateY(-4px) scale(1.02); opacity: 1; }
@media (max-width: 1000px) { .side-image { max-width: 360px; } }
@media (max-width: 880px) { .quiz-sides { grid-template-columns: 1fr; } .side-image { display: none; } }

.panel-top { display: flex; gap: 0.5rem; justify-content: flex-end; margin-bottom: 0.5rem; }
.btn-small { padding: 0.4rem 0.7rem; font-size: 0.9rem; }
.btn-secondary { background: linear-gradient(135deg, #3b82f6, #06b6d4); color: #fff; }

.tip { margin-top: 0.75rem; padding: 0.6rem 0.8rem; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; font-size: 0.95rem; }
.progress-area { margin-top: 0.75rem; }
.progress-bar { width: 100%; height: 10px; background: rgba(255,255,255,0.15); border-radius: 6px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #10B981, #3B82F6); transition: width .3s ease; }
.legend { display: flex; gap: 1rem; justify-content: space-between; font-size: 0.9rem; opacity: 0.95; margin-top: 0.4rem; }

.paused-overlay { position: absolute; inset: 0; display: grid; place-items: center; background: rgba(0,0,0,0.45); border-radius: 14px; font-size: 2rem; font-weight: 800; color: #fff; pointer-events: none; }
.question-panel { position: relative; }
</style>
