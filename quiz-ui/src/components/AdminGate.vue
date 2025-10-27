<script setup>
import { ref } from 'vue'
import Auth from '@/services/AuthService'
import QuestionsManager from './QuestionsManager.vue'
import QuizApi from '@/services/QuizApiService'

const isAuth = ref(Auth.isAuthenticated())
const password = ref('')
const loading = ref(false)
const error = ref('')
const notice = ref('')

async function submit(e){
  e?.preventDefault()
  error.value = ''
  loading.value = true
  const ok = await Auth.login(password.value)
  loading.value = false
  if(ok){
    isAuth.value = true
  } else {
    error.value = 'Mot de passe invalide'
  }
}

function logout() {
  Auth.logout()
  isAuth.value = false
  password.value = ''
  error.value = ''
}

async function rebuildDb(){
  notice.value = ''
  const { status } = await QuizApi.rebuildDb()
  notice.value = status === 200 ? 'Base de données reconstruite' : 'Échec du rebuild de la base'
}

async function purgeParticipations(){
  notice.value = ''
  const { status } = await QuizApi.purgeParticipations()
  notice.value = status === 204 ? 'Participations purgées' : 'Échec de la purge des participations'
}

async function exportQuestions(){
  const { status, data } = await QuizApi.exportQuestions()
  if(status >=200 && status < 300){
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'questions-export.json'
    a.click()
    URL.revokeObjectURL(url)
  }
}
</script>

<template>
  <section>
    <div v-if="isAuth" class="admin-shortcuts">
      <router-link to="/admin/questions" class="btn-link">Gérer les questions</router-link>
      <button class="btn-link" @click="$router.back()">Retour</button>
    </div>
    <div v-if="isAuth" class="admin-header">
      <h1>Administration</h1>
      <button @click="logout" class="btn-logout">Se déconnecter</button>
    </div>
    <QuestionsManager v-if="isAuth" />
    <div v-if="isAuth" class="admin-tools">
      <h2>Outils admin</h2>
      <div class="buttons">
        <button class="btn" @click="rebuildDb">Rebuild DB</button>
        <button class="btn" @click="purgeParticipations">Purger les participations</button>
        <button class="btn" @click="exportQuestions">Exporter les questions (JSON)</button>
      </div>
      <p v-if="notice" class="notice-ok">{{ notice }}</p>
    </div>
    <div v-else class="login">
      <h1>Accès admin</h1>
      <p class="notice">Vous n'avez pas accès à cette partie.</p>
      <form @submit="submit" class="form">
        <label for="pwd">Mot de passe</label>
        <input id="pwd" type="password" v-model="password" placeholder="••••••" autocomplete="current-password" autofocus />
        <button type="submit" :disabled="loading">Se connecter</button>
        <p v-if="error" class="err">{{ error }}</p>
      </form>
    </div>
  </section>
</template>

<style scoped>
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 960px;
  margin: 0 auto 2rem;
  padding: 1rem 2rem;
  background: rgba(0,0,0,0.35);
  border-radius: 8px;
  color: #fff;
}

.admin-header h1 {
  margin: 0;
  color: #d4af37;
  font-size: 1.8rem;
}

.btn-logout {
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 6px;
  background: #e74c3c;
  color: #fff;
  font-family: inherit;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-logout:hover {
  background: #c0392b;
}

.login { max-width: 420px; margin: 4rem auto; padding: 2rem; background: rgba(0,0,0,0.35); border-radius: 8px; color: #fff; position: relative; z-index: 3; }
.form { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.5rem; }
.notice { opacity: 0.9; margin-top: 0.25rem; }
label { font-weight: 600; }
input { padding: 0.6rem 0.75rem; border-radius: 6px; border: 1px solid rgba(255,255,255,0.35); background: rgba(255,255,255,0.9); color: #222; }
button { padding: 0.6rem 0.9rem; border: none; border-radius: 6px; background: #d4af37; color: #222; font-weight: 700; cursor: pointer; }
.err { color: #ffb3b3; margin-top: 0.25rem; }

.admin-shortcuts { max-width: 960px; margin: 0.75rem auto 0; display:flex; gap: .5rem; justify-content:flex-end }
.btn-link { padding: 0.6rem 0.9rem; border-radius: 6px; background: #3498db; color: #fff; font-weight: 700; text-decoration: none; font-family: inherit; }

.admin-tools { max-width: 960px; margin: 1rem auto 2rem; padding: 1rem 1.25rem; background: rgba(0,0,0,0.35); border-radius: 8px; color: #fff; }
.admin-tools h2 { margin: 0 0 0.75rem; color: #d4af37; }
.admin-tools .buttons { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.admin-tools .btn { padding: 0.6rem 0.9rem; border: none; border-radius: 6px; background: #d4af37; color: #222; font-weight: 700; cursor: pointer; }
.notice-ok { color: #b6f7b6; margin-top: 0.5rem; }
</style>
