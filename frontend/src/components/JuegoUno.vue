<template>
  <div class="rps-game-container">
    <h1>Piedra, Papel o Tijera (con Gestos)</h1>

    <div class="scores">
      <span>Tú: {{ playerScore }}</span>
      <span>Computadora: {{ computerScore }}</span>
    </div>

    <div class="game-area">
      <div class="player-area">
        <h2>Tu Elección</h2>
        <div class="choice-display" :class="{ 'placeholder': !playerChoice }">
          <img v-if="playerChoice" :src="getChoiceImagePath(playerChoice)" :alt="playerChoice">
          <span v-else>?</span>
        </div>
        <div v-if="gameState === 'waiting_player_choice' && !useGestures" class="click-choices">
          <button @click="playRound('piedra')">Piedra</button>
          <button @click="playRound('papel')">Papel</button>
          <button @click="playRound('tijeras')">Tijera</button>
        </div>
      </div>

      <div class="vs-separator">VS</div>

      <div class="computer-area">
        <h2>Computadora</h2>
        <div class="choice-display" :class="{ 'placeholder': !computerChoice }">
          <img v-if="computerChoice" :src="getChoiceImagePath(computerChoice)" :alt="computerChoice">
          <span v-else>?</span>
        </div>
      </div>
    </div>

    <div class="results-area">
      <p v-if="resultMessage" class="result-message" :class="resultClass">{{ resultMessage }}</p>
      <button v-if="gameState === 'showing_results'" @click="nextRound">Siguiente Ronda</button>
    </div>

    <div class="gesture-controls">
      <label class="toggle-switch">
        <input type="checkbox" v-model="useGestures">
        <span class="slider"></span>
      </label>
      <span>Usar Gestos (Próximamente)</span>

      <div v-if="useGestures">
        <p v-if="gameState === 'waiting_player_choice'">¡Realiza tu gesto!</p>
        <div class="video-feed-container">
          <video ref="videoPlayerRPS" autoplay playsinline muted width="240" height="180"></video>
          <canvas ref="frameCanvasRPS" style="display: none;"></canvas>
        </div>
        <p v-if="isProcessingGesture">Procesando gesto...</p>
        <p v-if="gestureError" class="error-message">{{ gestureError }}</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

// --- Configuración ---
const OPTIONS = ['piedra', 'papel', 'tijeras'];
const WIN_CONDITIONS = {
  piedra: 'tijeras', // Rock vence a Scissors
  papel: 'rock',    // Paper vence a Rock
  tijeras: 'papel' // Scissors vence a Paper
};
const BACKEND_URL_RPS = 'http://localhost:5000'; // Asumiendo que tu backend corre aquí

// --- Estado Reactivo del Juego ---
const playerScore = ref(0);
const computerScore = ref(0);
const playerChoice = ref(null); // 'rock', 'paper', 'scissors'
const computerChoice = ref(null);
const resultMessage = ref('');
const gameState = ref('waiting_player_choice'); // 'waiting_player_choice', 'showing_results'
const useGestures = ref(false); // Para alternar entre clic y gestos (futuro)

// --- Estado para Gestos (futura implementación) ---
const videoPlayerRPS = ref(null);
const frameCanvasRPS = ref(null);
const isProcessingGesture = ref(false);
const gestureError = ref('');
let streamRPS = null;
let frameCaptureIntervalRPS = null;

// --- Imágenes para las Elecciones (requiere que tengas estas imágenes en tu carpeta `public` o `assets`) ---
// Por ejemplo, public/img/rock.png, public/img/paper.png, public/img/scissors.png
const getChoiceImagePath = (choice) => {
  if (!choice) return '';
  // Asegúrate que la ruta sea correcta según la estructura de tu proyecto Vue.
  // Si usas la carpeta `public`, la ruta es relativa a la raíz.
  return `/img/${choice}.png`;
};

const resultClass = computed(() => {
  if (!resultMessage.value) return '';
  if (resultMessage.value.includes('Ganaste')) return 'win';
  if (resultMessage.value.includes('Perdiste')) return 'lose';
  return 'draw';
});


