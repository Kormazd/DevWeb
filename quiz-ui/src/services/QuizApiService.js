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

  // Auth (usually use AuthService instead)
  login(password) { return request('post', '/login', { password }) },

  // Participation & score
  saveParticipation(playerName, answers) { return request('post', '/participations', { playerName, answers }) },
  getParticipation(playerName) { return request('get', `/participations/${encodeURIComponent(playerName)}`) },
  postScore(player, score, total) { return request('post', '/scores', { player, score, total }) },
}

export default quizApiService
