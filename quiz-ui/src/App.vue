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
    <footer class="footer contact-footer">
      <div class="contact-box">
        <div class="contact-left">
          <strong>Créateurs</strong>
          <span>Julien • Tom • Lilian</span>
        </div>
        <div class="contact-right">
          <span>Classe: <em>E4FI_1I</em></span>
          <span>École: <em>ESIEE Paris</em></span>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
@import '/static/css/main.css';

@font-face {
  font-family: 'ClashRegular';
  src: url('/fonts/Clash_Regular.woff2') format('woff2');
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

.main-content { flex: 1; padding: 2rem 0 5.5rem; position: relative; z-index: 2; }

.footer { background: rgba(44, 62, 80, 0.9); color: white; padding: 0.75rem 0; position: fixed; left: 0; right: 0; bottom: 0; z-index: 9; backdrop-filter: blur(6px); border-top: 1px solid rgba(255,255,255,0.1); }
.contact-box { max-width: 1200px; margin: 0 auto; padding: 0 1rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; font-size: 0.95rem; }
.contact-left strong { color: #f5d36b; margin-right: 0.5rem; }
.contact-right span { margin-left: 1rem; opacity: 0.95; }

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
    padding: 0 1rem;
  }
  
  .nav-brand {
    font-size: 1.2rem;
  }
  
  .nav-links {
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .nav-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .main-content {
    padding: 1rem 0 6rem;
  }
  
  .footer {
    padding: 0.5rem 0;
    font-size: 0.85rem;
  }
  
  .contact-box {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .contact-right span {
    margin: 0.5rem;
  }
}
</style>
