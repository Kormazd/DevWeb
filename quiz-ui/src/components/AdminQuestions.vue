<script setup>
import { onMounted, ref, computed } from 'vue'
import QuizApi from '@/services/QuizApiService'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(true)
const error = ref('')
const qlist = ref([])
const search = ref('')
const onlyPublished = ref(false)

async function load(){
  loading.value = true
  error.value = ''
  const { status, data } = await QuizApi.getQuestions()
  if(status>=200 && status<300){ qlist.value = data } else { error.value = data?.error || 'Erreur chargement' }
  loading.value = false
}

onMounted(load)

const filtered = computed(() => {
  let arr = Array.isArray(qlist.value) ? qlist.value : []
  if (search.value.trim()) {
    const s = search.value.toLowerCase()
    arr = arr.filter(q => (q.title||'').toLowerCase().includes(s) || String(q.position||'').includes(s))
  }
  if (onlyPublished.value) arr = arr.filter(q => q.published !== false)
  return arr
})

function createNew(){ router.push({ name: 'AdminQuestionEdit', params: { id: 'new' } }) }
function editQuestion(q){ router.push({ name: 'AdminQuestionEdit', params: { id: q.id } }) }

async function togglePublish(q){
  const next = !(q.published !== false)
  await QuizApi.setPublished(q.id, next)
  q.published = next
}

async function remove(q){
  if(!confirm('Supprimer cette question ?')) return
  await QuizApi.deleteQuestion(q.id)
  await load()
}
</script>

<template>
  <section class="page">
    <div class="header">
      <h1>Questions</h1>
      <div class="tools">
        <button class="btn" type="button" @click="$router.back()">Retour</button>
        <input v-model="search" placeholder="Rechercher…" />
        <label><input type="checkbox" v-model="onlyPublished"/> Publiées</label>
        <button class="btn" @click="createNew">Créer une question</button>
      </div>
    </div>

    <p v-if="loading">Chargement…</p>
    <p v-else-if="error" class="err">{{ error }}</p>

    <div v-else class="list">
      <div v-for="q in filtered" :key="q.id" class="item">
        <div class="main">
          <strong>#{{ q.position }}</strong>
          <span class="title">{{ q.title }}</span>
          <span class="badge" :class="{ off: q.published === false }">{{ q.published === false ? 'Brouillon' : 'Publié' }}</span>
        </div>
        <div class="actions">
          <button class="btn" @click="() => togglePublish(q)">{{ q.published === false ? 'Publier' : 'Dépublier' }}</button>
          <button class="btn" @click="() => editQuestion(q)">Éditer</button>
          <button class="btn danger" @click="() => remove(q)">Supprimer</button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.page { max-width: 980px; margin: 0 auto; padding: 1rem 1.25rem; color: #fff; }
.header { display:flex; align-items:center; justify-content: space-between; margin-bottom: 1rem; }
.tools { display:flex; align-items:center; gap: .5rem; }
input { padding:.5rem .6rem; border-radius: 6px; border:1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.9); color:#222; }
.list { display:grid; gap:.5rem; }
.item { display:flex; align-items:center; justify-content: space-between; background: rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.15); border-radius: 8px; padding:.6rem .75rem; }
.main { display:flex; align-items:center; gap:.6rem; }
.title { opacity:.95 }
.badge { font-size:.85rem; padding:.15rem .5rem; border-radius: 6px; background:#2ecc71; color:#0b0d12; font-weight:700 }
.badge.off { background:#f1c40f }
.actions { display:flex; gap:.4rem }
.btn { padding:.5rem .7rem; border:none; border-radius:6px; background:#d4af37; color:#222; font-weight:700; cursor:pointer }
.btn.danger { background:#e74c3c; color:#fff }
.err { color:#ffb3b3 }
</style>
