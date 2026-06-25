"""
Agente Científico — Interpreta resultados de clasificación y medición usando LLM.
Valida que los resultados tengan sentido físico para nanomateriales SEM.
"""
from typing import Dict, Any, Optional

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_HEADERS,
    MODELS_FALLBACK, MODEL_METRICS,
)
from rag_utils import query_rag


class ScientistAgent:
    """Agente científico que interpreta resultados usando LLM via OpenRouter."""

    def __init__(self):
        self.llm = None
        self.model_id = ""
        self._connect_llm()

    def _connect_llm(self):
        """Conecta al LLM con fallback automático."""
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            print("⚠ langchain_openai no disponible. Agente científico en modo offline.")
            return

        for model_id in MODELS_FALLBACK:
            try:
                llm = ChatOpenAI(
                    base_url=OPENROUTER_BASE_URL,
                    api_key=OPENROUTER_API_KEY,
                    model=model_id,
                    temperature=0.3,
                    default_headers=OPENROUTER_HEADERS,
                    max_tokens=1500,
                )
                llm.invoke("test")
                self.llm = llm
                self.model_id = model_id
                print(f"✓ Agente Científico conectado: {model_id}")
                return
            except Exception as e:
                print(f"  [!] {model_id}: {e}")

        print("⚠ No se pudo conectar a LLM. Agente científico en modo offline.")

    def analyze(
        self,
        classification: Dict[str, Any],
        measurements: Dict[str, Any],
        activation_analysis: Dict[str, Any],
        compound: str = "Desconocido"
    ) -> Dict[str, str]:
        """
        Genera análisis científico de los resultados.

        Returns:
            dict con scientific_analysis y recommendations.
        """
        if self.llm is None:
            return self._offline_analysis(classification, measurements, compound)

        # Realizar consulta al RAG usando ChromaDB
        print(f"  🔍 Consultando RAG en ChromaDB para: {compound} {classification.get('label', '')}")
        rag_context = query_rag(f"{compound} {classification.get('label', '')} properties applications")

        prompt = self._build_prompt(classification, measurements, activation_analysis, compound, rag_context)

        try:
            response = self.llm.invoke(prompt)
            analysis = response.content
        except Exception as e:
            print(f"Error LLM: {e}")
            return self._offline_analysis(classification, measurements, compound)

        return {
            "scientific_analysis": analysis,
            "llm_model": self.model_id,
        }

    def _build_prompt(
        self,
        classification: Dict,
        measurements: Dict,
        activation: Dict,
        compound: str,
        rag_context: str
    ) -> str:
        stats = measurements.get("statistics", {})
        morph = measurements.get("morphology_interpretation", "")

        return f"""Eres un científico experto en microscopía electrónica de barrido (SEM) y nanomateriales.

MATERIAL Y RESULTADOS DEL CLASIFICADOR:
- Compuesto Químico: {compound}
- Clase predicha: {classification.get('label', 'N/A')}
- Confianza: {classification.get('confidence', 0):.1%}
- Probabilidades: {classification.get('probabilities', {})}

MÉTRICAS DEL MODELO (pre-evaluación en test set):
- Accuracy: {MODEL_METRICS.get('accuracy', 0):.1%}
- F1-score: {MODEL_METRICS.get('f1_score', 0):.4f}
- AUC-ROC: {MODEL_METRICS.get('auc_roc', 0):.4f}

MEDICIONES MORFOLÓGICAS:
- Partículas detectadas: {stats.get('count', 0)}
- Diámetro equivalente promedio: {stats.get('diameter_mean_nm', 0):.0f} ± {stats.get('diameter_std_nm', 0):.0f} nm
- Rango de tamaño: {stats.get('diameter_min_nm', 0):.0f} — {stats.get('diameter_max_nm', 0):.0f} nm
- Aspect ratio promedio: {stats.get('aspect_ratio_mean', 0):.2f}
- Circularidad promedio: {stats.get('circularity_mean', 0):.3f}
- Interpretación morfológica: {morph}

GRAD-CAM (Interpretabilidad):
- Activación alta: {activation.get('high_activation_pct', 0):.1f}% de la imagen
- Región principal: {activation.get('primary_region', 'N/A')}
- {MODEL_METRICS.get('gradcam_interpretation', '')}

═══ LITERATURA CIENTÍFICA CON REFERENCIAS BIBLIOGRÁFICAS (Recuperada vía RAG — ChromaDB) ═══
{rag_context}
═══ FIN DE LITERATURA ═══

Genera un análisis científico estructurado en español (400-550 palabras) que incluya OBLIGATORIAMENTE:

1. **Validación de la clasificación**: ¿La predicción es consistente con las mediciones morfológicas?

2. **Análisis dimensional**: ¿Los tamaños medidos son realistas para este tipo de nanoestructura? Compara con los rangos reportados en la literatura recuperada.

3. **Predicción de Propiedades**: Basado en el compuesto "{compound}", la morfología ({classification.get('label', 'N/A')}), y el diámetro promedio de {stats.get('diameter_mean_nm', 0):.0f} nm, predice las propiedades físicas, ópticas, eléctricas o catalíticas esperadas. Apóyate DIRECTAMENTE en los datos de la literatura del RAG.

4. **Aplicaciones Potenciales**: Lista al menos 3-5 aplicaciones tecnológicas concretas de este material con esta morfología y tamaño, basándote en la literatura recuperada.

5. **Comparación con Literatura Científica**: Compara EXPLÍCITAMENTE los resultados obtenidos con los datos de las referencias bibliográficas. CITA el autor, año y revista de cada referencia que uses (están incluidas en la literatura como "[REF]"). Ejemplo: "De acuerdo con Chen & Mao (2007, Chemical Reviews)..."

6. **Calidad de la muestra y Recomendaciones**: Observaciones sobre homogeneidad y sugerencias de análisis complementarios (XRD, FTIR, BET, etc.).

IMPORTANTE: Debes citar al menos 2 referencias bibliográficas EXPLÍCITAMENTE con autor y año. Usa lenguaje científico preciso pero accesible."""

    def _offline_analysis(
        self, classification: Dict, measurements: Dict, compound: str
    ) -> Dict[str, str]:
        """Análisis offline cuando el LLM no está disponible."""
        pred = classification.get("label", "N/A")
        conf = classification.get("confidence", 0)
        stats = measurements.get("statistics", {})

        analysis = f"""## Análisis Científico (modo offline)

**Compuesto:** {compound}
**Clasificación:** {pred} con {conf:.1%} de confianza.

**Mediciones:**
- Se detectaron {stats.get('count', 0)} estructuras.
- Diámetro equivalente promedio: {stats.get('diameter_mean_nm', 0):.0f} ± {stats.get('diameter_std_nm', 0):.0f} nm
- Aspect ratio promedio: {stats.get('aspect_ratio_mean', 0):.2f}
- Circularidad promedio: {stats.get('circularity_mean', 0):.3f}

**Interpretación:**
{measurements.get('morphology_interpretation', 'Sin interpretación disponible.')}

**Modelo:** ResNet-18 fine-tuned sobre NFFA-EUROPE SEM Dataset.
Accuracy: {MODEL_METRICS.get('accuracy', 0):.1%}, AUC-ROC: {MODEL_METRICS.get('auc_roc', 0):.4f}.

> Nota: Análisis generado sin conexión al LLM. Para un análisis más detallado,
> configure OPENROUTER_API_KEY en las variables de entorno."""

        return {
            "scientific_analysis": analysis,
            "llm_model": "offline",
        }
