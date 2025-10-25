<script setup>
import { RouterView } from 'vue-router'

</script>

<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-brand">Clash Quiz</router-link>
        <div class="nav-links">
        <router-link to="/" class="nav-link">Accueil</router-link>
        <router-link to="/scores" class="nav-link">Score</router-link>
        <router-link to="/admin" class="nav-link">Admin</router-link>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <RouterView />
    </main>
    
    
  </div>
</template>

<style>
@import '/static/css/style.css';

@font-face {
  font-family: 'ClashRegular';
  src: url('./assets/Fonts/Clash_Regular.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'ClashRegular', sans-serif;
  line-height: 1.6;
  color: #2c3e50;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: linear-gradient(135deg, #2c3e50, #34495e);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
  position: relative;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-family: 'ClashRegular', sans-serif;
  font-size: 1.5rem;
  font-weight: bold;
  color: #d4af37;
  text-decoration: none;
  transition: color 0.3s ease;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.nav-brand:hover {
  color: #3498db;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
}

.nav-link:hover {
  color: #3498db;
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  color: #3498db;
  background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  padding: 2rem 0;
  position: relative;
  z-index: 2; /* ensure view content is above background */
}

.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem 0;
  margin-top: auto;
}

.footer p {
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-links {
    gap: 1rem;
  }
  
  .main-content {
    padding: 1rem 0;
  }
}
</style>
