<template>
  <div class="inicio"> <section class="hero">
      <h1>DETECCIÓN DE GESTOS</h1>
      <p>Interactúa y explora de una manera única e intuitiva.</p>
      <button @click="irAAbout" class="cta-button">Descubre Más</button>
    </section>

    <section class="about" id="about">
      <h2>¿Qué es la Detección de Gestos?</h2>
      <p>Es una tecnología que permite a las computadoras entender e interpretar los movimientos humanos, abriendo un mundo de interacciones naturales e innovadoras.</p>
    </section>

    <section class="features">
      <h2>Capacidades Destacadas</h2>
      <div class="feature-cards">
        <div class="feature-card">
          <h3><span class="icon">✨</span> Interacción Intuitiva</h3>
          <p>Controla aplicaciones y juegos con movimientos naturales de tu rostro y manos.</p>
        </div>
        <div class="feature-card">
          <h3><span class="icon">💡</span> Experiencias Inmersivas</h3>
          <p>Sumérgete en entornos digitales que responden a tus expresiones y acciones.</p>
        </div>
        <div class="feature-card">
          <h3><span class="icon">🚀</span> Innovación Constante</h3>
          <p>Explora la frontera de la interacción humano-computadora con tecnología de vanguardia.</p>
        </div>
      </div>
    </section>

    <section class="innovation">
      <h2>El Futuro de la Interacción</h2>
      <p>Los algoritmos avanzados y sensores precisos están transformando cómo interactuamos con la tecnología, haciéndola más personal, expresiva y eficiente.</p>
    </section>

    <footer class="footer">
      <img src="/CODECRAFT_LOGO.png" alt="Codecraft Logo" class="footer-logo-home">
      <p>© Codecraft 2025. Innovación en cada gesto.</p>
    </footer>
  </div>
</template>

