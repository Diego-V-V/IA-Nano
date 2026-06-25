# Contribuir al Proyecto Final — Clasificador SEM Multi-Agente

## Descripción del proyecto

Este proyecto implementa un clasificador de imágenes SEM (nanopartículas 0D vs nanohilos 1D)
con un sistema multi-agente para análisis científico automatizado. Está dividido en 4 notebooks
secuenciales y un directorio de soporte.

---

## Estructura del proyecto

```
Proyecto final/
├── notebooks/
│   ├── 01_dataset_preparation.ipynb   # Descarga, EDA, split, DataLoaders
│   ├── 02_model_training.ipynb        # ResNet-18, fine-tuning en 2 fases
│   ├── 03_evaluation_gradcam.ipynb    # Métricas, Grad-CAM, análisis de errores
│   └── 04_multiagent_analysis.ipynb   # LangGraph + ChromaDB + OpenRouter
├── data/
│   ├── raw/          # Dataset NFFA-EUROPE original (Particles/, Nanowires/)
│   └── processed/    # Imágenes 224×224 RGB en train/val/test
├── models/           # best_sem_classifier.pth
├── reports/          # dataset_config.json, training_history.json, model_metrics.json
├── api/              # FastAPI endpoint — Sistema multi-agente (5 agentes)
│   ├── main.py       # App principal — POST /api/analyze, GET /api/health, etc.
│   ├── orchestrator.py  # Coordinador del pipeline
│   ├── config.py     # Configuración centralizada
│   ├── rag_utils.py  # ChromaDB RAG
│   ├── agents/       # Agentes individuales (classifier, measurer, visualizer, scientist, reporter)
│   └── static/
│       └── index.html  # Frontend web
│                     # URL local: http://localhost:8000
│                     # Docs Swagger: http://localhost:8000/docs
├── requirements.txt
├── CONTRIBUTING.md   # ← Este archivo
└── CHANGELOG.md
```

---

## Proceso de actualización

### 1. Actualizar dependencias de PyTorch/ML

```bash
# Verificar versiones actuales
pip list | grep -E "torch|torchvision|scikit-learn"

# Actualizar
pip install --upgrade torch torchvision

# Verificar que no se rompió nada
python -c "from torchvision import models; m = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1); print('OK')"
```

**Puntos de ruptura conocidos:**
- `models.ResNet18_Weights.IMAGENET1K_V1` reemplazó a `pretrained=True` en torchvision ≥0.13
- Si torchvision depreca `ResNet18_Weights`, buscar el nuevo enum en la documentación oficial

### 2. Actualizar dependencias de LangChain/LangGraph

```bash
# Verificar versiones actuales
pip list | grep -E "langchain|langgraph|chromadb"

# Actualizar con cuidado (LangChain rompe APIs frecuentemente)
pip install --upgrade langchain langchain-core langchain-openai langgraph
```

**Puntos de ruptura conocidos:**
- `create_tool_calling_agent` puede cambiar de firma entre versiones menores de LangChain
- `MessagesPlaceholder(variable_name="agent_scratchpad")` puede renombrarse
- `StateGraph` de LangGraph: verificar que `add_conditional_edges` siga existiendo
- `chromadb.EphemeralClient()` → en versiones futuras podría renombrarse a `Client(ephemeral=True)`

### 3. Actualizar modelos LLM en OpenRouter

Los modelos de OpenRouter cambian frecuentemente. Para actualizar:

1. Verificar modelos disponibles en https://openrouter.ai/models
2. Actualizar la lista `MODELS_FALLBACK` en `04_multiagent_analysis.ipynb`
3. Actualizar la variable de entorno `OPENROUTER_MODEL` si cambió el modelo por defecto
4. Probar con un invoke simple antes de ejecutar el pipeline completo

**Modelos recomendados (Mayo 2026):**
| Modelo | ID OpenRouter | Costo/1M tokens |
|--------|--------------|-----------------|
| Gemini 2.5 Flash | `google/gemini-2.5-flash` | ~$0.15 |
| GPT-4o Mini | `openai/gpt-4o-mini` | ~$0.30 |
| Claude 3 Haiku | `anthropic/claude-3-haiku` | ~$0.25 |

---

## Protocolo de calidad por notebook

Cada notebook debe cumplir:

1. **Warm-up**: Primera celda verifica dependencias e instala las faltantes
2. **Teoría antes del código**: Cada sección técnica tiene una celda Markdown previa explicando el concepto
3. **Output documentado**: Cada celda de código termina con `print()` descriptivo
4. **Conexión explícita**: Última celda indica `→ Continuar con: XX_nombre.ipynb`
5. **Artefactos guardados**: Cada notebook guarda sus outputs en `reports/` o `models/`

---

## Cómo contribuir

### Reportar un error
1. Especificar qué notebook y qué celda falló
2. Incluir el traceback completo
3. Indicar: versiones de Python, PyTorch, LangChain (`pip list`)
4. Indicar: sistema operativo y si tiene GPU disponible

### Proponer una mejora
1. Describir qué se quiere mejorar y por qué
2. Indicar si afecta una notebook específica o el pipeline completo
3. Si es un cambio de arquitectura (e.g., cambiar ResNet-18 por otro modelo), justificar con métricas

### Agregar una nueva notebook
1. Seguir la convención de nombres: `XX_nombre_descriptivo.ipynb`
2. Cumplir el protocolo de calidad (ver arriba)
3. Actualizar este CONTRIBUTING.md con la nueva notebook en la estructura
4. Actualizar CHANGELOG.md con la fecha y descripción del cambio

---

## Convenciones de código

- **Python**: PEP 8, type hints en funciones públicas
- **Notebooks**: Una sección = un concepto. No mezclar conceptos en una celda
- **Variables**: `UPPER_CASE` para constantes, `lower_case` para variables
- **Paths**: Usar `pathlib.Path`, no strings hardcodeados
- **Modelos LLM**: Siempre via `OPENROUTER_API_KEY` en `.env`, nunca hardcodeada
