# ⚛️ Proyecto Final — Clasificador SEM Multi-Agente

Sistema de Inteligencia Artificial para Clasificación y Análisis de Imágenes de Microscopía Electrónica de Barrido (SEM) de Nanomateriales.

Implementa un pipeline multi-agente basado en **ResNet-18** (Transfer Learning), **Grad-CAM** (interpretabilidad), **LangGraph** (orquestación) y **ChromaDB** (RAG), expuesto como una **API REST con FastAPI**.

---

## 🎯 Objetivo

Clasificar automáticamente imágenes SEM en dos categorías:
- **Nanopartículas (0D)** — estructuras esféricas/redondeadas  
- **Nanohilos (1D)** — estructuras elongadas lineales

Y generar un **reporte científico automatizado** usando un sistema multi-agente con LLM.

---

## 📊 Métricas del Modelo

| Métrica | Valor |
|---------|-------|
| **Accuracy** | 97.74 % |
| **F1-Score** | 97.74 % |
| **AUC-ROC** | 99.82 % |
| **Precision** | 97.74 % |
| **Recall** | 97.74 % |
| Dataset | NFFA-EUROPE SEM Dataset |
| Imágenes de test | 1 062 |
| Errores | 24 / 1 062 |

---

## 🗂️ Estructura del Proyecto

```
Proyecto final/
├── notebooks/
│   ├── 01_dataset_preparation.ipynb    # Descarga, EDA, resize 224×224, split 70/15/15
│   ├── 02_model_training.ipynb         # ResNet-18 fine-tuning en 2 fases (ImageNet → SEM)
│   ├── 03_evaluation_gradcam.ipynb     # Métricas, Grad-CAM, análisis de errores
│   ├── 04_multiagent_analysis.ipynb    # LangGraph + ChromaDB + OpenRouter (4 agentes)
│   └── 05_test_agents.ipynb           # Pruebas unitarias de agentes
├── api/
│   ├── main.py                         # 🚀 FastAPI app — punto de entrada
│   ├── config.py                       # Configuración centralizada (paths, API keys, métricas)
│   ├── orchestrator.py                 # Pipeline multi-agente (5 agentes secuenciales)
│   ├── rag_utils.py                    # ChromaDB RAG para chat de seguimiento
│   └── agents/
│       ├── classifier.py               # Agente 1: ResNet-18 (clasificación)
│       ├── measurer.py                 # Agente 2: OpenCV (medición morfológica)
│       ├── visualizer.py              # Agente 3: Grad-CAM (interpretabilidad)
│       ├── scientist.py               # Agente 4: LLM (análisis científico)
│       └── reporter.py                # Agente 5: LLM (reporte final)
│   └── static/
│       └── index.html                  # Frontend web de la API
├── data/
│   ├── raw/          # ← Dataset NFFA-EUROPE original (generado por NB01, no en repo)
│   └── processed/    # ← Imágenes 224×224 RGB train/val/test (generado por NB01, no en repo)
├── models/
│   └── best_sem_classifier.pth         # ⚠️ No incluido (44 MB). Ver instrucciones abajo.
├── reports/
│   ├── model_metrics.json              # Métricas del modelo entrenado
│   ├── training_history.json           # Historial de pérdida y accuracy por época
│   ├── dataset_config.json             # Configuración del dataset
│   ├── multiagent_report.md            # Reporte de ejemplo generado por NB04
│   └── test_agent_report.md           # Reporte de prueba de agentes
├── requirements.txt                    # Dependencias del proyecto
├── CONTRIBUTING.md                     # Protocolo de actualización y contribución
└── CHANGELOG.md                        # Historial de cambios
```

---

## 🌐 API — Endpoint

### 🔗 URL pública (Render)

```
https://sem-analyzer-api.onrender.com
```

> ⚠️ La primera carga puede tardar ~30s (cold start en plan gratuito de Render).

### URL local (desarrollo)

```
http://localhost:8000
```

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Frontend web (interfaz de análisis) |
| `GET` | `/api/health` | Health check del sistema |
| `GET` | `/api/model-info` | Información del modelo y métricas |
| `POST` | `/api/analyze` | **Análisis completo** de imagen SEM |
| `POST` | `/api/chat` | Chat de seguimiento con RAG |
| `GET` | `/api/sample-images` | Lista imágenes de prueba disponibles |
| `GET` | `/docs` | Documentación interactiva Swagger UI |
| `GET` | `/redoc` | Documentación ReDoc |

### Ejemplo de uso — POST /api/analyze

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@mi_imagen_sem.png" \
  -F "compound=Au"
