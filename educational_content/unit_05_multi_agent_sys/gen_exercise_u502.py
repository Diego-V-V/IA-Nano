# -*- coding: utf-8 -*-
"""Append the Extension Exercise (SEM Technical Report Generator) to U5_02."""
import json, os, uuid

NB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "U5_02_LANGCHAIN_AVANZADO_LANGGRAPH.ipynb")

with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

def md(src):
    lines = [line + "\n" for line in src.split("\n")]
    lines[-1] = lines[-1].rstrip("\n")
    return {"cell_type": "markdown", "id": str(uuid.uuid4())[:8], "metadata": {}, "source": lines}

def code(src):
    lines = [line + "\n" for line in src.split("\n")]
    lines[-1] = lines[-1].rstrip("\n")
    return {"cell_type": "code", "execution_count": None, "id": str(uuid.uuid4())[:8], "metadata": {}, "outputs": [], "source": lines}

cells = [
    md("""---
## Ejercicio de Extensión: Generador de Reportes Técnicos SEM

Construimos un sistema de generación de reportes técnicos para el **Proyecto Final (Clasificador SEM)** usando LangGraph, implementando los 6 requisitos del ejercicio:

1. **Nodo de análisis** del tema solicitado
2. **Nodo de búsqueda** de información (mock con métricas reales del modelo)
3. **Nodo de redacción** del reporte
4. **Nodo de revisión** de calidad con ciclo de corrección (max 2 intentos)
5. **Nodo de human-in-the-loop** para aprobación antes de "publicar"
6. **Checkpointing con SQLite** para que el reporte persista entre sesiones

```
START → analyze_topic → search_info → write_report → review_quality
                                                          │
                                              ┌───────────┤
                                              │ (max 2)   │
                                              ▼           │
                                         write_report ◄───┘
                                              │
                                              ▼ (aceptado)
                                      human_approval ──► publish → END
```"""),

    code("""# ============================================================
# EJERCICIO DE EXTENSIÓN: Generador de Reportes SEM con LangGraph
# ============================================================
# Requisitos: langgraph, langchain-openai, langgraph-checkpoint-sqlite
# ============================================================

import os, json
from typing import TypedDict, Literal, Annotated
from dotenv import load_dotenv
load_dotenv(override=True)

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# --- LLM Setup (OpenRouter) ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODELS = ["openai/gpt-4o-mini", "google/gemini-2.5-flash", "anthropic/claude-3-haiku"]

llm_report = None
for m in MODELS:
    try:
        _c = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY, model=m, temperature=0,
            default_headers={
                "HTTP-Referer": "https://github.com/antigravity-nano",
                "X-Title": "SEM Report Generator",
            },
        )
        _c.invoke("OK")
        llm_report = _c
        print(f"LLM conectado: {m}")
        break
    except Exception as e:
        print(f"  [!] {m}: {e}")

if llm_report is None:
    raise RuntimeError("No se pudo conectar a ningun modelo.")

print("Setup completo.")"""),

    md("""### Paso 1: Definir el Estado del Grafo

El estado contiene todas las variables que fluyen entre los nodos del pipeline de reportes."""),

    code("""# ============================================================
# 1. ESTADO DEL GRAFO
# ============================================================

class ReportState(TypedDict):
    topic: str                # Tema solicitado por el usuario
    analysis: str             # Resultado del análisis del tema
    search_results: str       # Información recuperada (mock con datos reales)
    draft: str                # Borrador del reporte
    review_feedback: str      # Feedback de la revisión de calidad
    is_approved: bool         # ¿El revisor aprobó el draft?
    human_decision: str       # Decisión del humano: "aprobar" o "rechazar"
    final_report: str         # Reporte final publicado
    revision_count: int       # Contador de revisiones (max 2)

print("Estado ReportState definido con 9 campos.")"""),

    md("""### Paso 2: Definir los Nodos del Grafo

Cada nodo es una función `(state) -> dict` que lee el estado y devuelve las keys a actualizar."""),

    code("""# ============================================================
# 2. NODOS DEL GRAFO
# ============================================================

# --- Nodo 1: Análisis del tema ---
def analyze_topic(state: ReportState) -> dict:
    \"\"\"Analiza el tema solicitado y extrae los puntos clave a cubrir.\"\"\"
    prompt = (
        f"Eres un científico experto en microscopía SEM y ML. "
        f"Analiza el siguiente tema y lista 3-4 puntos clave que un reporte técnico debe cubrir:\\n\\n"
        f"Tema: {state['topic']}"
    )
    analysis = llm_report.invoke(prompt).content
    print(f"  [analyze_topic] Puntos clave identificados.")
    return {"analysis": analysis}


# --- Nodo 2: Búsqueda de información (mock con datos reales) ---
def search_info(state: ReportState) -> dict:
    \"\"\"Recupera información relevante del proyecto (métricas, Grad-CAM, dataset).\"\"\"
    # Mock: datos reales del modelo ResNet-18 SEM
    search_data = \"\"\"
=== DATOS DEL MODELO ===
Modelo: ResNet-18 (ImageNet → SEM fine-tuned)
Tarea: Clasificación binaria - Nanoparticles (0D) vs Nanowires (1D)
Dataset: NFFA-EUROPE SEM Dataset
Test size: 107 imágenes

=== MÉTRICAS ===
- Accuracy: 99.07% (106/107 correctas)
- F1-Score: 0.9903
- Precision: 0.9907
- Recall: 0.9907
- AUC-ROC: 0.9943
- Errores: 1 de 107 imágenes (1 nanopartícula clasificada como nanohilo)
- Matriz de confusión: [[6, 1], [0, 100]]

=== GRAD-CAM ===
- Capa objetivo: layer4[-1]
- Nanopartículas: Alta activación en bordes esféricos y contornos redondeados
- Nanohilos: Fuerte activación en estructuras elongadas y lineales
- Interpretación: El modelo detecta correctamente las features morfológicas clave
\"\"\"
    print(f"  [search_info] Datos del modelo recuperados.")
    return {"search_results": search_data}


# --- Nodo 3: Redacción del reporte ---
def write_report(state: ReportState) -> dict:
    \"\"\"Genera un borrador del reporte técnico.\"\"\"
    revision_count = state.get("revision_count", 0)
    feedback = state.get("review_feedback", "")

    if feedback and revision_count > 0:
        prompt = (
            f"Eres un redactor científico. Mejora el siguiente borrador de reporte técnico "
            f"basándote en el feedback de revisión.\\n\\n"
            f"FEEDBACK: {feedback}\\n\\n"
            f"BORRADOR ANTERIOR:\\n{state['draft']}\\n\\n"
            f"DATOS DISPONIBLES:\\n{state['search_results']}\\n\\n"
            f"Genera el borrador mejorado en formato Markdown."
        )
    else:
        prompt = (
            f"Eres un redactor científico. Escribe un reporte técnico conciso (300-500 palabras) "
            f"sobre el siguiente tema, usando los datos proporcionados.\\n\\n"
            f"TEMA: {state['topic']}\\n\\n"
            f"ANÁLISIS:\\n{state['analysis']}\\n\\n"
            f"DATOS:\\n{state['search_results']}\\n\\n"
            f"El reporte debe incluir: Resumen, Metodología, Resultados, Interpretación de Grad-CAM, "
            f"y Conclusiones. Formato Markdown."
        )

    draft = llm_report.invoke(prompt).content
    print(f"  [write_report] Borrador generado (revisión #{revision_count + 1})")
    return {"draft": draft, "revision_count": revision_count + 1}


# --- Nodo 4: Revisión de calidad ---
def review_quality(state: ReportState) -> dict:
    \"\"\"Evalúa la calidad del reporte y decide si necesita corrección.\"\"\"
    prompt = (
        f"Eres un revisor científico exigente. Evalúa este reporte técnico:\\n\\n"
        f"{state['draft']}\\n\\n"
        f"Criterios: 1) ¿Incluye métricas numéricas precisas? 2) ¿Interpreta Grad-CAM? "
        f"3) ¿Tiene estructura clara (secciones)? 4) ¿Las conclusiones son coherentes?\\n\\n"
        f"Responde EXACTAMENTE con una de estas opciones:\\n"
        f"APROBADO - si cumple los 4 criterios\\n"
        f"RECHAZADO: [motivo específico] - si falla en algún criterio"
    )
    review = llm_report.invoke(prompt).content.strip()
    is_approved = "APROBADO" in review.upper() and "RECHAZADO" not in review.upper()
    feedback = "" if is_approved else review

    status = "APROBADO" if is_approved else "RECHAZADO"
    print(f"  [review_quality] Resultado: {status} (revisión #{state.get('revision_count', 0)})")
    if not is_approved:
        print(f"  Feedback: {feedback[:100]}...")
    return {"is_approved": is_approved, "review_feedback": feedback}


# --- Nodo 5: Human-in-the-loop (simulado) ---
def human_approval(state: ReportState) -> dict:
    \"\"\"Simula la aprobación humana. En producción, esto sería un breakpoint real.\"\"\"
    # En este ejercicio simulamos la aprobación automática
    print(f"  [human_approval] Reporte presentado para aprobación humana.")
    print(f"  [human_approval] >>> APROBADO por el revisor humano (simulado)")
    return {"human_decision": "aprobar"}


# --- Nodo 6: Publicación ---
def publish_report(state: ReportState) -> dict:
    \"\"\"Publica el reporte final.\"\"\"
    print(f"  [publish] Reporte publicado exitosamente.")
    return {"final_report": state["draft"]}

print("6 nodos definidos: analyze_topic, search_info, write_report, review_quality, human_approval, publish_report")"""),

    md("""### Paso 3: Construir y Compilar el Grafo con SQLite Checkpointing"""),

    code("""# ============================================================
# 3. CONSTRUCCIÓN DEL GRAFO + SQLITE CHECKPOINTING
# ============================================================
import shutil

# Routing: después de la revisión, ¿corregir o avanzar?
def route_after_review(state: ReportState) -> Literal["write_report", "human_approval"]:
    \"\"\"Decide si el reporte necesita corrección o está listo para aprobación humana.\"\"\"
    if state["is_approved"]:
        return "human_approval"
    elif state.get("revision_count", 0) >= 2:
        print("  [routing] Max revisiones alcanzado (2). Enviando a aprobación humana.")
        return "human_approval"
    else:
        print("  [routing] Reporte rechazado. Enviando a corrección...")
        return "write_report"

# Construir el grafo
builder = StateGraph(ReportState)

# Agregar nodos
builder.add_node("analyze_topic", analyze_topic)
builder.add_node("search_info", search_info)
builder.add_node("write_report", write_report)
builder.add_node("review_quality", review_quality)
builder.add_node("human_approval", human_approval)
builder.add_node("publish_report", publish_report)

# Agregar aristas
builder.add_edge(START, "analyze_topic")
builder.add_edge("analyze_topic", "search_info")
builder.add_edge("search_info", "write_report")
builder.add_edge("write_report", "review_quality")

# Arista condicional: review → write_report (corrección) o human_approval
builder.add_conditional_edges(
    "review_quality",
    route_after_review,
    {"write_report": "write_report", "human_approval": "human_approval"},
)

builder.add_edge("human_approval", "publish_report")
builder.add_edge("publish_report", END)

# --- SQLite Checkpointing ---
SQLITE_PATH = "./u5_02_report_checkpoint.db"

# Limpiar checkpoint anterior si existe
if os.path.exists(SQLITE_PATH):
    os.remove(SQLITE_PATH)
    print(f"Checkpoint anterior eliminado: {SQLITE_PATH}")

from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
conn = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn)

# Compilar con checkpointing
report_graph = builder.compile(checkpointer=checkpointer)
print("Grafo compilado con SQLite checkpointing.")
print(f"  Checkpoint DB: {SQLITE_PATH}")"""),

    md("""### Paso 4: Visualizar el Grafo"""),

    code("""# ============================================================
# 4. VISUALIZACIÓN DEL GRAFO
# ============================================================
try:
    from IPython.display import Image, display
    display(Image(report_graph.get_graph().draw_mermaid_png()))
    print("Grafo visualizado.")
except Exception:
    mermaid_code = report_graph.get_graph().draw_mermaid()
    print("Diagrama Mermaid del grafo:")
    print(mermaid_code)"""),

    md("""### Paso 5: Ejecutar el Pipeline Completo

Ejecutamos el grafo con un tema del Proyecto Final. El pipeline recorrerá todos los nodos y el estado persistirá en SQLite."""),

    code("""# ============================================================
# 5. EJECUCIÓN DEL PIPELINE
# ============================================================

TOPIC = (
    "Evaluación del modelo ResNet-18 para clasificación binaria "
    "de micrografías SEM: nanopartículas vs nanohilos del dataset NFFA-EUROPE"
)

print("=" * 70)
print("PIPELINE DE GENERACIÓN DE REPORTES SEM")
print("=" * 70)
print(f"Tema: {TOPIC}")
print("-" * 70)

# Configuración del thread (permite checkpointing)
config = {"configurable": {"thread_id": "sem_report_001"}}

# Ejecutar el grafo
result = report_graph.invoke(
    {
        "topic": TOPIC,
        "analysis": "",
        "search_results": "",
        "draft": "",
        "review_feedback": "",
        "is_approved": False,
        "human_decision": "",
        "final_report": "",
        "revision_count": 0,
    },
    config=config,
)

print("\\n" + "=" * 70)
print("REPORTE FINAL PUBLICADO")
print("=" * 70)
print(result["final_report"])
print("\\n" + "-" * 70)
print(f"Revisiones realizadas: {result['revision_count']}")
print(f"Estado de aprobación: {result['human_decision']}")"""),

    md("""### Paso 6: Verificar Persistencia del Checkpoint

Demostramos que el estado persiste en SQLite — el reporte puede recuperarse entre sesiones."""),

    code("""# ============================================================
# 6. VERIFICAR PERSISTENCIA DEL CHECKPOINT
# ============================================================

# Consultar el estado guardado en SQLite
checkpoint_state = report_graph.get_state(config)

print("=== ESTADO RECUPERADO DEL CHECKPOINT SQLite ===")
print(f"Thread ID: sem_report_001")
print(f"Revisiones: {checkpoint_state.values.get('revision_count', 'N/A')}")
print(f"Aprobado por revisor: {checkpoint_state.values.get('is_approved', 'N/A')}")
print(f"Decisión humana: {checkpoint_state.values.get('human_decision', 'N/A')}")
print(f"Longitud del reporte final: {len(checkpoint_state.values.get('final_report', ''))} caracteres")
print(f"\\nEl reporte persiste en: {SQLITE_PATH}")
print("Si reiniciaras el kernel, podrías recuperar este estado exacto.")

# Cerrar la conexión
conn.close()
print("\\nConexión SQLite cerrada.")"""),

    md("""### Resumen del Ejercicio

| Requisito | Implementación | Estado |
|-----------|---------------|--------|
| 1. Nodo de análisis | `analyze_topic` — LLM analiza el tema y extrae puntos clave | ✅ |
| 2. Nodo de búsqueda | `search_info` — Mock con métricas reales del ResNet-18 | ✅ |
| 3. Nodo de redacción | `write_report` — LLM genera reporte Markdown estructurado | ✅ |
| 4. Revisión con ciclo | `review_quality` + `route_after_review` — max 2 correcciones | ✅ |
| 5. Human-in-the-loop | `human_approval` — simulado (en producción: breakpoint real) | ✅ |
| 6. SQLite checkpoint | `SqliteSaver` con `u5_02_report_checkpoint.db` | ✅ |

**Contexto del Proyecto Final**: Todo el pipeline está contextualizado al clasificador SEM ResNet-18, usando las métricas reales (Accuracy 99.07%, AUC-ROC 0.9943) y la interpretación de Grad-CAM del modelo entrenado."""),
]

nb["cells"].extend(cells)

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Ejercicio de extensión insertado en U5_02 ({len(cells)} celdas).")
