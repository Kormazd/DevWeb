import api from '@/services/api'
const STORAGE_KEY = 'quiz_admin_token'

export default {
  async login(password) {
    try {
      const { data } = await api.post('/login', { password })
      if (data && data.token) {
        window.localStorage.setItem(STORAGE_KEY, String(data.token))
        return true
      }
      return false
    } catch {
      return false
    }
  },
  logout() { window.localStorage.removeItem(STORAGE_KEY) },
  isAuthenticated() {
    return Boolean(window.localStorage.getItem(STORAGE_KEY))
  },
  getToken() { return window.localStorage.getItem(STORAGE_KEY) || '' }
}


