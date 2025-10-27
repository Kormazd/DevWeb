<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Storage from '@/services/ParticipationStorageService'
import megaUrl from '@/assets/Mega_Knight_03.png'
import princeUrl from '@/assets/Prince_03.png'
import reineUrl from '@/assets/Reine_archer_pekka.png'

const router = useRouter()
const playerName = ref('')


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

function startQuiz() {
  const name = (playerName.value || '').trim()
  if (!name) return
  Storage.savePlayerName(name)
  router.push({ name: 'QuizPage' })
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
  setRandomSides()
})
</script>

<template>
  <section class="page">
    <h1 class="page-title">Nouveau quiz</h1>
    <div class="quiz-sides quiz-sides--start">
      <img v-if="leftSide" class="side-image left" :src="leftSide" alt="illustration gauche" />
      <div class="quiz-center">
        <div class="start-box">
          <label for="player">Nom du joueur</label>
          <input id="player" v-model="playerName" placeholder="Ton nom" />
          <button class="btn" :disabled="!playerName" @click="startQuiz">Commencer</button>
        </div>
      </div>
      <img v-if="rightSide" class="side-image right" :src="rightSide" alt="illustration droite" />
    </div>
  </section>
</template>

<style scoped>
.page { max-width: none; width: 100%; margin: 0; padding: 1.5rem 0; color: #fff; }
.page-title { text-align: center; margin: 0 0 0.5rem 0; font-size: 2.4rem; color: #f5d36b; text-shadow: 0 1px 0 rgba(0,0,0,0.2); }
.err { color: #ffb3b3; }
.start, .quiz, .result { background: rgba(0,0,0,0.35); padding: 1rem 1.25rem; border-radius: 8px; }
/* Boîte de démarrage centrée et dominante */
.start-box { display: grid; gap: 0.75rem; padding: 1.25rem 1.5rem; border-radius: 12px; background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 8px 24px rgba(0,0,0,0.25); max-width: 520px; margin: 0 auto; }
label { font-weight: 600; }
input { padding: 0.6rem 0.75rem; border-radius: 6px; border: 1px solid rgba(255,255,255,0.35); background: rgba(255,255,255,0.9); color: #222; }
.btn { padding: 0.6rem 0.9rem; border: none; border-radius: 6px; background: #d4af37; color: #222; font-weight: 700; cursor: pointer; }
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

/* Images latérales quiz */
.quiz-sides { width: min(1900px, 98vw); margin: 0 auto; display: grid; grid-template-columns: minmax(260px, 1fr) minmax(820px, 980px) minmax(260px, 1fr); align-items: start; column-gap: 2rem; }
.quiz-center { grid-column: 2; }
.question-panel { background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 1rem 1.25rem; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
.side-image { width: 100%; max-width: 560px; height: auto; object-fit: contain; filter: drop-shadow(0 12px 30px rgba(0,0,0,0.4)); opacity: 0.98; transition: transform .25s ease, opacity .25s ease; margin-top: 24px; }
.side-image.left { justify-self: end; margin-right: 0; }
.side-image.right { justify-self: start; margin-left: 0; }
.side-image:hover { transform: translateY(-4px) scale(1.02); opacity: 1; }
@media (max-width: 1000px) { .side-image { max-width: 360px; } }
@media (max-width: 880px) { .quiz-sides { grid-template-columns: 1fr; } .side-image { display: none; } }

/* Variante écran de démarrage: contenu dominant, images plus contenues */
.quiz-sides--start { grid-template-columns: minmax(200px, 1fr) minmax(980px, 1120px) minmax(200px, 1fr); }
.quiz-sides--start .side-image { max-width: 380px; margin-top: 8px; }
.quiz-sides--start .start-box { margin: 0 auto; }
</style>
