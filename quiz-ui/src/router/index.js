import { createRouter, createWebHistory } from 'vue-router'

// Imports depuis src/components
import HomePage from '../components/HomePage.vue'
import NewQuizPage from '../components/NewQuizPage.vue'
import ScorePage from '../components/ScorePage.vue'
import QuestionsManager from '../components/QuestionsManager.vue'
import AdminGate from '../components/AdminGate.vue'

const routes = [
  { path: '/', name: 'HomePage', component: ScorePage },
  { path: '/new-quiz', name: 'NewQuizPage', component: NewQuizPage },
  { path: '/score', name: 'ScorePage', component: ScorePage },
  { path: '/admin', name: 'Admin', component: AdminGate },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Plus de redirection globale: le gate s'occupe du mot de passe côté /admin

export default router
