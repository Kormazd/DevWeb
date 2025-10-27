<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import QuizApi from '@/services/QuizApiService'

const route = useRoute()
const router = useRouter()
const isNew = computed(() => route.params.id === 'new')

const form = ref({ title:'', text:'', game:'', position: null, image:'', published: true, answers: [
  { text:'', isCorrect:false }, { text:'', isCorrect:false }, { text:'', isCorrect:false }, { text:'', isCorrect:false }
] })
const loading = ref(!isNew.value)
const saving = ref(false)
const error = ref('')
const previewUrl = ref('')
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5001'

onMounted(async () => {
  if(!isNew.value){
    const { status, data } = await QuizApi.getQuestion(route.params.id)
    if(status>=200 && status<300){
      form.value = {
        title: data.title || '', text: data.text || '', game: data.game || '', position: data.position || null,
        image: data.image || '', published: data.published !== false,
        answers: (data.answers || []).map(a => ({ text: a.text || '', isCorrect: !!a.isCorrect }))
      }
      while(form.value.answers.length < 4) form.value.answers.push({ text:'', isCorrect:false })
      previewUrl.value = data.image_url || ''
    } else { error.value = data?.error || 'Chargement impossible' }
  }
  loading.value = false
})

function ensureSingleCorrect(idx){
  form.value.answers = form.value.answers.map((a,i) => ({ ...a, isCorrect: i===idx }))
}

function onFileChange(e){
  const f = e.target.files?.[0]
  if(!f) return
  previewUrl.value = URL.createObjectURL(f)
  form.value.__file = f
}

async function uploadIfNeeded(){
  if(form.value.__file){
    const { status, data } = await QuizApi.uploadImage(form.value.__file)
    if(status>=200 && status<300){
      form.value.image = data.filename
    } else {
      throw new Error(data?.error || 'Upload échoué')
    }
  }
}

async function save(){
  error.value = ''
  saving.value = true
  try{
    await uploadIfNeeded()
    const payload = { ...form.value }
    delete payload.__file
    if(isNew.value){
      const { status, data } = await QuizApi.postQuestion(payload)
      if(status>=200 && status<300){ router.replace({ name:'AdminQuestions' }) } else { throw new Error(data?.error || 'Erreur création') }
    } else {
      const { status, data } = await QuizApi.putQuestion(route.params.id, payload)
      if(!(status>=200 && status<300)){ throw new Error(data?.error || 'Erreur sauvegarde') }
      router.replace({ name:'AdminQuestions' })
    }
  }catch(e){ error.value = e.message }
  finally{ saving.value = false }
}

function cancel(){ router.back() }
</script>

<template>
  <section class="page">
    <h1>{{ isNew ? 'Créer une question' : 'Éditer la question' }}</h1>
    <button class="btn" type="button" @click="$router.back()" style="margin:.5rem 0">Retour</button>
    <p v-if="loading">Chargement…</p>
    <p v-else-if="error" class="err">{{ error }}</p>

    <form v-else class="form" @submit.prevent="save">
      <div class="row">
        <label>Titre</label>
        <input v-model="form.title" required placeholder="Titre" />
      </div>
      <div class="row">
        <label>Texte</label>
        <textarea v-model="form.text" rows="3" placeholder="Texte de la question"></textarea>
      </div>
      <div class="row">
        <label>Jeu</label>
        <select v-model="form.game">
          <option value="">(non spécifié)</option>
          <option>Clash of Clans</option>
          <option>Clash Royale</option>
          <option>Boom Beach</option>
        </select>
      </div>
      <div class="row">
        <label>Position</label>
        <input v-model.number="form.position" type="number" min="1" placeholder="Position" />
      </div>
      <div class="row">
        <label>Image</label>
        <input type="file" accept="image/*" @change="onFileChange" />
        <input v-model="form.image" placeholder="Nom de fichier (assets)" />
        <div v-if="previewUrl || form.image" class="preview">
          <img :src="previewUrl || (form.image ? apiBase + '/assets/' + form.image : '')" alt="aperçu" />
        </div>
      </div>
      <div class="row">
        <label>Publié</label>
        <input type="checkbox" v-model="form.published" />
      </div>

      <div class="answers">
        <h3>Réponses</h3>
        <div class="answer" v-for="(a, idx) in form.answers" :key="idx">
          <input v-model="a.text" placeholder="Réponse" />
          <label><input type="checkbox" :checked="a.isCorrect" @change="() => ensureSingleCorrect(idx)" /> Correcte</label>
        </div>
      </div>

      <div class="actions">
        <button class="btn" type="submit" :disabled="saving">Sauvegarder</button>
        <button class="btn" type="button" @click="cancel">Annuler</button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.page { max-width: 820px; margin: 0 auto; padding: 1rem 1.25rem; color: #fff; }
.err { color:#ffb3b3 }
.form { display:grid; gap:.75rem }
.row { display:grid; gap:.25rem }
label { font-weight:600 }
input, textarea, select { padding:.6rem .75rem; border-radius:6px; border:1px solid rgba(255,255,255,0.35); background: rgba(255,255,255,0.9); color:#222 }
.preview { margin-top:.5rem }
.preview img { max-width: 260px; height:auto; border-radius:6px; box-shadow: 0 6px 20px rgba(0,0,0,0.35) }
.answers { margin-top:.5rem; display:grid; gap:.5rem }
.answer { display:flex; align-items:center; gap:.5rem }
.actions { display:flex; gap:.5rem; margin-top:.5rem }
.btn { padding:.6rem .9rem; border:none; border-radius:6px; background:#d4af37; color:#222; font-weight:700; cursor:pointer }
</style>
