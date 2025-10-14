<script setup>
import { onMounted, ref } from 'vue'
import HeroBanner from './HeroBanner.vue'
import BackgroundScene from './BackgroundScene.vue'
import Storage from '@/services/ParticipationStorageService'

const topLocalScore = ref(0)
onMounted(() => {
  topLocalScore.value = Math.max(Number(Storage.getScore() || 0), 0)
})
</script>

<template>
  <section class="page">
    <BackgroundScene :question-index="0" />
    <HeroBanner />
    <div class="scores">
      <h2>Top scores</h2>
      <div class="score-item">
        <span>Meilleur score local</span>
        <strong>{{ topLocalScore }}</strong>
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