// --- Lógica del Juego ---
function playRound(pChoice) {
  if (gameState.value !== 'waiting_player_choice') return;

  playerChoice.value = pChoice;
  computerChoice.value = OPTIONS[Math.floor(Math.random() * OPTIONS.length)];

  determineWinner();
  gameState.value = 'showing_results';
}

function determineWinner() {
  if (playerChoice.value === computerChoice.value) {
    resultMessage.value = "¡Es un Empate!";
  } else if (WIN_CONDITIONS[playerChoice.value] === computerChoice.value) {
    resultMessage.value = `¡Ganaste! ${capitalize(playerChoice.value)} vence a ${computerChoice.value}.`;
    playerScore.value++;
  } else {
    resultMessage.value = `¡Perdiste! ${capitalize(computerChoice.value)} vence a ${playerChoice.value}.`;
    computerScore.value++;
  }
}

function nextRound() {
  playerChoice.value = null;
  computerChoice.value = null;
  resultMessage.value = '';
  gameState.value = 'waiting_player_choice';

  if (useGestures.value) {
    gestureError.value = '';
    // Reiniciar la detección de gestos si está activa
    startGestureDetection();
  }
}

function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// --- Lógica para Gestos (Futura Implementación) ---
watch(useGestures, (newValue) => {
  if (newValue) {
    setupCameraRPS();
    if (gameState.value === 'waiting_player_choice') {
      startGestureDetection();
    }
  } else {
    stopGestureDetectionAndCamera();
  }
});

async function setupCameraRPS() {
  if (streamRPS) { // Si ya hay un stream, detenerlo primero
    streamRPS.getTracks().forEach(track => track.stop());
    streamRPS = null;
  }
  if (!videoPlayerRPS.value) return;
  try {
    streamRPS = await navigator.mediaDevices.getUserMedia({ video: { width: 240, height: 180 } });
    videoPlayerRPS.value.srcObject = streamRPS;
    videoPlayerRPS.value.onloadedmetadata = () => {
      if (frameCanvasRPS.value) {
        frameCanvasRPS.value.width = videoPlayerRPS.value.videoWidth;
        frameCanvasRPS.value.height = videoPlayerRPS.value.videoHeight;
      }
    };
    gestureError.value = '';
  } catch (err) {
    console.error("Error al acceder a la cámara para RPS:", err);
    gestureError.value = "No se pudo acceder a la cámara.";
    useGestures.value = false; // Volver a modo clic si falla la cámara
  }
}

function startGestureDetection() {
  if (!useGestures.value || gameState.value !== 'waiting_player_choice' || !streamRPS) return;
  if (frameCaptureIntervalRPS) clearInterval(frameCaptureIntervalRPS);

  console.log("Iniciando detección de gestos para Piedra, Papel, Tijera...");
  isProcessingGesture.value = false; // Asegurarse que no esté bloqueado

  frameCaptureIntervalRPS = setInterval(async () => {
    if (isProcessingGesture.value || !useGestures.value || gameState.value !== 'waiting_player_choice') return;

    const imageDataUrl = captureFrameForRPS();
    if (imageDataUrl) {
      isProcessingGesture.value = true;
      gestureError.value = ''; // Limpiar error anterior
      try {
        // Este endpoint `/process_rps_gesture` es el que tendrías que crear en tu backend
        // Debería reconocer 'rock', 'paper', 'scissors' a partir de la imagen de la mano
        const response = await fetch(`${BACKEND_URL_RPS}/process_rps_gesture`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: imageDataUrl })
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.error || `Error del backend: ${response.status}`);
        }

        const data = await response.json(); // Espera algo como { "detected_gesture": "rock" } o null
        isProcessingGesture.value = false;

        if (data.detected_gesture && OPTIONS.includes(data.detected_gesture)) {
          console.log("Gesto detectado por backend:", data.detected_gesture);
          stopGestureDetection(); // Detener la detección una vez que se elige un gesto válido
          playRound(data.detected_gesture);
        } else if (data.detected_gesture) {
          console.warn("Gesto no reconocido para el juego:", data.detected_gesture);
          // Podrías dar un feedback de "gesto no válido"
        }
        // Si es null, sigue intentando en el siguiente intervalo
      } catch (error) {
        console.error("Error procesando gesto RPS:", error);
        gestureError.value = `Error de comunicación: ${error.message}`;
        isProcessingGesture.value = false;
        // Podrías detener la detección aquí o permitir reintentos
      }
    }
  }, 300); // Ajusta la frecuencia de envío de frames (ej. cada 300ms)
}

