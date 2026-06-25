"""
FastAPI — Sistema Unificado Multi-Agente para Análisis SEM.
Endpoints para subir imágenes SEM y obtener análisis completo.
"""
import sys
import os

# Asegurar que el directorio api/ está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import time
import json
from pathlib import Path

from config import MODEL_METRICS, STATIC_DIR, PROJECT_ROOT
from orchestrator import get_pipeline
from rag_utils import query_rag

# Estado global para el chat: almacena el último reporte generado
_last_analysis_context = {"report": "", "compound": "", "classification": "", "measurements": ""}

# ── App FastAPI ──────────────────────────────────────────────
app = FastAPI(
    title="SEM Multi-Agent Analyzer",
    description=(
        "Sistema Multi-Agente para Clasificación y Medición "
        "de Nanopartículas en imágenes SEM"
    ),
    version="1.0.0",
)

# Habilitar CORS para evitar errores de fetch locales (como file:// o localhost cruzado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Montar archivos estáticos ────────────────────────────────
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Endpoints ────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    """Sirve el frontend principal."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>SEM Analyzer</h1><p>index.html no encontrado.</p>")


@app.get("/api/health")
async def health():
    """Health check del sistema."""
    return {
        "status": "ok",
        "system": "SEM Multi-Agent Analyzer",
        "version": "1.0.0",
        "model_loaded": Path(
            PROJECT_ROOT / "models" / "best_sem_classifier.pth"
        ).exists(),
    }


@app.get("/api/model-info")
async def model_info():
    """Información del modelo y métricas pre-calculadas."""
    return {
        "model": MODEL_METRICS.get("model", "ResNet-18"),
        "task": MODEL_METRICS.get("task", "Binary SEM Classification"),
        "dataset": MODEL_METRICS.get("dataset", "NFFA-EUROPE SEM"),
        "metrics": {
            "accuracy": MODEL_METRICS.get("accuracy", 0),
            "f1_score": MODEL_METRICS.get("f1_score", 0),
            "precision": MODEL_METRICS.get("precision", 0),
            "recall": MODEL_METRICS.get("recall", 0),
            "auc_roc": MODEL_METRICS.get("auc_roc", 0),
        },
        "classes": MODEL_METRICS.get("classes", []),
        "test_size": MODEL_METRICS.get("test_size", 0),
        "gradcam_interpretation": MODEL_METRICS.get("gradcam_interpretation", ""),
    }


@app.post("/api/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    compound: str = Form("Desconocido")
):
    """
    Analiza una imagen SEM con el pipeline multi-agente completo.

    Acepta: PNG, JPG, TIFF, BMP
    Retorna: Clasificación, mediciones, Grad-CAM, análisis científico, reporte.
    """
    # Validar tipo de archivo
    allowed_types = {
        "image/png", "image/jpeg", "image/tiff", "image/bmp",
        "image/tif", "image/jpg",
    }
    content_type = file.content_type or ""
    filename = file.filename or "unknown"
    ext = Path(filename).suffix.lower()

    if content_type not in allowed_types and ext not in {
        ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp"
    }:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no soportado: {content_type}. "
                   f"Use PNG, JPG, TIFF o BMP.",
        )

    # Leer imagen
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"No se pudo leer la imagen: {e}",
        )

    # Ejecutar pipeline multi-agente
    try:
        pipeline = get_pipeline()
        results = pipeline.analyze(image, compound)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el pipeline de análisis: {e}",
        )

    # Guardar contexto del análisis para el chat
    global _last_analysis_context
    _last_analysis_context = {
        "report": results.get("report", ""),
        "compound": compound,
        "classification": str(results.get("classification", {})),
        "measurements": str(results.get("measurements", {}).get("statistics", {})),
        "scientific_analysis": results.get("scientific_analysis", {}).get("scientific_analysis", ""),
    }

    return JSONResponse(content=results)


@app.post("/api/chat")
async def chat_followup(request: dict):
    """
    Chat de seguimiento: el usuario puede hacer preguntas sobre el reporte generado.
    Usa el contexto del último análisis + RAG para responder.
    """
    from pydantic import BaseModel
    user_message = request.get("message", "").strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Mensaje vacío.")

    # Recuperar contexto RAG relevante a la pregunta
    rag_context = query_rag(user_message, n_results=2)

    # Construir prompt con contexto del último reporte
    ctx = _last_analysis_context
    prompt = f"""Eres un asistente científico experto en nanotecnología y análisis SEM.
El usuario acaba de recibir un reporte de análisis de micrografía SEM y quiere hacer seguimiento.

CONTEXTO DEL ÚLTIMO ANÁLISIS:
- Compuesto: {ctx.get('compound', 'N/A')}
- Clasificación: {ctx.get('classification', 'N/A')}
- Mediciones: {ctx.get('measurements', 'N/A')}

EXTRACTO DEL REPORTE GENERADO:
{ctx.get('scientific_analysis', 'No disponible')[:1500]}

LITERATURA CIENTÍFICA RELEVANTE (RAG — ChromaDB):
{rag_context}

PREGUNTA DEL USUARIO:
{user_message}

Responde en español de forma concisa pero científicamente precisa (150-300 palabras).
Si la pregunta se relaciona con la literatura recuperada, cita las referencias (autor, año).
Si la pregunta no tiene relación con el análisis SEM, indica amablemente que tu especialidad
es nanotecnología y análisis de micrografías."""

    # Intentar responder con LLM
    try:
        from config import (
            OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_HEADERS,
            MODELS_FALLBACK,
        )
        from langchain_openai import ChatOpenAI

        for model_id in MODELS_FALLBACK:
            try:
                llm = ChatOpenAI(
                    base_url=OPENROUTER_BASE_URL,
                    api_key=OPENROUTER_API_KEY,
                    model=model_id,
                    temperature=0.4,
                    default_headers=OPENROUTER_HEADERS,
                    max_tokens=800,
                )
                response = llm.invoke(prompt)
                return {
                    "response": response.content,
                    "model": model_id,
                    "rag_used": bool(rag_context and "Error" not in rag_context),
                }
            except Exception:
                continue

        return {"response": "No se pudo conectar al LLM. Verifica tu OPENROUTER_API_KEY.", "model": "offline", "rag_used": False}
    except ImportError:
        return {"response": "langchain_openai no está instalado.", "model": "offline", "rag_used": False}


@app.get("/api/sample-images")
async def sample_images():
    """Lista imágenes de prueba disponibles en el dataset."""
    test_dir = PROJECT_ROOT / "data" / "processed" / "test"
    samples = []

    if test_dir.exists():
        for class_dir in sorted(test_dir.iterdir()):
            if class_dir.is_dir():
                images = sorted(class_dir.glob("*.png"))[:3]
                for img_path in images:
                    samples.append({
                        "name": img_path.name,
                        "class": class_dir.name,
                        "path": str(img_path.relative_to(PROJECT_ROOT)),
                    })

    return {"samples": samples, "total": len(samples)}


# ── Main ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Iniciando SEM Multi-Agent Analyzer...")
    print("   http://localhost:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
