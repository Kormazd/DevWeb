<script setup>
import { ref } from 'vue'
import Auth from '@/services/AuthService'
import { useRouter } from 'vue-router'

const password = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()

async function submit(e){
  e?.preventDefault()
  error.value = ''
  loading.value = true
  const ok = await Auth.login(password.value)
  loading.value = false
  if(ok){
    router.replace('/admin')
  } else {
    error.value = 'Mot de passe invalide'
  }
}
</script>

<template>
  <section class="login">
    <h1>Connexion Admin</h1>
    <button class="btn" type="button" @click="$router.back()" style="margin-bottom:0.75rem">Retour</button>
    <form @submit="submit" class="form">
      <label for="pwd">Mot de passe</label>
      <input id="pwd" type="password" v-model="password" placeholder="••••••" autocomplete="current-password" autofocus />
      <button class="btn" type="submit" :disabled="loading">Connexion</button>
      <p v-if="error" class="err">{{ error }}</p>
    </form>
  </section>
</template>

<style scoped>
.login { max-width: 420px; margin: 4rem auto; padding: 2rem; background: rgba(0,0,0,0.35); border-radius: 8px; color: #fff; position: relative; z-index: 3; }
.form { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.5rem; }
label { font-weight: 600; }
input { padding: 0.6rem 0.75rem; border-radius: 6px; border: 1px solid rgba(255,255,255,0.35); background: rgba(255,255,255,0.9); color: #222; }
.btn { padding: 0.6rem 0.9rem; border: none; border-radius: 6px; background: #d4af37; color: #222; font-weight: 700; cursor: pointer; }
.err { color: #ffb3b3; margin-top: 0.25rem; }
</style>



