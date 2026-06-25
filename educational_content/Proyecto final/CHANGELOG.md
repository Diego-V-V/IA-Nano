# Changelog — Proyecto Final: Clasificador SEM Multi-Agente

Todas las actualizaciones notables a este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.0.0] — 2026-05-13

### Agregado
- **NB01 — Dataset Preparation**: Descarga automatizada del NFFA-EUROPE SEM Dataset
  (categorías Particles y Nanowires), EDA, resize a 224×224, split 70/15/15
- **NB02 — Model Training**: Transfer learning con ResNet-18 (ImageNet pretrained),
  entrenamiento en 2 fases (FC-only 10 epochs + fine-tuning completo 10 epochs)
- **NB03 — Evaluation & Grad-CAM**: Evaluación en test set (accuracy, F1, AUC-ROC),
  matriz de confusión, Grad-CAM sobre layer4[-1], análisis de errores
- **NB04 — Multi-Agent Analysis**: Sistema de 4 agentes (Analyst, Scientist, Writer,
  Reviewer) orquestados con LangGraph StateGraph, tools con arXiv y ChromaDB,
  ciclo de revisión condicional (max 3 iteraciones)
- `requirements.txt` con dependencias pinneadas
- `CONTRIBUTING.md` con protocolo de actualización y contribución
- `CHANGELOG.md` (este archivo)

### Stack tecnológico — v1.0.0
| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Deep Learning | PyTorch | ≥2.0.0 |
| Transfer Learning | torchvision (ResNet-18) | ≥0.15.0 |
| Weights | `ResNet18_Weights.IMAGENET1K_V1` | — |
| Agentes | LangChain | 0.3.25 |
| Orquestación | LangGraph | 0.2.56 |
| LLM Provider | OpenRouter | — |
| Modelo LLM primario | `google/gemini-2.5-flash` | — |
| Modelo LLM fallback 1 | `openai/gpt-4o-mini` | — |
| Modelo LLM fallback 2 | `anthropic/claude-3-haiku` | — |
| Vector Store | ChromaDB (EphemeralClient) | ≥0.4.0 |
| Dataset | NFFA-EUROPE SEM Dataset | Modarres et al., 2017 |
| Python | CPython | 3.11.x |

### Costos estimados de ejecución
| Notebook | Recurso | Costo estimado |
|----------|---------|----------------|
| NB01 | CPU + descarga ~200MB | $0.00 (local) |
| NB02 | CPU/GPU, ~20 min (CPU) / ~5 min (GPU) | $0.00 (local) |
| NB03 | CPU, ~2 min | $0.00 (local) |
| NB04 | OpenRouter API, ~15,000-25,000 tokens | ~$0.003-$0.005 (Gemini Flash) |
| **Total** | | **< $0.01 por ejecución completa** |

---

## Guía de actualización para futuras versiones

### Al actualizar LangChain
- [ ] Verificar que `create_tool_calling_agent` no cambió de firma
- [ ] Verificar que `ChatPromptTemplate.from_messages` sigue funcionando
- [ ] Verificar imports: `from langchain_openai import ChatOpenAI`
- [ ] Ejecutar NB04 completa y verificar que el grafo produce reporte

### Al actualizar LangGraph
- [ ] Verificar que `StateGraph`, `START`, `END` siguen en `langgraph.graph`
- [ ] Verificar que `add_conditional_edges` sigue existiendo
- [ ] Verificar que `add_messages` sigue en `langgraph.graph.message`

### Al actualizar PyTorch/torchvision
- [ ] Verificar que `ResNet18_Weights.IMAGENET1K_V1` no fue deprecado
- [ ] Verificar que `models.resnet18(weights=...)` sigue siendo la API
- [ ] Re-entrenar modelo si las weights cambiaron (poco probable)

### Al cambiar modelo LLM por defecto
- [ ] Actualizar `OPENROUTER_MODEL` en NB04
- [ ] Actualizar `MODELS_FALLBACK` con alternativas vigentes
- [ ] Verificar precios actualizados en https://openrouter.ai/models
- [ ] Actualizar la tabla de costos en este CHANGELOG
