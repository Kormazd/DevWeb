<template>
  <header class="container" style="display:flex; align-items:center; justify-content:space-between; gap:16px;">
    <h1 class="h-royal">Quiz Royale</h1>
    <div style="display:flex; gap:10px; align-items:center;">
      <UiBadge>💎 {{ gems }}</UiBadge>
      <UiBadge>⭐ {{ crowns }}</UiBadge>
      <UiButton variant="gold">Boutique</UiButton>
    </div>
  </header>
</template>

<script setup>
import UiBadge from './UiBadge.vue'
import UiButton from './UiButton.vue'

defineProps({ 
  gems: { type: Number, default: 120 }, 
  crowns: { type: Number, default: 3 } 
})
</script>