function stopGestureDetection() {
  clearInterval(frameCaptureIntervalRPS);
  frameCaptureIntervalRPS = null;
  isProcessingGesture.value = false;
}

function stopGestureDetectionAndCamera() {
  stopGestureDetection();
  if (streamRPS) {
    streamRPS.getTracks().forEach(track => track.stop());
    streamRPS = null;
  }
  if (videoPlayerRPS.value) {
    videoPlayerRPS.value.srcObject = null;
  }
  console.log("Cámara y detección de gestos RPS detenidas.");
}


function captureFrameForRPS() {
  if (!videoPlayerRPS.value || !frameCanvasRPS.value || videoPlayerRPS.value.readyState < videoPlayerRPS.value.HAVE_ENOUGH_DATA) {
    return null;
  }
  const context = frameCanvasRPS.value.getContext('2d');
  context.drawImage(videoPlayerRPS.value, 0, 0, frameCanvasRPS.value.width, frameCanvasRPS.value.height);
  return frameCanvasRPS.value.toDataURL('image/jpeg', 0.7);
}


onMounted(() => {
  // El juego está listo para que el jugador elija
});

onUnmounted(() => {
  stopGestureDetectionAndCamera();
});

</script>

<style scoped>
.rps-game-container {
font-family: "Montserrat";
  text-align: center;
  padding: 20px;
  padding-top: 80px;
  background-color: #f4f7f6;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  max-width: 600px;
  margin: 20px auto;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

.scores {
font-family: "Montserrat";
  display: flex;
  justify-content: space-around;
  font-size: 1.2em;
  color: black;
  font-weight: bold;
  margin-bottom: 25px;
  padding: 10px;
  background-color: #e9ecef;
  border-radius: 8px;
}

.game-area {
  display: flex;
  justify-content: space-around;
  align-items: flex-start; /* Alinear items arriba */
  margin-bottom: 25px;
}

.player-area, .computer-area {
  flex: 1;
  padding: 15px;
}

.player-area h2, .computer-area h2 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #555;
}

.choice-display {
  width: 100px;
  height: 100px;
  border: 2px solid #ddd;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto 15px auto;
  background-color: #fff;
  font-size: 3em;
  color: #ccc;
}
.choice-display.placeholder {
  color: #e0e0e0;
}
.choice-display img {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
}

.click-choices button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}
.click-choices button:hover {
  background-color: #0056b3;
}

.vs-separator {
  font-size: 2em;
  font-weight: bold;
  color: #777;
  align-self: center; /* Centrar verticalmente el VS */
  padding: 0 20px;
}

.results-area {
  margin-bottom: 20px;
}
.result-message {
  font-size: 1.3em;
  font-weight: bold;
  min-height: 25px; /* Para evitar saltos de layout */
  margin-bottom: 15px;
}
.result-message.win { color: #28a745; }
.result-message.lose { color: #dc3545; }
.result-message.draw { color: #6c757d; }

.results-area button {
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  cursor: pointer;
}
.results-area button:hover {
  background-color: #218838;
}

.gesture-controls {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #ddd;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px; /* Ancho reducido */
  height: 28px; /* Alto reducido */
  margin-right: 10px;
  vertical-align: middle;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 28px; /* Para que sea ovalado */
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px; /* Tamaño del círculo reducido */
  width: 20px; /* Tamaño del círculo reducido */
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(22px); /* Desplazamiento reducido */
}

.gesture-controls span {
  vertical-align: middle;
}

.video-feed-container {
  margin-top: 10px;
  border: 1px dashed #ccc;
  display: inline-block; /* Para que no ocupe todo el ancho */
}
.video-feed-container video {
  display: block; /* Para quitar espacio extra debajo */
  transform: scaleX(-1); /* Espejo */
}
.error-message {
  color: #dc3545;
  font-size: 0.9em;
  margin-top: 5px;
}
</style>
