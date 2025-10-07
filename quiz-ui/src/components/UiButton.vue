<template>
  <button :class="['btn', variantClass]" v-bind="$attrs">
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'primary' }
})

const variantClass = computed(() => ({
  'btn--primary': props.variant === 'primary',
  'btn--gold': props.variant === 'gold',
  'btn--danger': props.variant === 'danger',
  'btn--ghost': props.variant === 'ghost'
}))
</script>

