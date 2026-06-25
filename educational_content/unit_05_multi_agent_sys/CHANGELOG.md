# Changelog — Unidad 5: Sistemas Multi-Agente Modernos

Todas las actualizaciones notables a este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.0.0] — 2026-05-13

### Agregado
- **U5_00**: Meta-notebook de estructuración educativa guiada por IA.
- **U5_01**: Fundamentos de Agentes Modernos (ReAct, Smolagents, Tool Calling).
- **U5_02**: Orquestación con LangGraph (StateGraph, Checkpoints, HITL).
- **U5_03**: Sistemas Multi-Agente con CrewAI (Roles, delegación).
- **U5_04**: Interoperabilidad y Protocolos A2A (Google ADK, MCP).
- **U5_05**: RAG y Memoria Avanzada (ChromaDB, Mem0).
- **U5_06**: Graph RAG y Memoria Estructurada (Neo4j).
- **U5_07**: Despliegue en Producción (FastAPI Multimodal, Model Routing).
- **U5_08**: Proyecto Integrador de la Unidad.

### Stack Tecnológico — v1.0.0
| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Orquestación | LangChain | 0.3.25 |
| Grafos de Estado | LangGraph | 0.2.56 |
| Multi-Agente | CrewAI | 0.80.0 |
| Agentes Corporativos | Google ADK | 1.0.0 |
| Code Agents | smolagents | 1.13.0 |
| Vector Store | ChromaDB | 0.6.3 |
| Memoria Inteligente | Mem0 | latest |
| Graph Database | Neo4j | 5.x |
| APIs Backend | FastAPI | 0.115.11 |

### Costos Estimados de Ejecución
El costo total estimado para ejecutar la Unidad 5 completa asumiendo el modelo `google/gemini-2.5-flash` o `gpt-4o-mini` a través de OpenRouter es **< $0.05 USD por estudiante**. Todos los modelos locales con `Ollama` tienen un costo de $0.00.

---

## Guía de actualización para futuras versiones

### Al actualizar LangChain / LangGraph
- [ ] Verificar migraciones de `agent_executor` a `create_react_agent` en LangGraph.
- [ ] Validar compatibilidad de `ChatPromptTemplate` con las nuevas versiones.

### Al actualizar CrewAI
- [ ] Comprobar deprecación de atributos en las clases `Agent` y `Task`.
- [ ] Verificar compatibilidad de integraciones de LLM (soporte para LangChain LLMs vs. LiteLLM).

### Al actualizar APIs de Memoria
- [ ] Validar inicialización y persistencia en disco de ChromaDB.
- [ ] Comprobar la conexión asíncrona de Neo4j en el Graph RAG.