```

**Respuesta JSON:**
```json
{
  "status": "completed",
  "classification": {
    "label": "Nanopartículas (0D)",
    "predicted_class": "nanoparticles",
    "confidence": 0.9987,
    "probabilities": { "nanoparticles": 0.9987, "nanowires": 0.0013 }
  },
  "measurements": {
    "statistics": {
      "count": 42,
      "diameter_mean_nm": 18.3,
      "diameter_std_nm": 4.1,
      "aspect_ratio_mean": 1.12,
      "circularity_mean": 0.891
    }
  },
  "visualization": {
    "original_base64": "...",
    "heatmap_base64": "...",
    "overlay_base64": "..."
  },
  "scientific_analysis": { "scientific_analysis": "..." },
  "report": "# Reporte Científico\n..."
}
```

---

## 🚀 Instalación y Ejecución

### 1. Requisitos previos

- Python 3.11.x
- `pip` o `conda`

### 2. Clonar el repositorio

```bash
git clone https://github.com/Diego-V-V/IA-Nano.git
cd "IA-Nano/educational_content/Proyecto final"
```

### 3. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con:

```env
OPENROUTER_API_KEY=tu_api_key_aqui
```

> Obtén tu API key gratis en [https://openrouter.ai](https://openrouter.ai)

### 5. Descargar el modelo pre-entrenado

El modelo `best_sem_classifier.pth` (44 MB) no está en el repositorio por límites de tamaño de GitHub.  
Hay dos opciones:

**Opción A — Entrenar desde cero (recomendado):**
```bash
# Ejecutar los notebooks en orden:
# 1. notebooks/01_dataset_preparation.ipynb  → genera data/processed/
# 2. notebooks/02_model_training.ipynb       → genera models/best_sem_classifier.pth
```

**Opción B — Descargar el modelo entrenado:**
> El modelo entrenado puede descargarse desde [Google Drive (solicitar acceso al profesor)](mailto:profesor@universidad.edu)  
> Colocarlo en: `models/best_sem_classifier.pth`

### 6. Iniciar la API

```bash
cd api
python main.py
```

O con uvicorn directamente:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Abrir el frontend

Navegar a: **http://localhost:8000**

O explorar la documentación interactiva en: **http://localhost:8000/docs**

---

## 🤖 Arquitectura Multi-Agente

```
Imagen SEM
    │
    ▼
┌──────────────────┐
│ Agente 1         │  ResNet-18 fine-tuned
│ Clasificador     │→ Clase + Confianza + Probabilidades
└──────────────────┘
    │
    ▼
┌──────────────────┐
│ Agente 2         │  OpenCV + scikit-image
│ Medidor          │→ Conteo, diámetros (nm), aspect ratio, circularidad
└──────────────────┘
    │
    ▼
┌──────────────────┐
│ Agente 3         │  Grad-CAM (layer4[-1])
│ Visualizador     │→ Heatmap + Overlay de activaciones
└──────────────────┘
    │
    ▼
┌──────────────────┐
│ Agente 4         │  LLM via OpenRouter
│ Científico       │→ Interpretación científica contextualizada
└──────────────────┘
    │
    ▼
┌──────────────────┐
│ Agente 5         │  LLM via OpenRouter
│ Reportero        │→ Reporte científico Markdown completo
└──────────────────┘
    │
    ▼
Reporte Final + Chat RAG (ChromaDB)
```

---

## 📚 Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Deep Learning | PyTorch | ≥2.0.0 |
| Transfer Learning | torchvision (ResNet-18) | ≥0.15.0 |
| Interpretabilidad | Grad-CAM (implementación custom) | — |
| Orquestación multi-agente | LangGraph | 0.2.56 |
| Framework LLM | LangChain | 0.3.25 |
| Proveedor LLM | OpenRouter | — |
| Modelo LLM principal | `google/gemini-2.5-flash` | — |
| Vector Store (RAG) | ChromaDB | ≥0.4.0 |
| API REST | FastAPI | ≥0.115.0 |
| Servidor ASGI | Uvicorn | ≥0.30.0 |
| Dataset | NFFA-EUROPE SEM Dataset (Modarres et al., 2017) | — |
| Python | CPython | 3.11.x |

---

## 📋 Notebooks — Orden de Ejecución

| # | Notebook | Descripción | Outputs |
|---|----------|-------------|---------|
| 1 | `01_dataset_preparation.ipynb` | Descarga dataset, EDA, resize, split | `data/processed/`, `reports/dataset_config.json` |
| 2 | `02_model_training.ipynb` | Fine-tuning ResNet-18 en 2 fases | `models/best_sem_classifier.pth`, `reports/training_history.json` |
| 3 | `03_evaluation_gradcam.ipynb` | Métricas, matriz de confusión, Grad-CAM | `reports/model_metrics.json`, `reports/*.png` |
| 4 | `04_multiagent_analysis.ipynb` | Pipeline 4-agente LangGraph | `reports/multiagent_report.md` |
| 5 | `05_test_agents.ipynb` | Pruebas de agentes API | `reports/test_agent_report.md` |

---

## 📄 Referencia del Dataset

Modarres, M. H., et al. (2017). *Neural network for nanoscience scanning electron microscope image recognition*. **Scientific Reports**, 7(1), 13282. https://doi.org/10.1038/s41598-017-13565-z

Dataset disponible en: [NFFA-EUROPE](https://www.nffa.eu/apply/data-policy/nanoscience-foundry-and-fine-analysis/)

---

## 📝 Licencia

MIT License — Ver [LICENSE](../../LICENSE) en la raíz del repositorio.
