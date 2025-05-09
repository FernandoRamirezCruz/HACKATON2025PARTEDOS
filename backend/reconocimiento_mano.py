import cv2
import mediapipe as mp
import time
import random

GESTURES = {
    "puño": [0, 0, 0, 0, 0],
    "palma": [1, 1, 1, 1, 1],
    "paz": [0, 1, 1, 0, 0],
    "pulgar_arriba": [1, 0, 0, 0, 0],
    "ok": [1, 1, 1, 0, 1]
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    fingers = []

    # Pulgar
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Otros dedos
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def match_gesture(fingers, expected):
    return fingers == GESTURES[expected]

def run_game(duration=60, difficulty="easy"):
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(max_num_hands=1)
    score = 0
    start_time = time.time()
    current_gesture = random.choice(list(GESTURES.keys()))

    print(f"¡Comienza el juego! Gesto objetivo: {current_gesture.upper()}")

    while time.time() - start_time < duration:
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                fingers = detect_fingers(handLms)
                mp_drawing.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

                if match_gesture(fingers, current_gesture):
                    score += 1
                    print(f"¡Correcto! Gesto detectado: {current_gesture}")
                    current_gesture = random.choice(list(GESTURES.keys()))
                    time.sleep(1)  # para evitar contar múltiples veces el mismo gesto

        # Mostrar gesto esperado
        cv2.putText(image, f"Gesto: {current_gesture.upper()}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        # Mostrar puntaje
        cv2.putText(image, f"Puntos: {score}", (10, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Mostrar cronómetro
        elapsed = int(time.time() - start_time)
        remaining = duration - elapsed
        cv2.putText(image, f"Tiempo: {remaining}s", (10, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Juego de Gestos", image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Juego terminado. Puntos: {score}")
    return score
