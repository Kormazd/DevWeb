// Quiz Supercell - JavaScript pour l'interactivitÃ©
class SupercellQuiz {
    constructor() {
        this.currentQuestion = 0;
        this.score = 0;
        this.questions = [];
        this.userAnswers = [];
        this.isAnswered = false;
        
        this.initializeElements();
        this.bindEvents();
        this.loadQuestions();
    }
    
    initializeElements() {
        // Ã‰crans
        this.welcomeScreen = document.getElementById('welcome-screen');
        this.quizScreen = document.getElementById('quiz-screen');
        this.resultsScreen = document.getElementById('results-screen');
        
        // Boutons
        this.startBtn = document.getElementById('start-quiz');
        this.nextBtn = document.getElementById('next-question');
        this.restartBtn = document.getElementById('restart-quiz');
        this.shareBtn = document.getElementById('share-results');
        
        // Ã‰lÃ©ments du quiz
        this.questionText = document.getElementById('question-text');
        this.questionCategory = document.getElementById('question-category');
        this.answersContainer = document.getElementById('answers-container');
        this.currentQuestionSpan = document.getElementById('current-question');
        this.totalQuestionsSpan = document.getElementById('total-questions');
        this.currentScoreSpan = document.getElementById('current-score');
        this.progressFill = document.querySelector('.progress-fill');
        
        // Ã‰lÃ©ments des rÃ©sultats
        this.finalScore = document.getElementById('final-score');
        this.finalPoints = document.getElementById('final-points');
        this.correctAnswers = document.getElementById('correct-answers');
        this.accuracy = document.getElementById('accuracy');
        this.achievementBadge = document.getElementById('achievement-badge');
    }
    
    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startQuiz());
        this.nextBtn.addEventListener('click', () => this.nextQuestion());
        this.restartBtn.addEventListener('click', () => this.restartQuiz());
        this.shareBtn.addEventListener('click', () => this.shareResults());
    }
    
    async loadQuestions() {
        try {
            // On appelle la route GET /questions de notre backend
            const response = await api.getQuestions();
            
            // Les questions viennent maintenant de la vraie base de donnÃ©es !
            this.questions = response.data; 
    
            // On met Ã  jour le nombre total de questions
            this.totalQuestionsSpan.textContent = this.questions.length;
            
            console.log("Questions chargÃ©es depuis l'API avec succÃ¨s !");
    
        } catch (error) {
            console.error("Erreur lors du chargement des questions depuis l'API:", error);
            // Affiche un message d'erreur Ã  l'utilisateur
            this.questionText.textContent = "Impossible de charger les questions. Veuillez vÃ©rifier que le serveur backend est bien dÃ©marrÃ© et rafraÃ®chir la page.";
            this.answersContainer.innerHTML = '';
        }
    }
    
    startQuiz() {
        this.currentQuestion = 0;
        this.score = 0;
        this.userAnswers = [];
        
        this.showScreen(this.quizScreen);
        this.displayQuestion();
        this.updateProgress();
        this.updateScore();
    }
    
    showScreen(screen) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        screen.classList.add('active');
        
        // Animation d'entrÃ©e
        screen.style.animation = 'none';
        screen.offsetHeight; // Trigger reflow
        screen.style.animation = 'fadeInUp 0.5s ease';
    }
    
    displayQuestion() {
        const question = this.questions[this.currentQuestion];
        this.isAnswered = false;
        
        this.questionText.textContent = question.question;
        this.questionCategory.textContent = question.category;
        this.currentQuestionSpan.textContent = this.currentQuestion + 1;
        
        // CrÃ©er les options de rÃ©ponse
        this.answersContainer.innerHTML = '';
        question.answers.forEach((answer, index) => {
            const answerElement = document.createElement('div');
            answerElement.className = 'answer-option';
            answerElement.textContent = answer;
            answerElement.addEventListener('click', () => this.selectAnswer(index));
            this.answersContainer.appendChild(answerElement);
        });
        
        this.nextBtn.disabled = true;
        this.nextBtn.textContent = this.currentQuestion === this.questions.length - 1 ? 'Voir les résultats' : 'Question suivante';
    }
    
    selectAnswer(selectedIndex) {
        if (this.isAnswered) return;
        
        this.isAnswered = true;
        const question = this.questions[this.currentQuestion];
        const answerOptions = document.querySelectorAll('.answer-option');
        
        // Marquer la rÃ©ponse sÃ©lectionnÃ©e
        answerOptions[selectedIndex].classList.add('selected');
        
        // RÃ©vÃ©ler la bonne rÃ©ponse aprÃ¨s un dÃ©lai
        setTimeout(() => {
            answerOptions.forEach((option, index) => {
                if (index === question.correct) {
                    option.classList.add('correct');
                } else if (index === selectedIndex && selectedIndex !== question.correct) {
                    option.classList.add('incorrect');
                }
            });
            
            // Calculer le score
            if (selectedIndex === question.correct) {
                this.score += 100;
                this.showFeedback('Correct ! ðŸŽ‰', 'success');
            } else {
                this.showFeedback('Incorrect ðŸ˜”', 'error');
            }
            
            this.userAnswers.push(selectedIndex);
            this.updateScore();
            const isLast = this.currentQuestion === this.questions.length - 1;
            const baseLabel = isLast ? 'Voir les résultats' : 'Question suivante';
            const correctCount = this.userAnswers.filter((ans, idx) => ans === this.questions[idx].correct).length;
            const recap = isLast ? ` — ${correctCount}/${this.questions.length}, ${this.score} pts` : ` — ${this.score} pts`;
            this.nextBtn.textContent = baseLabel + recap;
            const isLast = this.currentQuestion === this.questions.length - 1;\n            const baseLabel = isLast ? 'Voir les résultats' : 'Question suivante';\n            this.nextBtn.textContent = ${baseLabel} (score: );\n            this.nextBtn.disabled = false;
        }, 500);
    }
    
    showFeedback(message, type) {
        // CrÃ©er un Ã©lÃ©ment de feedback temporaire
        const feedback = document.createElement('div');
        feedback.className = `feedback feedback-${type}`;
        feedback.textContent = message;
        feedback.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: ${type === 'success' ? 'var(--primary-green)' : 'var(--primary-red)'};
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: bold;
            z-index: 1000;
            animation: feedbackPop 0.5s ease;
        `;
        
        document.body.appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 1500);
    }
    
    nextQuestion() {
        this.currentQuestion++;
        
        if (this.currentQuestion >= this.questions.length) {
            this.showResults();
        } else {
            this.displayQuestion();
            this.updateProgress();
        }
    }
    
    updateProgress() {
        const progress = ((this.currentQuestion) / this.questions.length) * 100;
        this.progressFill.style.width = `${progress}%`;
    }
    
    updateScore() {
        this.currentScoreSpan.textContent = this.score;
        
        // Animation du score
        this.currentScoreSpan.style.animation = 'none';
        this.currentScoreSpan.offsetHeight;
        this.currentScoreSpan.style.animation = 'pulse 0.5s ease';
    }
    
    showResults() {
        const correctAnswersCount = this.userAnswers.filter((answer, index) => 
            answer === this.questions[index].correct
        ).length;
        
        const accuracyPercentage = Math.round((correctAnswersCount / this.questions.length) * 100);
        
        this.finalScore.textContent = `${correctAnswersCount}/${this.questions.length}`;
        this.finalPoints.textContent = `${this.score} points`;
        this.correctAnswers.textContent = `${correctAnswersCount}/${this.questions.length}`;
        this.accuracy.textContent = `${accuracyPercentage}%`;
        
        // DÃ©terminer le badge d'achievement
        this.updateAchievementBadge(accuracyPercentage);
        
        this.showScreen(this.resultsScreen);
        
        // Animation des statistiques
        setTimeout(() => {
            document.querySelectorAll('.stat-value').forEach((stat, index) => {
                stat.style.animation = `slideInRight ${0.3 + index * 0.1}s ease`;
            });
        }, 300);
    }
    
    updateAchievementBadge(accuracy) {
        const badgeIcon = this.achievementBadge.querySelector('.badge-icon');
        const badgeText = this.achievementBadge.querySelector('.badge-text');
        
        if (accuracy >= 90) {
            badgeIcon.textContent = 'ðŸ‘‘';
            badgeText.textContent = 'Roi Supercell !';
            this.achievementBadge.style.background = 'linear-gradient(135deg, #FFD700, #FFA500)';
        } else if (accuracy >= 70) {
            badgeIcon.textContent = 'ðŸ†';
            badgeText.textContent = 'Champion Supercell !';
            this.achievementBadge.style.background = 'linear-gradient(135deg, #C0C0C0, #87CEEB)';
        } else if (accuracy >= 50) {
            badgeIcon.textContent = 'ðŸŽ–ï¸';
            badgeText.textContent = 'Guerrier Supercell !';
            this.achievementBadge.style.background = 'linear-gradient(135deg, #CD7F32, #D2691E)';
        } else {
            badgeIcon.textContent = 'ðŸŽ®';
            badgeText.textContent = 'Apprenti Supercell !';
            this.achievementBadge.style.background = 'linear-gradient(135deg, #696969, #808080)';
        }
    }
    
    restartQuiz() {
        this.showScreen(this.welcomeScreen);
    }
    
    shareResults() {
        const correctAnswersCount = this.userAnswers.filter((answer, index) => 
            answer === this.questions[index].correct
        ).length;
        
        const shareText = `ðŸŽ® J'ai terminÃ© le Quiz Supercell ! ðŸŽ®\n\n` +
                         `ðŸ“Š Score: ${correctAnswersCount}/${this.questions.length}\n` +
                         `â­ Points: ${this.score}\n` +
                         `ðŸŽ¯ PrÃ©cision: ${Math.round((correctAnswersCount / this.questions.length) * 100)}%\n\n` +
                         `Testez vos connaissances sur l'univers Supercell !`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Quiz Supercell - Mes rÃ©sultats',
                text: shareText,
                url: window.location.href
            });
        } else {
            // Fallback pour les navigateurs qui ne supportent pas l'API de partage
            navigator.clipboard.writeText(shareText).then(() => {
                this.showFeedback('RÃ©sultats copiÃ©s ! ðŸ“‹', 'success');
            }).catch(() => {
                // Fallback ultime
                const textarea = document.createElement('textarea');
                textarea.value = shareText;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                this.showFeedback('RÃ©sultats copiÃ©s ! ðŸ“‹', 'success');
            });
        }
    }
}

