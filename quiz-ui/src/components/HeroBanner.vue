<template>
  <section class="hero" data-parallax="true" @mousemove="onMove" @mouseleave="reset">
    <!-- Image layer -->
    <div class="hero__layer" :style="layerStyle"></div>
    <!-- Soft gradient overlay -->
    <div class="hero__layer hero__layer--gradient"></div>

    <div>
      <h1 class="hero__title">Quiz Royale</h1>
      <p class="hero__subtitle">Arènes, couronnes et gloire !</p>
      <div class="hero__badges">
        <span class="parchment">🛡️ Révision</span>
        <span class="parchment">👑 Classement</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'

/**
 * Images disponibles (déposées dans public/assets/characters)
 * - mega-knight.png
 * - prince.png
 */
const pool = [
  { cls:'bg-mega-knight', alt:'Mega Chevalier' },
  { cls:'bg-prince', alt:'Prince' },
]

const index = ref(0)
const rotMs = 6500
let timer

const layerStyle = computed(() => {
  const entry = pool[index.value]
  const bgUrl = bgFromClass(entry.cls)
  return {
    backgroundImage: bgUrl,
    backgroundSize: 'contain',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center bottom',
    opacity: '0.8'
  }
})
// Force l'application de l'image de fond
function applyBg(){
  const el = document.querySelector('.hero .hero__layer')
  if(!el) return
  const entry = pool[index.value]
  const bgUrl = bgFromClass(entry.cls)
  el.style.backgroundImage = bgUrl
  el.style.backgroundSize = 'contain'
  el.style.backgroundRepeat = 'no-repeat'
  el.style.backgroundPosition = 'center bottom'
  el.style.opacity = '0.8'
}
function bgFromClass(cls){
  if(cls==='bg-mega-knight') return "url('/assets/characters/mega-knight.png')"
  if(cls==='bg-prince') return "url('/assets/characters/prince.png')"
  return 'none'
}

function next(){ index.value = (index.value + 1) % pool.length; applyBg() }
function start(){ stop(); timer = setInterval(next, rotMs) }
function stop(){ if(timer) clearInterval(timer) }

const mx = ref(0), my = ref(0)
function onMove(e){
  const r = e.currentTarget.getBoundingClientRect()
  mx.value = ((e.clientX - r.left) / r.width - 0.5) * 2
  my.value = ((e.clientY - r.top) / r.height - 0.5) * 2
  const layer = e.currentTarget.querySelector('.hero__layer')
  if(layer){
    layer.style.transform = `translate3d(${mx.value*10}px, ${my.value* -6}px, 0) scale(1.03)`
  }
}
function reset(e){
  const layer = e.currentTarget.querySelector('.hero__layer')
  if(layer){ layer.style.transform = 'translate3d(0,0,0) scale(1.03)' }
}

onMounted(()=>{ applyBg(); start(); })
onBeforeUnmount(()=> stop())
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero__layer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.hero__layer--gradient {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
  z-index: 2;
}

.hero__title {
  font-family: 'Sigmar One', cursive;
  font-size: 4rem;
  color: #ffd700;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);
  margin-bottom: 1rem;
  position: relative;
  z-index: 3;
}

.hero__subtitle {
  font-family: 'Cinzel', serif;
  font-size: 1.5rem;
  color: #f8f9fa;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 3;
}

.hero__badges {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  position: relative;
  z-index: 3;
}

@media (max-width: 768px) {
  .hero__title {
    font-size: 2.5rem;
  }
  
  .hero__subtitle {
    font-size: 1.2rem;
  }
  
  .hero__badges {
    flex-direction: column;
    align-items: center;
  }
}
</style>
