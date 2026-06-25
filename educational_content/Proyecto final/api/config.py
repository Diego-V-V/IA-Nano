"""
Configuración centralizada del Sistema Multi-Agente SEM.
Carga paths, API keys, constantes del modelo y métricas.
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# ── Paths ────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Proyecto final/
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
DATA_DIR = PROJECT_ROOT / "data"
STATIC_DIR = Path(__file__).resolve().parent / "static"

MODEL_PATH = MODELS_DIR / "best_sem_classifier.pth"

# ── Cargar .env ──────────────────────────────────────────────
for _p in [Path(__file__).parent, PROJECT_ROOT, PROJECT_ROOT.parent,
           PROJECT_ROOT.parent.parent]:
    _env = _p / ".env"
    if _env.exists():
        load_dotenv(str(_env), override=True)
        break

# ── API Keys ─────────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Fallback: leer del notebook 05 si no hay env var
if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = "TU_OPENROUTER_API_KEY"

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_HEADERS = {
    "HTTP-Referer": "https://github.com/antigravity-nano",
    "X-Title": "SEM Particle Analyzer",
}

MODELS_FALLBACK = [
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
    "anthropic/claude-3-haiku",
]

# ── Modelo ResNet-18 ─────────────────────────────────────────
IMAGE_SIZE = 224
NUM_CLASSES = 2
CLASSES = ["nanoparticles", "nanowires"]
CLASS_LABELS = {
    "nanoparticles": "Nanopartículas (0D)",
    "nanowires": "Nanohilos (1D)",
}

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# ── Métricas del modelo (pre-calculadas) ─────────────────────
_metrics_path = REPORTS_DIR / "model_metrics.json"
if _metrics_path.exists():
    with open(_metrics_path, encoding="utf-8") as f:
        MODEL_METRICS = json.load(f)
else:
    MODEL_METRICS = {
        "accuracy": 0.9907, "f1_score": 0.9903, "auc_roc": 0.9943,
        "precision": 0.9907, "recall": 0.9907,
        "n_errors": 1, "test_size": 107, "error_rate": 0.0093,
        "classes": CLASSES,
        "gradcam_interpretation": (
            "Grad-CAM highlights edge features and aspect ratios. "
            "Nanoparticles activate on rounded/spherical boundaries. "
            "Nanowires activate on elongated linear structures."
        ),
    }
