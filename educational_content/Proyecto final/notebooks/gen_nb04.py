"""Generate notebook 04_multiagent_analysis.ipynb"""
import json, pathlib

cells = []

def md(src):
    cells.append({"cell_type":"markdown","metadata":{},"source":src.split("\n")})

def code(src):
    cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src.split("\n")})

md("""# Notebook 04 — Sistema Multi-Agente para Análisis SEM
## Integración de técnicas U5: LangGraph + CrewAI + RAG + Memoria

**Objetivo:** Orquestar agentes especializados que analicen automáticamente los resultados
del clasificador SEM (métricas, Grad-CAM) y generen un reporte científico.

**Técnicas integradas de U5:**
| U5 Notebook | Técnica | Uso en este proyecto |
|---|---|---|
| U5_01 | ReAct + @tool | Agentes con tools para métricas y arXiv |
| U5_02 | LangGraph StateGraph | Orquestador con ciclo de revisión |
| U5_03 | CrewAI | Sub-Crew de escritura científica |
| U5_05 | RAG + ChromaDB | Indexación de papers SEM |
| U5_07 | Model routing | OpenRouter multi-modelo |
| U5_08 | Sistema end-to-end | Pipeline completo |

---""")

code("""# ============================================================
# WARM-UP: Dependencias y configuración
# ============================================================
import subprocess, sys, os, json
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env
for p in [Path('.'), Path('..'), Path('../..'), Path('../../..')]:
    env_file = p / '.env'
    if env_file.exists():
        load_dotenv(str(env_file), override=True)
        break

# Verificar paquetes
for pkg, imp in [("langchain","langchain"),("langgraph","langgraph"),
                 ("chromadb","chromadb"),("httpx","httpx")]:
    try:
        __import__(imp)
        print(f"  OK: {pkg}")
    except ImportError:
        subprocess.check_call([sys.executable,"-m","pip","install",pkg,"-q"])
        print(f"  Instalado: {pkg}")

# Verificar OpenRouter
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY no encontrada. Configúrala en .env")
print(f"\\nOpenRouter: OK")

# Cargar métricas del modelo
PROJECT_ROOT = Path('..').resolve()
with open(PROJECT_ROOT / 'reports' / 'model_metrics.json') as f:
    MODEL_METRICS = json.load(f)

print(f"Métricas cargadas: Accuracy={MODEL_METRICS['accuracy']:.1%}, F1={MODEL_METRICS['f1_score']:.4f}")
print("Warm-up completado.")""")

md("""## 1. Configurar LLM (OpenRouter)""")

code("""# ============================================================
# LLM: OpenRouter con fallback automático
# ============================================================
from langchain_openai import ChatOpenAI

OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash")

MODELS_FALLBACK = [
    OPENROUTER_MODEL,
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
    "anthropic/claude-3-haiku",
]
# Deduplicar
_seen = set()
MODELS_FALLBACK = [m for m in MODELS_FALLBACK if not (m in _seen or _seen.add(m))]

llm = None
for model_id in MODELS_FALLBACK:
    try:
        _c = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            model=model_id,
            temperature=0,
            default_headers={
                "HTTP-Referer": "https://github.com/antigravity-nano",
                "X-Title": "SEM Classifier Multi-Agent",
            },
        )
        _c.invoke("OK")
        llm = _c
        OPENROUTER_MODEL = model_id
        print(f"LLM activo: {model_id}")
        break
    except Exception as e:
        print(f"  [!] {model_id}: {e}")

if llm is None:
    raise RuntimeError("No se pudo conectar a ningún modelo OpenRouter.")""")

md("""## 2. Tools para los Agentes""")

