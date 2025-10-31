<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  total: { type: Number, required: true },
  correct: { type: Number, required: true },
  playVictory: { type: Boolean, default: false },
})

const router = useRouter()
const rate = computed(() => (props.total ? props.correct / props.total : 0))
const stars = computed(() => {
  const t = rate.value
  if (t < 0.33) return 0
  if (t < 0.66) return 1
  if (t < 0.9) return 2
  return 3
})

const show = ref(false)
onMounted(() => {
  // small delay to let animations feel snappier
  requestAnimationFrame(() => { show.value = true })
  // optional: light audio cue
  if (props.playVictory) {
    const audio = new Audio('/sounds/victory.mp3')
    audio.volume = 0.4
    audio.play().catch(() => {})
  }
})

function replay() {
  router.push('/new-quiz')
}

function home() {
  router.push('/')
}
</script>

<template>
  <section class="end-screen" :class="{ show }">
    <div class="bg-glow"></div>
    <div class="end-container">
      <h1 class="title">Résultat du Combat</h1>

      <div class="stars">
        <div
          v-for="i in 3"
          :key="i"
          class="star"
          :style="{ animationDelay: (i * 120) + 'ms' }"
          :class="{ active: i <= stars }"
        >
          ⭐
        </div>
      </div>
      <div class="stats">
        <p>Bonnes réponses : <strong>{{ correct }}</strong> / {{ total }}</p>
        <p>Fautes : <strong>{{ total - correct }}</strong></p>
        <p>Taux de réussite : <strong>{{ (rate * 100).toFixed(1) }}%</strong></p>
      </div>
      <div class="actions">
        <button class="btn btn-yellow" @click="replay">Rejouer</button>
        <button class="btn btn-outline" @click="home">Menu</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.end-screen {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem 1rem 8rem;
  background: radial-gradient(1200px 600px at 50% -10%, rgba(10, 22, 74, 0.9) 0%, rgba(7, 8, 25, 0.95) 60%, rgba(5, 6, 18, 1) 100%),
              linear-gradient(135deg, #0a0a1f 0%, #14265e 60%, #0a0a1f 100%);
  color: white;
  opacity: 0;
  animation: fadeIn 600ms ease forwards;
}

.end-screen .bg-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(circle at 50% 30%, rgba(0, 120, 255, 0.25), transparent 40%),
              radial-gradient(circle at 50% 70%, rgba(255, 208, 0, 0.22), transparent 50%);
  filter: blur(20px);
}

.end-container {
  position: relative;
  text-align: center;
  background: rgba(255,255,255,0.08);
  border: 3px solid #ffd400;
  border-radius: 20px;
  padding: 2rem 2.2rem;
  box-shadow: 0 0 40px rgba(255, 212, 0, 0.25), inset 0 0 20px rgba(255, 255, 255, 0.05);
  transform: scale(0.92) translateY(12px);
  animation: zoomIn 700ms cubic-bezier(.2,.8,.2,1) forwards;
}

.title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 1.25rem;
  text-shadow: 0 0 15px #ffd400, 0 0 40px rgba(255, 212, 0, 0.2);
}

.stars {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.star {
  font-size: 3rem;
  opacity: 0.2;
  transform: scale(0.7);
  transition: all 0.35s ease;
}

.star.active {
  opacity: 1;
  color: #ffd400;
  text-shadow: 0 0 20px #ffd400, 0 0 40px #ffb700, 0 0 60px rgba(255,183,0,0.5);
  transform: scale(1.25) rotate(-5deg);
  animation: starPop 520ms cubic-bezier(.2,.8,.2,1);
}

.stats {
  font-size: 1.15rem;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
}

.btn {
  padding: 0.65rem 1.2rem;
  border-radius: 10px;
  font-weight: 700;
  border: 2px solid #ffd400;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-yellow { background: #ffd400; color: #222; }
.btn-yellow:hover { background: #ffe750; }
.btn-outline { background: transparent; color: white; }
.btn-outline:hover { border-color: white; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes zoomIn { from { transform: scale(0.7) translateY(20px); opacity: 0; } to { transform: scale(1) translateY(0); opacity: 1; } }
@keyframes starPop {
  0% { transform: scale(0) rotate(0deg); opacity: 0; }
  80% { transform: scale(1.4) rotate(-15deg); opacity: 1; }
  100% { transform: scale(1.2) rotate(0deg); }
}

@media (max-width: 560px) {
  .end-container { padding: 1.25rem 1rem; border-width: 2px; }
  .title { font-size: 1.4rem; }
  .star { font-size: 2.2rem; }
  .stats { font-size: 1rem; }
}
</style>


