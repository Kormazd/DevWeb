<script setup>
const props = defineProps({ currentQuestion: Object })
const emit = defineEmits(['answer-selected'])
</script>

<template>
  <div v-if="currentQuestion">
    <h3>{{ currentQuestion.title }}</h3>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" class="img-fluid mb-3" />
    <p>{{ currentQuestion.text }}</p>

    <div class="list-group">
      <button
        v-for="ans in currentQuestion.possibleAnswers"
        :key="ans.id"
        class="list-group-item list-group-item-action"
        @click="emit('answer-selected', ans)"
      >
        {{ ans.text }}
      </button>
    </div>
  </div>
</template>