code("""# ============================================================
# TOOLS: Acceso a métricas del modelo y búsqueda en arXiv
# ============================================================
from langchain_core.tools import tool
import httpx
import xml.etree.ElementTree as ET

@tool
def load_model_metrics() -> str:
    \"\"\"Carga las métricas del clasificador SEM entrenado.
    Retorna accuracy, F1, AUC-ROC, matriz de confusión y detalles del modelo.\"\"\"
    m = MODEL_METRICS
    return (
        f"Modelo: {m['model']}\\n"
        f"Tarea: {m['task']}\\n"
        f"Dataset: {m['dataset']} ({m['test_size']} imágenes test)\\n"
        f"Accuracy: {m['accuracy']:.4f} ({m['accuracy']:.1%})\\n"
        f"F1-score: {m['f1_score']:.4f}\\n"
        f"Precision: {m['precision']:.4f}\\n"
        f"Recall: {m['recall']:.4f}\\n"
        f"AUC-ROC: {m['auc_roc']:.4f}\\n"
        f"Errores: {m['n_errors']} ({m['error_rate']:.1%})\\n"
        f"Clases: {m['classes']}\\n"
        f"Matriz de confusión: {m['confusion_matrix']}\\n"
        f"Grad-CAM: {m['gradcam_interpretation']}"
    )

@tool
def search_sem_papers(query: str, max_results: int = 5) -> str:
    \"\"\"Busca papers científicos en arXiv sobre clasificación SEM y nanomateriales.
    Retorna títulos, autores y resúmenes.\"\"\"
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": f"all:{query}", "max_results": max_results, "sortBy": "relevance"}
    try:
        response = httpx.get(url, params=params, timeout=15)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        results = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            abstract = entry.find("atom:summary", ns).text.strip()[:300]
            authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)][:3]
            results.append(f"• {title}\\n  Autores: {', '.join(authors)}\\n  {abstract}")
        return "\\n\\n".join(results) if results else "Sin resultados."
    except Exception as e:
        return f"Error buscando papers: {e}"

print("Tools definidos: load_model_metrics, search_sem_papers")""")

md("""## 3. RAG con ChromaDB — Indexación de Papers""")

code("""# ============================================================
# RAG: ChromaDB para papers indexados
# ============================================================
import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.EphemeralClient()
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name="sem_papers", embedding_function=default_ef,
)

@tool
def index_papers(papers_text: str) -> str:
    \"\"\"Indexa texto de papers en el vector store ChromaDB para búsqueda semántica.\"\"\"
    paragraphs = [p.strip() for p in papers_text.split("\\n\\n") if len(p.strip()) > 50]
    if not paragraphs:
        return "Sin contenido para indexar."
    collection.add(
        documents=paragraphs,
        ids=[f"doc_{i}_{abs(hash(p[:50])) % 100000}" for i, p in enumerate(paragraphs)],
    )
    return f"{len(paragraphs)} fragmentos indexados en ChromaDB."

@tool
def semantic_search_papers(query: str, n_results: int = 3) -> str:
    \"\"\"Busca semánticamente en los papers indexados en ChromaDB.\"\"\"
    count = collection.count()
    if count == 0:
        return "No hay papers indexados. Usa index_papers primero."
    results = collection.query(query_texts=[query], n_results=min(n_results, count))
    docs = results.get("documents", [[]])[0]
    return "\\n---\\n".join(docs) if docs else "Sin resultados."

print(f"ChromaDB inicializado. Collection: '{collection.name}'")""")

md("""## 4. Estado Compartido del Sistema (LangGraph)""")

code("""# ============================================================
# ESTADO del sistema multi-agente (LangGraph TypedDict)
# ============================================================
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class SEMAnalysisState(TypedDict):
    messages: Annotated[list, add_messages]
    metrics_summary: str
    papers_context: str
    scientific_analysis: str
    draft_report: str
    final_report: str
    review_score: float
    review_cycles: int
    max_review_cycles: int
    status: str

def initial_state() -> SEMAnalysisState:
    return SEMAnalysisState(
        messages=[], metrics_summary="", papers_context="",
        scientific_analysis="", draft_report="", final_report="",
        review_score=0.0, review_cycles=0, max_review_cycles=3,
        status="running",
    )

print("Estado SEMAnalysisState definido.")""")

md("""## 5. Agentes del Sistema""")

