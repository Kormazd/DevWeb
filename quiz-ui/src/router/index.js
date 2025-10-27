import { createRouter, createWebHistory } from 'vue-router'

// Imports depuis src/components
import HomePage from '../components/HomePage.vue'
import NewQuizPage from '../components/NewQuizPage.vue'
import QuizPage from '../components/QuizPage.vue'
import AdminGate from '../components/AdminGate.vue'
import AdminLogin from '../components/AdminLogin.vue'
import AdminQuestions from '../components/AdminQuestions.vue'
import AdminQuestionEdit from '../components/AdminQuestionEdit.vue'
import ScoresPage from '../components/ScoresPage.vue'

const routes = [
  { path: '/new-quiz', name: 'NewQuizPage', component: NewQuizPage },
  { path: '/quiz', name: 'QuizPage', component: QuizPage },
  { path: '/scores', name: 'ScoresPage', component: ScoresPage },
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/admin/login', name: 'AdminLogin', component: AdminLogin },
  { path: '/admin', name: 'Admin', component: AdminGate, meta: { requiresAuth: true } },
  { path: '/admin/questions', name: 'AdminQuestions', component: AdminQuestions, meta: { requiresAuth: true } },
  { path: '/admin/question/:id', name: 'AdminQuestionEdit', component: AdminQuestionEdit, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Guard: protect admin routes
router.beforeEach((to, from, next) => {
  if (to.meta && to.meta.requiresAuth) {
    const token = localStorage.getItem('quiz_admin_token')
    if (!token) return next({ name: 'AdminLogin', query: { redirect: to.fullPath } })
  }
  next()
})

export default router
