<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-brand" @click="goToHome">
        <h1>CODECRAFT</h1>
        <!-- <img src="/CODECRAFT_LOGO.png" alt="Codecrafters Logo" class="logo-image"> -->
      </div>
      <div class="navbar-links" :class="{ open: isMenuOpen }">
        <router-link to="/" class="navbar-button" @click="closeMenu">Inicio</router-link>
        <router-link to="/juegouno" class="navbar-button" @click="closeMenu">Piedra, papel, tijera</router-link>
        <router-link to="/juegodos" class="navbar-button" @click="closeMenu">Simón dice</router-link>
      </div>
      <div class="menu-toggle" @click="toggleMenu">
        ☰
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    goToHome() {
      this.$router.push({ name: 'HomePage' }); // Asegúrate que 'HomePage' sea un nombre de ruta válido
      this.closeMenu();
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    closeMenu() {
      this.isMenuOpen = false;
    },
  },
};
</script>

<style> /* SIN "scoped" */
/* ... Tus estilos globales y de navbar que ya tienes ... */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700&display=swap');

body {
  margin: 0;
  padding: 0;
  font-family: "",'Montserrat', sans-serif;
  background-color: #0A0A0F;
  color: #E0E0E0;
  min-height: 100vh;
  width: 100vw;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
  width: 100%;
  background-color: transparent; /* Para que se vea el fondo del body si es diferente */
  padding-top: 0px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 0;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 25px;
  background-color: rgba(12, 15, 23, 0.75);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  box-sizing: border-box;
  z-index: 1000;
  height: 70px;
}

.navbar-brand {
  cursor: pointer;
  display: flex;
  align-items: center;
  height: 100%;
}

.logo-image {
  height: 35px;
  width: auto;
  opacity: 0.9;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 15px;
}

.navbar-button {
  color: #b0b0c0;
  text-decoration: none;
  padding: 8px 18px;
  border: 1px solid transparent;
  border-radius: 6px;
  transition: background-color 0.2s, color 0.2s;
  font-weight: 400;
  font-size: 0.9rem;
}

.navbar-button:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #ffffff;
}

.navbar-button.router-link-exact-active {
  color: #ffffff;
  font-weight: 500;
  background-color: rgba(255, 255, 255, 0.08);
}

.menu-toggle {
  display: none;
  font-size: 1.8rem;
  color: #b0b0c0;
  cursor: pointer;
}

@media (max-width: 768px) {
  #app {
    padding-top: 0px;
  }
  .navbar {
    height: 60px;
    padding: 0 15px;
  }
  .logo-image {
    height: 30px;
  }
  .navbar-links {
    position: absolute;
    top: 60px;
    left: 0;
    background-color: rgba(12, 15, 23, 0.95);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    width: 100%;
    flex-direction: column;
    align-items: center;
    gap: 0;
    padding: 15px 0;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }
  .navbar-links.open {
    transform: translateX(0);
  }
  .navbar-button {
    width: 90%;
    text-align: center;
    padding: 12px 15px;
    margin-bottom: 8px;
  }
  .navbar-button:last-child {
    margin-bottom: 0;
  }
  .menu-toggle {
    display: block;
  }
}
</style>