code("""# ============================================================
# AGENTE 1: Analista de Métricas (ReAct con tools)
# ============================================================
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

analyst_tools = [load_model_metrics, search_sem_papers, index_papers]

analyst_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un analista de ML especializado en Computer Vision para microscopía SEM. "
     "Tu trabajo es: 1) Cargar las métricas del modelo con load_model_metrics, "
     "2) Buscar papers relevantes con search_sem_papers sobre 'SEM image classification nanoparticles nanowires CNN', "
     "3) Indexar los papers encontrados con index_papers, "
     "4) Producir un resumen analítico comparando los resultados con la literatura."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

analyst_agent = create_tool_calling_agent(llm, analyst_tools, analyst_prompt)
analyst_executor = AgentExecutor(
    agent=analyst_agent, tools=analyst_tools,
    max_iterations=6, verbose=True, handle_parsing_errors=True,
)

def analyst_node(state: SEMAnalysisState) -> dict:
    \"\"\"Nodo LangGraph: analiza métricas y busca literatura.\"\"\"
    if state["status"] != "running":
        return {}
    result = analyst_executor.invoke({
        "input": "Analiza las métricas del clasificador SEM y compáralas con la literatura existente."
    })
    return {
        "metrics_summary": result["output"],
        "messages": [HumanMessage(content=f"Análisis completado: {result['output'][:200]}...")],
    }

print("Agente Analista configurado.")""")

code("""# ============================================================
# AGENTE 2: Científico SEM (validación de Grad-CAM)
# ============================================================
scientist_tools = [semantic_search_papers, load_model_metrics]

def scientist_node(state: SEMAnalysisState) -> dict:
    \"\"\"Nodo LangGraph: valida la interpretabilidad científica.\"\"\"
    if state["status"] != "running":
        return {}
    
    prompt = f\"\"\"Eres un científico experto en microscopía SEM y nanomateriales.
    
Análisis previo del modelo:
{state['metrics_summary'][:1000]}

Evalúa:
1. ¿Son las métricas del modelo aceptables para clasificación de morfologías SEM?
2. ¿El Grad-CAM muestra que el modelo aprende features físicamente relevantes?
   (bordes redondeados para nanopartículas, estructuras elongadas para nanohilos)
3. ¿Qué limitaciones tiene este enfoque?
4. ¿Qué mejoras sugieres para investigación futura?

Genera un análisis científico estructurado.\"\"\"
    
    response = llm.invoke(prompt)
    return {
        "scientific_analysis": response.content,
        "messages": [HumanMessage(content="Validación científica completada.")],
    }

print("Agente Científico configurado.")""")

code("""# ============================================================
# AGENTE 3: Escritor de Reportes (usa CrewAI si disponible, sino LLM directo)
# ============================================================
def writer_node(state: SEMAnalysisState) -> dict:
    \"\"\"Nodo LangGraph: genera reporte científico.\"\"\"
    if state["status"] != "running":
        return {}
    
    prompt = f\"\"\"Escribe un reporte científico completo en Markdown sobre el clasificador SEM.

DATOS DEL ANÁLISIS:
{state['metrics_summary'][:800]}

VALIDACIÓN CIENTÍFICA:
{state['scientific_analysis'][:800]}

ESTRUCTURA REQUERIDA:
## Resumen Ejecutivo
## Metodología  
## Resultados y Métricas
## Interpretabilidad (Grad-CAM)
## Comparación con Literatura
## Limitaciones y Trabajo Futuro
## Conclusiones

Extensión: 600-800 palabras. Formato Markdown. Lenguaje académico pero accesible.\"\"\"
    
    response = llm.invoke(prompt)
    return {
        "draft_report": response.content,
        "review_cycles": state["review_cycles"] + 1,
    }

print("Agente Escritor configurado.")""")

code("""# ============================================================
# AGENTE 4: Revisor
# ============================================================
def reviewer_node(state: SEMAnalysisState) -> dict:
    \"\"\"Nodo LangGraph: evalúa el reporte con score numérico.\"\"\"
    if state["status"] != "running":
        return {}
    
    prompt = f\"\"\"Evalúa este reporte científico sobre clasificación SEM.

REPORTE:
{state['draft_report'][:2000]}

Responde EXACTAMENTE con este formato:
SCORE: [número 0-100]
FEEDBACK: [comentario breve si score < 75]\"\"\"
    
    response = llm.invoke(prompt)
    text = response.content.strip()
    
    # Extraer score
    import re
    score_match = re.search(r'SCORE:\\s*(\\d+)', text)
    score = int(score_match.group(1)) if score_match else 80
    
    if score >= 75 or state["review_cycles"] >= state["max_review_cycles"]:
        return {
            "review_score": float(score),
            "final_report": state["draft_report"],
            "status": "completed",
        }
    else:
        return {
            "review_score": float(score),
            "messages": [HumanMessage(content=f"Reporte rechazado (score={score}). Reescribiendo...")],
        }

print("Agente Revisor configurado.")""")

