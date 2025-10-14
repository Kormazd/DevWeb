import axios from 'axios'

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || 'http://localhost:5001/'}`,
  headers: {
    'Content-Type': 'application/json',
  },
})

async function call(method, resource, data = null, token = null) {
  const headers = {}
  if (token) headers.authorization = `Bearer ${token}`
  try {
    const response = await instance({ method, url: resource, data, headers })
    return { status: response.status, data: response.data }
  } catch (error) {
    console.error(error)
    const status = error?.response?.status || 500
    const dataResp = error?.response?.data || { error: 'Request failed' }
    return { status, data: dataResp }
  }
}

const quizApiService = {
  call,
  getQuizInfo() {
    return call('get', 'quiz-info')
  },
  getQuestions() {
    return call('get', 'questions')
  },
  submit(payload) {
    return call('post', 'submit', payload)
  },
  login(password) {
    return call('post', 'login', { password })
  },
  postQuestion(question, token) {
    return call('post', 'questions', question, token)
  },
  putQuestion(id, question, token) {
    return call('put', `questions/${id}`, question, token)
  },
  deleteQuestion(id, token) {
    return call('delete', `questions/${id}`, null, token)
  },
}

export default quizApiService


