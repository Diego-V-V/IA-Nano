# PROTOCOLO — Estándares de Calidad para la Unidad 5

Para asegurar una experiencia de aprendizaje consistente y libre de errores a lo largo de los notebooks de la Unidad 5, se debe cumplir el siguiente protocolo:

## 1. Reglas de Arquitectura de Notebooks
- **Warm-up Inicial:** Toda notebook debe comenzar con una celda que instale dependencias faltantes (`!pip install -q`) y verifique la carga correcta de las variables de entorno (`.env`), específicamente `OPENROUTER_API_KEY`.
- **Independencia:** Cada notebook debe poder ejecutarse de manera autónoma sin depender del estado en memoria de la notebook anterior (aunque sí de los archivos generados si se documenta claramente).
- **Conexiones Pedagógicas:** Al final de cada notebook, debe incluirse una celda Markdown que indique explícitamente `→ Continuar con: [Nombre de la Siguiente Notebook]`.

## 2. Reglas de Seguridad de Código (Security Review)
- **Cero Hardcoding:** Prohibido escribir API Keys directamente en el código. Todas deben cargarse mediante `os.environ.get()` o `dotenv`.
- **Evaluación Segura:** Nunca usar `eval()` o `exec()` al ejecutar código generado por los agentes matemáticos o lógicos. Utilizar librerías como `ast.literal_eval` o parsers seguros (AST binario).
- **Aislamiento de Bases de Datos:** Las bases de datos locales (ChromaDB, Neo4j, SQLite) deben utilizar rutas relativas dentro de la carpeta del proyecto y tener scripts de inicialización y limpieza.

## 3. Reglas de Orquestación y LLMs
- **Fallback Activo:** Toda inicialización del modelo LLM principal (`ChatOpenAI`, `ChatAnthropic`, etc.) debe estar envuelta en una estructura de cascada (e.g. Try-Except con Gemini -> GPT-4o-mini -> Claude Haiku -> Ollama).
- **Costo Controlado:** Configurar temperatura `T=0` para tareas analíticas y un límite estricto de iteraciones (`max_iterations=5` o similar) en los grafos de LangGraph y AgentExecutor para prevenir bucles infinitos que consuman tokens.
- **Trazabilidad:** Imprimir explícitamente el estado del sistema, el modelo activo y el número de tokens/iteraciones consumidas al final de las secciones críticas.
