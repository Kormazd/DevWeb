<script setup>
import { onMounted, ref } from 'vue'
import QuizApi from '@/services/QuizApiService'

const loading = ref(true)
const error = ref('')
const questions = ref([])

async function load() {
  loading.value = true
  error.value = ''
  const { status, data } = await QuizApi.getQuestions()
  if (status >= 200 && status < 300 && Array.isArray(data)) {
    questions.value = data
  } else {
    error.value = data?.error || 'Chargement des questions échoué'
  }
  loading.value = false
}

onMounted(load)
</script>

<template>
  <section class="page">
    <h1>Gestion des questions</h1>
    <p v-if="loading">Chargement…</p>
    <p v-else-if="error" class="err">{{ error }}</p>

    <div v-else class="list">
      <div v-for="q in questions" :key="q.id" class="item">
        <div class="item__main">
          <strong>#{{ q.position }}</strong>
          <span class="title">{{ q.title }}</span>
        </div>
        <div class="item__meta">
          <span>{{ (q.answers || []).length }} réponses</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.page {
  max-width: 960px;
  margin: 0 auto;
  padding: 1rem 2rem;
  color: #fff;
}
.err { color: #ffb3b3; }
.list { display: grid; gap: 0.5rem; margin-top: 1rem; }
.item { display: flex; align-items: center; justify-content: space-between; background: rgba(0,0,0,0.35); padding: 0.5rem 0.75rem; border-radius: 8px; }
.item__main { display: flex; align-items: center; gap: 0.75rem; }
.title { opacity: 0.95; }
</style>