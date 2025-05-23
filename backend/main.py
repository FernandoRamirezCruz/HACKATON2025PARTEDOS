from fastapi import FastAPI
from fastapi.responses import  StreamingResponse
from fastapi.templating import Jinja2Templates
from facial import generate_facial_video
from manos import generate_hand_video

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuración CORS para conectar con el frontend (Vue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Ajusta según el puerto de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importa tus routers
from facial import generate_facial_video
from manos import generate_hand_video

@app.get("/facial")
async def facial():
    return StreamingResponse(generate_facial_video(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/manos")
async def manos():
    return StreamingResponse(generate_hand_video(), media_type="multipart/x-mixed-replace; boundary=frame")

# Monta el frontend construido (solo para producción)
app.mount("/", StaticFiles(directory="../frontend/", html=True), name="frontend")