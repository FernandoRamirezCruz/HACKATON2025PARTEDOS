<template>
  <div class="game-container">
    <header class="game-header">
      <h1>{{ gameTitle }}</h1>
    </header>

    <section class="instructions">
      <h2>Instrucciones</h2>
      <p>{{ instructions }}</p>
    </section>

    <main class="game-area">
      <div class="placeholder">¡El juego estará aquí!</div>
    </main>

    <footer class="game-footer">
      <div class="score">Puntuación: {{ score }}</div>
      <div class="other-info">{{ otherInfo }}</div>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'GameInterface',
  setup() {
    const gameTitle = ref('Simón Dice');
    const instructions = ref('Haz el gesto que aparece en pantalla, si no haces el gesto antes de que te toque pierdes.');
    const score = ref(0);
    const otherInfo = ref('Información adicional');

    // Aquí podrías tener lógica para actualizar la puntuación, etc.
    const updateScore = (points) => {
      score.value += points;
    };

    // Por ahora, simulamos una actualización de puntuación después de un tiempo
    setTimeout(() => {
      updateScore(0);

      otherInfo.value = '¡Puntuación actualizada!';
    }, 3000);

    return {
      gameTitle,
      instructions,
      score,
      otherInfo,
      updateScore,
    };
  },
};
</script>

<style scoped>
.game-container {

    color: black;
  display: flex;

  flex-direction: column;
  align-items: center;
  padding: 20px;
  padding-top: 60px;
  font-family: "Montserrat",sans-serif;

  background-color: #f4f4f4;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 600px;
  margin: 20px auto;
}

.game-header {
  text-align: center;
  margin-bottom: 20px;
}

.instructions {
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.game-area {
  background-color: #e0e0e0;
  width: 100%;
  height: 300px; /* Ajusta la altura según necesites */
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  margin-bottom: 20px;
}

.placeholder {
  font-size: 1.2em;
  color: #777;
}

.game-footer {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 10px 0;
  color: #555;
}

.score, .other-info {
  background-color: #fff;
  padding: 8px 12px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
</style>