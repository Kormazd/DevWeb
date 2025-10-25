<script setup>
import { onMounted, ref } from 'vue'
import QuizApi from '@/services/QuizApiService'

const loading = ref(true)
const error = ref('')
const saving = ref(false)
const questions = ref([])
let dragIndex = -1

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

function onDragStart(index) { dragIndex = index }
function onDragOver(e) { e.preventDefault() }
function onDrop(index) {
  if (dragIndex === -1 || dragIndex === index) return
  const arr = [...questions.value]
  const [moved] = arr.splice(dragIndex, 1)
  arr.splice(index, 0, moved)
  questions.value = arr
  dragIndex = -1
}

async function saveOrder() {
  if (!Array.isArray(questions.value) || !questions.value.length) return
  saving.value = true
  try {
    const updates = questions.value.map((q, idx) => ({ ...q, position: idx + 1 }))
    for (const q of updates) {
      await QuizApi.putQuestion(q.id, {
        title: q.title,
        text: q.text,
        position: q.position,
        image: q.image,
        answers: q.answers || [],
      })
    }
    await load()
  } catch (e) {
    error.value = "Échec de l'enregistrement de l'ordre"
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <section class="page">
    <h1>Gestion des questions</h1>
    <p v-if="loading">Chargement…</p>
    <p v-else-if="error" class="err">{{ error }}</p>

    <div v-else class="list">
      <div
        v-for="(q, idx) in questions"
        :key="q.id"
        class="item"
        draggable="true"
        @dragstart="onDragStart(idx)"
        @dragover="onDragOver"
        @drop="onDrop(idx)"
      >
        <div class="item__main">
          <span class="handle">↕</span>
          <strong>#{{ idx + 1 }}</strong>
          <span class="title">{{ q.title }}</span>
        </div>
        <div class="item__meta">
          <span>{{ (q.answers || []).length }} réponses</span>
        </div>
      </div>
      <div class="actions">
        <button class="btn" :disabled="saving" @click="saveOrder">Enregistrer l'ordre</button>
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
.item { display: flex; align-items: center; justify-content: space-between; background: rgba(0,0,0,0.35); padding: 0.5rem 0.75rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); }
.item__main { display: flex; align-items: center; gap: 0.75rem; }
.title { opacity: 0.95; }
.handle { cursor: grab; user-select: none; opacity: 0.85; }
.actions { margin-top: 0.75rem; }
.btn { padding: 0.6rem 0.9rem; border: none; border-radius: 6px; background: #d4af37; color: #222; font-weight: 700; cursor: pointer; }
</style>

