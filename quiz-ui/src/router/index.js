import { createRouter, createWebHistory } from 'vue-router'

// Imports depuis src/components
import HomePage from '../components/HomePage.vue'
import NewQuizPage from '../components/NewQuizPage.vue'
import AdminGate from '../components/AdminGate.vue'

const routes = [
  { path: '/new-quiz', name: 'NewQuizPage', component: NewQuizPage },
  { path: '/quiz', redirect: { name: 'NewQuizPage' } },
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/admin', name: 'Admin', component: AdminGate },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Plus de redirection globale: le gate s'occupe du mot de passe côté /admin

export default router