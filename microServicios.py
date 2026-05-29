import os
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

PUERTO = int(os.getenv("PORT", 8000))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

from grafico import (
    headless_usuarios_por_curso,
    headless_cursos_mas_populares,
    pull_usuarios_por_curso,
    pull_cursos_mas_populares,
    analizar_usuarios,
    analizar_cursos,
)

app = FastAPI(title="Motor Analítico Educativo Privado - Nuevas Tecnologías")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
def estado_servidor():
    return {"status": "online", "mensaje": "Servidor corriendo exitosamente en conjunto"}

# ════════════════════════════════════════════════════════
# ENDPOINTS DE TEXTO / ANÁLISIS
# ════════════════════════════════════════════════════════

@app.get("/api/analisis/usuarios")
def obtener_analisis_usuarios():
    return analizar_usuarios()

@app.get("/api/analisis/cursos")
def obtener_analisis_cursos():
    return analizar_cursos()

# ════════════════════════════════════════════════════════
# ENDPOINTS HEADLESS  →  JSON (Gráficas en Base64)
# ════════════════════════════════════════════════════════

@app.get("/api/graficos/headless/usuarios-por-curso")
def headless_ep_usuarios_por_curso():
    return headless_usuarios_por_curso()

@app.get("/api/graficos/headless/cursos-mas-populares")
def headless_ep_cursos_mas_populares(top: int = 5):
    return headless_cursos_mas_populares(top)

# ════════════════════════════════════════════════════════
# ENDPOINTS PULL  →  image/png
# ════════════════════════════════════════════════════════

@app.get("/api/graficos/pull/usuarios-por-curso", response_class=Response)
def pull_ep_usuarios_por_curso():
    return Response(content=pull_usuarios_por_curso(), media_type="image/png")

@app.get("/api/graficos/pull/cursos-mas-populares", response_class=Response)
def pull_ep_cursos_mas_populares(top: int = 5):
    return Response(content=pull_cursos_mas_populares(top), media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("microServicios:app", host="0.0.0.0", port=PUERTO, reload=True)