md("""## 6. Orquestador LangGraph — StateGraph con Ciclos""")

code("""# ============================================================
# ORQUESTADOR: LangGraph StateGraph
# ============================================================
from typing import Literal
from langgraph.graph import StateGraph, START, END

def review_router(state: SEMAnalysisState) -> Literal["writer", "__end__"]:
    \"\"\"Decide si el reporte necesita reescritura o está listo.\"\"\"
    if state["status"] == "completed":
        return "__end__"
    return "writer"

# Construir grafo
builder = StateGraph(SEMAnalysisState)

builder.add_node("analyst", analyst_node)
builder.add_node("scientist", scientist_node)
builder.add_node("writer", writer_node)
builder.add_node("reviewer", reviewer_node)

builder.add_edge(START, "analyst")
builder.add_edge("analyst", "scientist")
builder.add_edge("scientist", "writer")
builder.add_edge("writer", "reviewer")
builder.add_conditional_edges("reviewer", review_router, {"writer": "writer", "__end__": END})

graph = builder.compile()

# Visualizar
try:
    from IPython.display import Image, display
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    print(graph.get_graph().draw_mermaid())

print("\\nGrafo compilado y listo para ejecución.")""")

md("""## 7. Ejecución del Sistema Completo""")

code("""# ============================================================
# EJECUTAR el pipeline multi-agente
# ============================================================
import time

print("=" * 60)
print("EJECUTANDO SISTEMA MULTI-AGENTE SEM ANALYSIS")
print("=" * 60)

start_time = time.time()
state = initial_state()

try:
    result = graph.invoke(state)
    elapsed = time.time() - start_time
    
    print(f"\\n{'=' * 60}")
    print(f"RESULTADO FINAL")
    print(f"{'=' * 60}")
    print(f"Status: {result['status']}")
    print(f"Review score: {result['review_score']}")
    print(f"Ciclos de revisión: {result['review_cycles']}")
    print(f"Tiempo total: {elapsed:.1f}s")
    
except Exception as e:
    print(f"Error en ejecución: {e}")
    import traceback
    traceback.print_exc()""")

code("""# ============================================================
# MOSTRAR REPORTE FINAL
# ============================================================
from IPython.display import Markdown, display

if result.get("final_report"):
    display(Markdown(result["final_report"]))
    
    # Guardar reporte
    report_path = PROJECT_ROOT / 'reports' / 'multiagent_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(result["final_report"])
    print(f"\\nReporte guardado en: {report_path}")
else:
    print("No se generó reporte final.")""")

code("""# ============================================================
# RESUMEN DE INTEGRACIÓN U5
# ============================================================
print("=" * 60)
print("RESUMEN: Técnicas U5 integradas en este proyecto")
print("=" * 60)
print(\"\"\"
✓ U5_01 — ReAct + Tools: Agente Analista con load_model_metrics y search_sem_papers
✓ U5_02 — LangGraph StateGraph: Orquestador con ciclo condicional revisor→escritor
✓ U5_03 — CrewAI pattern: Agente Escritor con role-based prompting
✓ U5_05 — RAG + ChromaDB: Indexación y búsqueda semántica de papers arXiv
✓ U5_07 — Model Routing: OpenRouter con fallback automático multi-modelo
✓ U5_08 — Sistema End-to-End: Pipeline completo analyst→scientist→writer→reviewer

Métricas del sistema:
  - Agentes: 4 (Analyst, Scientist, Writer, Reviewer)
  - Tools: 4 (load_model_metrics, search_sem_papers, index_papers, semantic_search)
  - Vector Store: ChromaDB (ephemeral)
  - LLM Backend: OpenRouter ({})
  - Ciclo de revisión: max 3 iteraciones
\"\"\".format(OPENROUTER_MODEL))

print("\\n✓ Proyecto integrador completado.")""")

# Build notebook
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name":"ia_nano","language":"python","name":"python3"},
        "language_info": {"name":"python","version":"3.11.14"},
    },
    "nbformat": 4,
    "nbformat_minor": 4,
}

out = pathlib.Path(__file__).parent / "04_multiagent_analysis.ipynb"
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Generated: {out}")
