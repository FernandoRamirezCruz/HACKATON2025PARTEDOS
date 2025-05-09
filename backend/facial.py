import cv2
import mediapipe as mp
from fastapi.responses import StreamingResponse
import time
import numpy as np

def generate_facial_video():
    cap = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()
    drawing = mp.solutions.drawing_utils
    parpadeo_detectado = False
    sonrisa_detectada = False
    contador_parpadeos = 0
    contador_sonrisas = 0
    tiempo_inicio = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = face_mesh.process(frame_rgb)

        if resultados.multi_face_landmarks:
            for rostro in resultados.multi_face_landmarks:
                drawing.draw_landmarks(frame, rostro, mp_face_mesh.FACEMESH_CONTOURS)
                puntos = rostro.landmark
                # Detecta parpadeo
                ojo_izq_sup = puntos[159]
                ojo_izq_inf = puntos[145]
                distancia_ojo = np.linalg.norm(
                    np.array([ojo_izq_sup.x, ojo_izq_sup.y]) - 
                    np.array([ojo_izq_inf.x, ojo_izq_inf.y])
                )
                if distancia_ojo < 0.01 and not parpadeo_detectado:
                    contador_parpadeos += 1
                    parpadeo_detectado = True
                elif distancia_ojo >= 0.01:
                    parpadeo_detectado = False

                # Detecta sonrisa
                boca_izq = puntos[61]
                boca_der = puntos[291]
                distancia_boca = np.linalg.norm(
                    np.array([boca_izq.x, boca_izq.y]) - 
                    np.array([boca_der.x, boca_der.y])
                )
                if distancia_boca > 0.05 and not sonrisa_detectada:
                    contador_sonrisas += 1
                    sonrisa_detectada = True
                elif distancia_boca <= 0.05:
                    sonrisa_detectada = False

        tiempo_actual = time.time()
        tiempo_transcurrido = int(tiempo_actual - tiempo_inicio)

        # Mostrar datos en pantalla
        cv2.putText(frame, f"Parpadeos: {contador_parpadeos}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Sonrisas: {contador_sonrisas}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"Tiempo: {tiempo_transcurrido}s", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
