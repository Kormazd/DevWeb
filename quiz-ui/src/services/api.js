import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5001'
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('quiz_admin_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auto-logout on server down (after N failures) or immediate on 401/403
let redirectingToLogin = false
let consecutiveServerFailures = 0
const MAX_SERVER_FAILURES = 3

function logoutToLogin(reason = 'unauthorized') {
  if (redirectingToLogin) return
  try {
    redirectingToLogin = true
    localStorage.removeItem('quiz_admin_token')
    const isOnAdmin = router?.currentRoute?.value?.meta?.requiresAuth || router?.currentRoute?.value?.path?.startsWith?.('/admin')
    if (isOnAdmin) {
      router.replace({ name: 'AdminLogin', query: { reason } }).finally(() => {
        setTimeout(() => { redirectingToLogin = false }, 500)
      })
    } else {
      setTimeout(() => { redirectingToLogin = false }, 500)
    }
  } catch (_) {
    redirectingToLogin = false
  }
}
api.interceptors.response.use(
  (response) => {
    // Any successful response resets the failure counter
    consecutiveServerFailures = 0
    return response
  },
  (error) => {
    const token = localStorage.getItem('quiz_admin_token')
    const status = error?.response?.status
    const url = error?.config?.url || ''
    const isLoginCall = /\/login(\?|$)/.test(url)

    const isNetworkDown = !error?.response || status === 0 // unreachable / timeout
    const isServerError = typeof status === 'number' && status >= 500
    const isAuthError = status === 401 || status === 403

    if (token && isAuthError && !isLoginCall) {
      logoutToLogin('unauthorized')
    } else if (token && (isNetworkDown || isServerError) && !isLoginCall) {
      consecutiveServerFailures += 1
      if (consecutiveServerFailures >= MAX_SERVER_FAILURES) {
        consecutiveServerFailures = 0
        logoutToLogin('server_off')
      }
    }
    return Promise.reject(error)
  }
)

// Heartbeat disabled: rely on real API traffic to detect server issues

/**
 * Résout l'URL d'une image pour l'affichage
 * @param {string} raw - Chemin de l'image venant de la BDD
 * @returns {string} - URL exploitable pour <img src="">
 */
export function imageUrl(raw) {
  if (!raw) return ''
  // déjà absolue
  if (/^https?:\/\//i.test(raw)) return raw
  // data URL (fichier choisi côté admin)
  if (typeof raw === 'string' && raw.startsWith('data:')) return raw
  // normalisations de compatibilité
  // /uploads/foo.png -> /images/foo.png (migration vers public/)
  if (raw.startsWith('/uploads/')) return `/images/${raw.split('/').pop()}`
  // /assets/foo.png -> /images/foo.png (anciens champs backend)
  if (raw.startsWith('/assets/')) return `/images/${raw.split('/').pop()}`
  // déjà un chemin public absolu (ex: /images/foo.png)
  if (raw.startsWith('/')) return raw
  // sinon, considérer que la BDD ne stocke que le nom de fichier
  // et que les fichiers sont servis depuis public/images
  return `/images/${raw}`
}

export default api




