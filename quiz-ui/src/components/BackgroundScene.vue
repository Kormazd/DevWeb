<template>
  <div class="bg-scene" data-parallax="true" @mousemove="onMove" @mouseleave="reset">
    <!-- Deux couches pour crossfade -->
    <div
      ref="layerA"
      class="bg-scene__layer"
      :class="activeLayer === 'A' ? 'is-active' : ''"
      :style="{'background-image': `url('${activeUrl}')`}"
      aria-hidden="true"
    />
    <div
      ref="layerB"
      class="bg-scene__layer"
      :class="activeLayer === 'B' ? 'is-active' : ''"
      :style="{'background-image': `url('${nextUrl}')`}"
      aria-hidden="true"
    />
    <div class="bg-scene__glow" aria-hidden="true"/>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { questionCharacterMapping } from '@/data/characters'

/**
 * Props :
 * - questionIndex (Number): index/ID courant de la question (0,1,2,...)
 * - mapping (Array<String> | Function): mappage index -> nom d'image (sans path)
 * 
 * Convention de noms attendue dans /public/images/ :
 *   mega-knight.png, prince.png, dark-prince.png, golem.png
 */
const props = defineProps({
  questionIndex: { type: Number, required: true },
  mapping: { type: [Array, Function], default: questionCharacterMapping }
})

// URLs calculées
const charName = computed(() => {
  if (Array.isArray(props.mapping)) {
    const choices = props.mapping.length ? props.mapping : ['mega-knight','prince','dark-prince','golem']
    return choices[props.questionIndex % choices.length]
  }
  // mapping = fonction
  return props.mapping(props.questionIndex)
})

const makeUrl = (name) => `http://localhost:5001/assets/${name}.png`

// Double buffer pour fondu
const activeLayer = ref('A')     // 'A' ou 'B'
const activeName = ref(charName.value)
const nextName = ref(charName.value)

const activeUrl = computed(() => makeUrl(activeName.value))
const nextUrl = computed(() => makeUrl(nextName.value))

watch(() => props.questionIndex, (/* newVal */) => {
  // Au changement de question : préparer la prochaine image et basculer les couches
  nextName.value = charName.value
  // Bascule de couche après un micro-tick pour laisser le style appliquer
  requestAnimationFrame(() => {
    activeLayer.value = activeLayer.value === 'A' ? 'B' : 'A'
    // Quand la transition est "faite", on copie la source dans l'autre couche pour la prochaine fois
    setTimeout(() => {
      activeName.value = nextName.value
    }, 600) // > var(--fade-duration)
  })
})

const layerA = ref(null)
const layerB = ref(null)

// Parallax léger
function onMove(e){
  const rect = e.currentTarget.getBoundingClientRect()
  const dx = ((e.clientX - rect.left) / rect.width - 0.5) * 2
  const dy = ((e.clientY - rect.top) / rect.height - 0.5) * 2
  const tx = dx * 10
  const ty = dy * -6
  if(layerA.value) layerA.value.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(1.04)`
  if(layerB.value) layerB.value.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(1.04)`
}
function reset(){
  if(layerA.value) layerA.value.style.transform = `translate3d(0,0,0) scale(1.04)`
  if(layerB.value) layerB.value.style.transform = `translate3d(0,0,0) scale(1.04)`
}

onMounted(() => {
  // Init pour que la première image soit visible
  activeName.value = charName.value
  nextName.value = charName.value
})
</script>

<style scoped>
.bg-scene {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}

.bg-scene__layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0;
  transition: opacity 0.6s ease-in-out;
  transform: scale(1.04);
}

.bg-scene__layer.is-active {
  opacity: 1;
}

.bg-scene__glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
  pointer-events: none;
}

/* Variables CSS pour la durée de transition */
:root {
  --fade-duration: 600ms;
}

/* Ne pas bloquer les clics sur le contenu au-dessus */
.bg-scene,
.bg-scene__layer {
  pointer-events: none;
}
</style>


