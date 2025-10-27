import api from '@/services/api'

async function request(method, url, data = null) {
  try {
    const response = await api({ method, url, data })
    return { status: response.status, data: response.data }
  } catch (error) {
    const status = error?.response?.status || 500
    const dataResp = error?.response?.data || { error: 'Request failed' }
    return { status, data: dataResp }
  }
}

const quizApiService = {
  // Info & scores
  getQuizInfo() { return request('get', '/quiz-info') },
  getScores(limit = 10) { return request('get', `/scores?limit=${encodeURIComponent(limit)}`) },

  // Questions
  getQuestions(params = {}) {
    const query = typeof params.position === 'number' ? `?position=${params.position}` : ''
    return request('get', `/questions${query}`)
  },
  getQuestion(id) { return request('get', `/questions/${id}`) },
  postQuestion(question) { return request('post', '/questions', question) },
  putQuestion(id, question) { return request('put', `/questions/${id}`, question) },
  deleteQuestion(id) { return request('delete', `/questions/${id}`) },
  setPublished(id, published) { return request('put', `/questions/${id}/publish`, { published }) },
  reorderQuestions(ids) { return request('post', '/questions/reorder', { ids }) },
  exportQuestions() { return request('get', '/questions/export') },
  importQuestions(list, override=false) { return request('post', `/questions/import?override=${override}`, { questions: list }) },

  // Auth (usually use AuthService instead)
  login(password) { return request('post', '/login', { password }) },
  health() { return request('get', '/health') },
  rebuildDb() { return request('post', '/rebuild-db') },

  // Participation & score
  saveParticipation(playerName, answers) { return request('post', '/participations', { playerName, answers }) },
  getParticipation(playerName) { return request('get', `/participations/${encodeURIComponent(playerName)}`) },
  listParticipations(params={}) {
    const q = new URLSearchParams()
    if (params.from) q.set('from', params.from)
    if (params.to) q.set('to', params.to)
    const qs = q.toString()
    return request('get', `/participations${qs ? ('?'+qs) : ''}`)
  },
  purgeParticipations() { return request('delete', '/participations/all') },
  postScore(player, score, total) { return request('post', '/scores', { player, score, total }) },
  uploadImage(file) {
    const form = new FormData()
    form.append('file', file)
    return api.post('/upload-image', form)
      .then(r => ({ status: r.status, data: r.data }))
      .catch(e => ({ status: e?.response?.status || 500, data: e?.response?.data || { error: 'Upload failed' } }))
  },
}

export default quizApiService


