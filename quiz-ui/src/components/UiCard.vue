<template>
  <div class="card" :style="{ padding }">
    <slot />
  </div>
</template>

<script setup>
defineProps({ padding: { type: String, default: '18px' } })
</script>

