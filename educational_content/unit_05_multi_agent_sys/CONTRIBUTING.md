# Contribuir a la Unidad 5: Sistemas Multi-Agente Modernos

## Estructura de la Unidad

La Unidad 5 contiene los notebooks base del curso que enseñan el diseño, implementación y despliegue de agentes inteligentes para investigación en nanotecnología.

## Proceso de actualización

### 1. Actualizar Dependencias del Ecosistema de Agentes

El ecosistema de IA cambia semanalmente. Al actualizar:

```bash
# Verificar versiones de LangChain, LangGraph y CrewAI
pip list | grep -E "langchain|langgraph|crewai|smolagents"

# Actualizar el entorno principal ia_nano
conda env update --file ../../environment.yml --prune
```

### 2. Modificación de Notebooks
- **Mantener el Routing:** Nunca introduzcas modelos de OpenAI o Anthropic de manera hardcodeada (`ChatOpenAI(api_key="sk-...")`). Utiliza SIEMPRE OpenRouter y el fallback con Ollama. Esto garantiza que estudiantes sin presupuesto puedan correr el curso localmente.
- **Retrocompatibilidad:** Si LangGraph depreca una función (ej. transiciones condicionales), añade una nota temporal alertando del cambio y reescribe la celda.

### 3. Reporte de Costos y APIs
Si un nuevo notebook requiere acceder a un API comercial (ej. un search engine comercial o un LLM premium), debes actualizar `cost_estimation.json` (o la tabla del README) para reflejar el nuevo costo esperado por ejecución.

### 4. Entregables de Calidad
Asegúrate de ejecutar el script `check_deprecations.py` dentro de la carpeta `unit_05_multi_agent_sys` antes de hacer commit de los cambios. Este script verifica si el código subyacente ha sufrido cambios críticos de API.
