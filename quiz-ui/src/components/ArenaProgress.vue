<template>
  <div class="arena-progress">
    <div class="arena-info">
      <h3 class="arena-name">{{ currentArenaName }}</h3>
      <div class="arena-level">Niveau {{ currentArena }}</div>
    </div>
    
    <div class="xp-container">
      <div class="xp-bar">
        <div 
          class="xp-fill" 
          :style="{ width: xpPercentage + '%' }"
          :class="xpBarClass"
        ></div>
      </div>
      <div class="xp-text">
        {{ xpCurrent }} / {{ xpNeeded }} XP
      </div>
    </div>
    
    <div class="progress-stats">
      <div class="stat">
        <span class="stat-value">{{ questionsAnswered }}</span>
        <span class="stat-label">Questions</span>
      </div>
      <div class="stat">
        <span class="stat-value">{{ correctAnswers }}</span>
        <span class="stat-label">Correctes</span>
      </div>
      <div class="stat">
        <span class="stat-value">{{ Math.round(accuracy) }}%</span>
        <span class="stat-label">Précision</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  questionsAnswered: { type: Number, default: 0 },
  correctAnswers: { type: Number, default: 0 }
})

const arenas = [
  { name: "Camp d'entraînement", level: 1, xpNeeded: 0 },
  { name: "Arène Gobeline", level: 2, xpNeeded: 2 },
  { name: "Arène des Squelettes", level: 3, xpNeeded: 4 },
  { name: "Arène des Barbares", level: 4, xpNeeded: 6 },
  { name: "Arène de P.E.K.K.A", level: 5, xpNeeded: 8 },
  { name: "Arène des Sorciers", level: 6, xpNeeded: 10 },
  { name: "Arène Royale", level: 7, xpNeeded: 12 },
  { name: "Arène des Glaces", level: 8, xpNeeded: 14 },
  { name: "Arène Légendaire", level: 9, xpNeeded: 16 },
  { name: "Arène Champion", level: 10, xpNeeded: 18 }
]

const currentArena = computed(() => {
  const xp = props.correctAnswers
  for (let i = arenas.length - 1; i >= 0; i--) {
    if (xp >= arenas[i].xpNeeded) {
      return arenas[i].level
    }
  }
  return 1
})

const currentArenaName = computed(() => {
  const arena = arenas.find(a => a.level === currentArena.value)
  return arena ? arena.name : "Camp d'entraînement"
})

const xpCurrent = computed(() => props.correctAnswers)

const xpNeeded = computed(() => {
  const currentArenaData = arenas.find(a => a.level === currentArena.value)
  const nextArenaData = arenas.find(a => a.level === currentArena.value + 1)
  
  if (!nextArenaData) {
    return currentArenaData.xpNeeded // Dernière arène
  }
  
  return nextArenaData.xpNeeded
})

const xpPercentage = computed(() => {
  const currentArenaData = arenas.find(a => a.level === currentArena.value)
  const nextArenaData = arenas.find(a => a.level === currentArena.value + 1)
  
  if (!nextArenaData) {
    return 100 // Dernière arène
  }
  
  const currentXP = props.correctAnswers - currentArenaData.xpNeeded
  const neededXP = nextArenaData.xpNeeded - currentArenaData.xpNeeded
  
  return Math.min(100, Math.max(0, (currentXP / neededXP) * 100))
})

const xpBarClass = computed(() => {
  if (xpPercentage.value >= 80) return 'xp-high'
  if (xpPercentage.value >= 50) return 'xp-medium'
  return 'xp-low'
})

const accuracy = computed(() => {
  if (props.questionsAnswered === 0) return 0
  return (props.correctAnswers / props.questionsAnswered) * 100
})
</script>

<style scoped>
.arena-progress {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #ffd700;
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.arena-info {
  text-align: center;
  margin-bottom: 20px;
}

.arena-name {
  font-family: 'Sigmar One', cursive;
  font-size: 1.8rem;
  color: #ffd700;
  margin: 0 0 5px 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.arena-level {
  font-size: 1.1rem;
  color: #fff;
  font-weight: bold;
}

.xp-container {
  margin-bottom: 20px;
}

.xp-bar {
  width: 100%;
  height: 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.3);
  position: relative;
}

.xp-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6b6b, #ffd700, #4ecdc4);
  border-radius: 8px;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  animation: xpGlow 2s ease-in-out infinite alternate;
}

.xp-fill::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: xpShine 2s ease-in-out infinite;
}

@keyframes xpGlow {
  0% { box-shadow: 0 0 5px rgba(255, 107, 107, 0.3); }
  100% { box-shadow: 0 0 15px rgba(255, 107, 107, 0.6); }
}

@keyframes xpShine {
  0% { left: -100%; }
  100% { left: 100%; }
}

.xp-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shimmer 2s infinite;
}

.xp-fill.xp-high {
  background: linear-gradient(90deg, #4ecdc4, #45b7d1, #96ceb4);
}

.xp-fill.xp-medium {
  background: linear-gradient(90deg, #ffd700, #ffed4e, #f39c12);
}

.xp-fill.xp-low {
  background: linear-gradient(90deg, #ff6b6b, #ff8e8e, #ffa8a8);
}

.xp-text {
  text-align: center;
  margin-top: 8px;
  font-weight: bold;
  color: #fff;
  font-size: 0.9rem;
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.stat {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffd700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.8rem;
  color: #ccc;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

@media (max-width: 768px) {
  .arena-progress {
    padding: 15px;
    margin: 15px 0;
  }
  
  .arena-name {
    font-size: 1.5rem;
  }
  
  .progress-stats {
    gap: 10px;
  }
  
  .stat {
    padding: 8px;
  }
  
  .stat-value {
    font-size: 1.2rem;
  }
}
</style>