# PLAN — Unidad 5: Sistemas Multi-Agente Modernos

## 1. Audiencia Objetivo y Prerrequisitos
- **Audiencia:** Investigadores, estudiantes de posgrado y profesionales en nanotecnología y ciencias aplicadas que necesitan automatizar análisis, revisión de literatura y flujos de trabajo científicos complejos.
- **Prerrequisitos:** 
  - Conocimientos de Python (nivel intermedio, version 3.11+)
  - Manejo de APIs REST y variables de entorno
  - Conceptos básicos de prompts y modelos generativos (Unidad 4)

## 2. Componentes a Desarrollar (Notebooks)
El curso se estructura en 8 módulos principales:
- `U5_00_META_CONSTRUYENDO_CON_IA.ipynb`: Metacognición sobre el diseño del curso con IA.
- `U5_01_FUNDAMENTOS_AGENTES_MODERNOS.ipynb`: Patrones ReAct, Tool Calling, agentes de código (smolagents).
- `U5_02_LANGCHAIN_AVANZADO_LANGGRAPH.ipynb`: Orquestación con grafos de estado, ciclos y Human-in-the-Loop.
- `U5_03_CREWAI_SISTEMAS_MULTIAGENTE.ipynb`: Agentes basados en roles para investigación colaborativa.
- `U5_04_GOOGLE_ADK_A2A_COMP.ipynb` (y GEMMA4): Comunicación Agente a Agente y protocolos MCP.
- `U5_05_RAG_MEMORIA_AVANZADA.ipynb`: ChromaDB y Mem0 para memoria a largo plazo.
- `U5_06_GRAPH_RAG_MEMORIA.ipynb`: Grafos de conocimiento con Neo4j.
- `U5_07_MULTIMODAL_PRODUCCION.ipynb`: Integración con FastAPI, observabilidad y visión.
- `U5_08_PROYECTO_INTEGRADOR.ipynb`: Construcción end-to-end de un pipeline científico.

## 3. Arquitectura de Skills
- Se utilizarán **skills reutilizables** a lo largo del curso.
- En los primeros notebooks (U5_01-U5_03), las herramientas se definen localmente o usando `@tool` para comprensión explícita.
- En arquitecturas de producción (U5_07-U5_08), se modulariza y expone mediante FastAPI y protocolos estándar.

## 4. Fallbacks y Resiliencia
- Se implementará un **enrutamiento en cascada** para los LLMs:
  `OpenRouter (Gemini/Claude) -> OpenAI (GPT-4o) -> Ollama (llama3.2 local)`
- Esto garantiza que los notebooks sean ejecutables sin internet o cuando las APIs comerciales fallen.
