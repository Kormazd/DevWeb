#!/bin/bash

# Script de démarrage pour le Quiz Clash Royale & Clash of Clans
# Démarre le backend et le frontend

echo "🎮 DÉMARRAGE DU QUIZ CLASH ROYALE & CLASH OF CLANS"
echo "=================================================="

# Fonction pour vérifier si un port est utilisé
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Port $1 déjà utilisé"
        return 0
    else
        echo "❌ Port $1 libre"
        return 1
    fi
}

# Démarrer le backend (API Flask)
echo ""
echo "🚀 Démarrage du backend (API Flask)..."
cd quiz-api

if check_port 5001; then
    echo "   Backend déjà en cours d'exécution sur le port 5001"
else
    echo "   Démarrage du serveur Flask..."
    if [ -x "venv/bin/python" ]; then
        ./venv/bin/python app.py &
    else
        echo "   (Avertissement) venv introuvable, utilisation de python3 système"
        python3 app.py &
    fi
    BACKEND_PID=$!
    echo "   Backend démarré (PID: $BACKEND_PID)"
fi

# Attendre que le backend soit prêt
echo "   Attente du démarrage du backend..."
sleep 3

# Vérifier que le backend répond
if curl -s http://localhost:5001/ > /dev/null; then
    echo "   ✅ Backend opérationnel"
else
    echo "   ❌ Erreur: Backend non accessible"
    exit 1
fi

# Démarrer le frontend (Vue.js)
echo ""
echo "🌐 Démarrage du frontend (Vue.js)..."
cd ../quiz-ui

if check_port 3000; then
    echo "   Frontend déjà en cours d'exécution sur le port 3000"
else
    echo "   Démarrage du serveur de développement Vue.js..."
    npm run dev &
    FRONTEND_PID=$!
    echo "   Frontend démarré (PID: $FRONTEND_PID)"
fi

# Attendre que le frontend soit prêt
echo "   Attente du démarrage du frontend..."
sleep 5

# Vérifier que le frontend répond
if curl -s http://localhost:3000/ > /dev/null; then
    echo "   ✅ Frontend opérationnel"
else
    echo "   ❌ Erreur: Frontend non accessible"
    exit 1
fi

echo ""
echo "🎉 QUIZ DÉMARRÉ AVEC SUCCÈS!"
echo "================================"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5001"
echo ""
echo "📊 Endpoints disponibles:"
echo "   - http://localhost:5001/quiz-info"
echo "   - http://localhost:5001/questions"
echo "   - http://localhost:5001/assets"
echo "   - http://localhost:5001/quiz-complete"
echo ""
echo "🛑 Pour arrêter les serveurs:"
echo "   - Backend: Ctrl+C dans le terminal du backend"
echo "   - Frontend: Ctrl+C dans le terminal du frontend"
echo ""
echo "📖 Documentation: API_DOCUMENTATION.md"
echo ""

# Afficher les logs en temps réel
echo "📋 Logs en temps réel (Ctrl+C pour arrêter):"
echo "============================================="

