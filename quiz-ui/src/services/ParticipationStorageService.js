export default {
  clear() {
    window.localStorage.removeItem('playerName')
    window.localStorage.removeItem('answers')
    window.localStorage.removeItem('lastScore')
  },
  savePlayerName(name) { window.localStorage.setItem('playerName', name || '') },
  getPlayerName() { return window.localStorage.getItem('playerName') || '' },

  saveAnswers(answers) { window.localStorage.setItem('answers', JSON.stringify(answers || [])) },
  getAnswers() { return JSON.parse(window.localStorage.getItem('answers') || '[]') },

  saveScore(score) { window.localStorage.setItem('lastScore', String(score ?? 0)) },
  getScore() { return Number(window.localStorage.getItem('lastScore') || 0) },
}