// Styles CSS supplÃ©mentaires pour les animations
const additionalStyles = `
    @keyframes feedbackPop {
        0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }
        50% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.1);
        }
        100% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
    
    .feedback {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
`;

// Ajouter les styles supplÃ©mentaires
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Initialiser le quiz quand le DOM est chargÃ©
document.addEventListener('DOMContentLoaded', () => {
    new SupercellQuiz();
});

// Easter eggs et effets spÃ©ciaux
document.addEventListener('keydown', (e) => {
    // Konami Code: â†‘â†‘â†“â†“â†â†’â†â†’BA
    const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    if (!window.konamiSequence) window.konamiSequence = [];
    
    window.konamiSequence.push(e.keyCode);
    window.konamiSequence = window.konamiSequence.slice(-10);
    
    if (window.konamiSequence.join(',') === konamiCode.join(',')) {
        // Effet spÃ©cial Konami Code
        document.body.style.animation = 'rainbow 2s ease infinite';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 5000);
    }
});

// Animation rainbow pour l'easter egg
const rainbowStyle = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        25% { filter: hue-rotate(90deg); }
        50% { filter: hue-rotate(180deg); }
        75% { filter: hue-rotate(270deg); }
        100% { filter: hue-rotate(360deg); }
    }
`;

const rainbowSheet = document.createElement('style');
rainbowSheet.textContent = rainbowStyle;
document.head.appendChild(rainbowSheet);


