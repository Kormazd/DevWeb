<template>
  <div class="qc">
    <div class="qc__header">
      <h2 class="h-royal">{{ title }}</h2>
      <p v-if="subtitle" class="qc__subtitle">{{ subtitle }}</p>
      <img
        v-if="imageUrl"
        class="qc__image"
        :src="imageUrl"
        :alt="title"
      />
    </div>

    <div class="qc__answers">
      <button
        v-for="(a, idx) in answers"
        :key="a.id || idx"
        class="qc__answer"
        :class="{ 'qc__answer--selected': modelValue === idx }"
        type="button"
        @click="$emit('update:modelValue', idx)"
      >
        <span class="qc__badge">{{ idx + 1 }}</span>
        <span class="qc__text">{{ a.text }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
// Props
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  imageUrl: { type: String, default: '' },
  answers: { type: Array, default: () => [] },
  modelValue: { type: Number, default: null },
})

// Emits
defineEmits(['update:modelValue'])
</script>

<style scoped>
.qc {
  display: grid;
  gap: 1.25rem;
}

.qc__header {
  text-align: left;
}

.qc__subtitle {
  color: #7f8c8d;
  margin: 0.25rem 0 0.5rem 0;
  line-height: 1.5;
}

.qc__image {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 0.5rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.08);
}

.qc__answers {
  display: grid;
  gap: 0.75rem;
}

.qc__answer {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  text-align: left;
  background: #fff;
  border: 1px solid #e6e8eb;
  border-radius: 10px;
  padding: 0.85rem 1rem;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
}

.qc__answer:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.06);
}

.qc__answer--selected {
  border-color: #f1c40f;
  box-shadow: 0 0 0 3px rgba(241, 196, 15, 0.25);
}

.qc__badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #2c3e50;
  color: #fff;
  font-weight: 700;
  flex-shrink: 0;
}

.qc__text {
  color: #2c3e50;
}
</style>