<script>
// Tu script de HomePage.vue sigue igual
export default {
  name: 'HomePage',
  methods: {
    irAAbout() {
      const seccionAbout = document.getElementById('about');
      if (seccionAbout) {
        seccionAbout.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Doto:wght@100..900&family=Montserrat:wght@600&family=Pixelify+Sans:wght@400..700&family=Rubik+Pixels&display=swap');
.inicio {
  display: flex;
  flex-direction: column;
  /* min-height: calc(100vh - 70px); Ya no es necesario aquí si router-view se expande bien */
  flex-grow: 1; /* Para que .inicio ocupe el espacio disponible dentro de #app (que es flex) */
  font-family: "Rubik Pixels",'Pixelify Sans', 'Montserrat', sans-serif; /* Hereda, pero puedes re-declarar */
  color: #E0E0E0;
  scroll-behavior: smooth;
  width: 100%;
  box-sizing: border-box;
  position: relative;
  overflow: hidden; /* Clave para que los gradientes no causen desbordamiento */

  /* Fondo tipo Aurora aplicado directamente a .inicio */
  background-color: #0A0A0F; /* Un color base oscuro por si los gradientes no cargan o para rellenar */
  background-image:
    radial-gradient(ellipse at 10% 20%, hsla(170, 60%, 40%, 0.35) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%, hsla(220, 60%, 40%, 0.25) 0%, transparent 60%),
    radial-gradient(ellipse at 90% 30%, hsla(200, 50%, 35%, 0.3) 0%, transparent 55%),
    radial-gradient(ellipse at 30% 90%, hsla(260, 50%, 30%, 0.2) 0%, transparent 70%);
  /* Juega con los valores de hsla (tono, saturación, luminosidad, alfa)
     y las posiciones (ellipse at X% Y%) para el efecto deseado.
     También con el porcentaje de 'transparent' para controlar la dispersión.
     La opacidad de la capa entera .aurora-background ya no es necesaria si
     controlas la opacidad de cada gradiente con el valor alfa en hsla.
  */
  background-blend-mode: screen; /* Prueba diferentes modos de mezcla */
}

/* Todas las secciones internas ahora deben estar posicionadas relativas
   para que aparezcan por encima del fondo de .inicio si este tuviera pseudo-elementos.
   Pero como el fondo está directamente en .inicio, solo necesitamos z-index en el hero
   si hay elementos de fondo superpuestos que podrían cubrir el texto. */

/* --- Hero Section --- */
.p {
    font-family: "Pixelify Sans";
}

.hero {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 70vh; /* Ajustado */
  padding: 100px 20px; /* Ajustado */
  text-align: center;
  position: relative;
  z-index: 1; /* Para estar sobre cualquier pseudo-elemento de fondo de .inicio si los usaras */
}

.hero h1 {
  font-size: 4rem;
  font-weight: 300;
  color: #FFFFFF;
  margin-bottom: 15px;
  letter-spacing: 0.5px;
  text-shadow: 0 0 20px rgba(200, 220, 255, 0.4), 0 0 30px rgba(180, 200, 255, 0.2); /* Glow más pronunciado */
}

.hero p {
  font-size: 1.3rem;
  font-family: "Pixelify Sans";
  margin-bottom: 30px;
  color: #b0b0c0;
  max-width: 600px;
  line-height: 1.6;
}

.cta-button {

  background-color: #FFFFFF;
  color: #12121a; /* Texto oscuro para contraste */
  border: none;
  padding: 14px 35px;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
  font-family: "Pixelify Sans";
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1), 0 0 30px rgba(255,255,255,0.1); /* Doble sombra */
}

.cta-button:hover {
  font-family: "Pixelify Sans";
  background-color: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.15), 0 0 40px rgba(255,255,255,0.2);
}

/* --- Secciones Generales --- */
.about, .features, .innovation {
  padding: 60px 20px;
  text-align: center;
  position: relative;
  z-index: 1;
  background-color: rgba(10,10,20, 0.1); /* Fondo muy sutil para separar secciones del fondo aurora */
  border-top: 1px solid rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  margin-top: -1px; /* Para que los bordes se solapen y no se vean dobles */
}
.about:last-of-type, .features:last-of-type, .innovation:last-of-type {
  border-bottom: none;
}


.about h2, .features h2, .innovation h2 {
      font-family: "Pixelify Sans";
  margin-bottom: 20px;
  font-size: 2rem;
  font-weight: 500;
  color: #d0d0d5;
}

.about p, .innovation p {
  font-family: "Pixelify Sans";
  font-size: 1.1rem;
  line-height: 1.7;
  max-width: 700px;
  margin: 0 auto 20px auto;
  color: #a0a0b0;
}

/* --- Feature Cards --- */
.feature-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
  margin-top: 40px;
}

.feature-card {
  font-family: "Pixelify Sans";
  background-color: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 25px;
  border-radius: 8px;
  width: 300px;
  transition: transform 0.3s, background-color 0.3s, border-color 0.3s;
  text-align: center;
}

.feature-card .icon {
  font-size: 1.8rem;
  display: block;
  margin-bottom: 15px;
  color: #00CFDE; /* Un cyan brillante para los iconos */
}

.feature-card h3 {
  margin-bottom: 15px;
  font-size: 1.25rem;
  font-weight: 500;
  color: #c5c5d0;
}
.feature-card p {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #9090a0;
}

.feature-card:hover {
  transform: translateY(-5px) scale(1.02); /* Ligero scale en hover */
  background-color: rgba(255, 255, 255, 0.04);
  border-color: rgba(0, 207, 222, 0.3); /* Borde con color de acento en hover */
}

/* --- Footer --- */
.footer {
      font-family: "Pixelify Sans";
  text-align: center;
  padding: 30px 20px;
  font-size: 0.85rem;
  background-color: transparent;
  color: #707080;
  position: relative;
  z-index: 1;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-logo-home {
  height: 30px;
  width: auto;
  margin-bottom: 8px;
  opacity: 0.6;
}

/* --- Media Queries (sin cambios importantes aquí, pero revisa si todo se ve bien) --- */
@media (max-width: 768px) {
  .inicio {
    /* background-size: cover; si el fondo aurora se ve mal, prueba ajustar esto */
  }
  .hero {
    min-height: 60vh;
    padding: 30px 15px 50px 15px;
  }
  .hero h1 {
    font-size: 2.3rem;
  }
  .hero p {
    font-size: 1.1rem;
  }
  .cta-button {
    padding: 12px 30px;
    font-size: 0.95rem;
  }

  .about, .features, .innovation {
    padding: 40px 15px;
  }
  .about h2, .features h2, .innovation h2 {
    font-size: 1.7rem;
  }
  .about p, .innovation p {
    font-size: 1rem;
  }

  .feature-card {
    width: calc(100% - 30px);
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
