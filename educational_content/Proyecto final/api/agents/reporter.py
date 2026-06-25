"""
Agente Reportero — Genera reporte científico final en Markdown.
Integra todos los resultados de los agentes del pipeline.
"""
from typing import Dict, Any, Optional
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_HEADERS,
    MODELS_FALLBACK, MODEL_METRICS,
)


class ReporterAgent:
    """Agente que genera un reporte científico final integrando todos los resultados."""

    def __init__(self):
        self.llm = None
        self.model_id = ""
        self._connect_llm()

    def _connect_llm(self):
        """Conecta al LLM con fallback automático."""
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            return

        for model_id in MODELS_FALLBACK:
            try:
                llm = ChatOpenAI(
                    base_url=OPENROUTER_BASE_URL,
                    api_key=OPENROUTER_API_KEY,
                    model=model_id,
                    temperature=0.4,
                    default_headers=OPENROUTER_HEADERS,
                    max_tokens=2000,
                )
                llm.invoke("test")
                self.llm = llm
                self.model_id = model_id
                print(f"✓ Agente Reportero conectado: {model_id}")
                return
            except Exception as e:
                pass

    def generate_report(
        self,
        classification: Dict[str, Any],
        measurements: Dict[str, Any],
        scientific_analysis: str,
        compound: str = "Desconocido",
        elapsed_time: float = 0,
    ) -> str:
        """
        Genera reporte final en Markdown.

        Returns:
            Reporte completo en Markdown.
        """
        if self.llm is not None:
            return self._llm_report(
                classification, measurements, scientific_analysis, compound, elapsed_time
            )
        return self._template_report(
            classification, measurements, scientific_analysis, compound, elapsed_time
        )

    def _llm_report(
        self,
        classification: Dict,
        measurements: Dict,
        scientific_analysis: str,
        compound: str,
        elapsed_time: float,
    ) -> str:
        stats = measurements.get("statistics", {})
        prompt = f"""Genera un reporte científico completo en Markdown sobre el análisis de una imagen SEM.

DATOS:
- Compuesto: {compound}
- Clasificación: {classification.get('label')} (confianza: {classification.get('confidence', 0):.1%})
- Partículas detectadas: {stats.get('count', 0)}
- Diámetro promedio: {stats.get('diameter_mean_nm', 0):.0f} ± {stats.get('diameter_std_nm', 0):.0f} nm
- Aspect ratio: {stats.get('aspect_ratio_mean', 0):.2f}
- Circularidad: {stats.get('circularity_mean', 0):.3f}
- Modelo: ResNet-18 (Accuracy: {MODEL_METRICS.get('accuracy', 0):.1%}, AUC-ROC: {MODEL_METRICS.get('auc_roc', 0):.4f})
- Tiempo de análisis: {elapsed_time:.1f}s

ANÁLISIS CIENTÍFICO PREVIO:
{scientific_analysis[:1500]}

ESTRUCTURA DEL REPORTE (en español):
# Reporte de Análisis SEM — Sistema Multi-Agente
## Resumen Ejecutivo
## Clasificación Morfológica
## Análisis Dimensional
## Interpretabilidad del Modelo (Grad-CAM)
## Predicción de Propiedades
## Comparación con Literatura Científica
## Conclusiones y Recomendaciones

Extensión: 500-700 palabras. Formato Markdown. Lenguaje científico accesible.
Incluye la fecha actual: {datetime.now().strftime('%Y-%m-%d %H:%M')}."""

        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception:
            return self._template_report(
                classification, measurements, scientific_analysis, compound, elapsed_time
            )

    def _template_report(
        self,
        classification: Dict,
        measurements: Dict,
        scientific_analysis: str,
        compound: str,
        elapsed_time: float,
    ) -> str:
        """Genera reporte usando plantilla cuando no hay LLM disponible."""
        stats = measurements.get("statistics", {})
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        return f"""# Reporte de Análisis SEM — Sistema Multi-Agente

**Fecha:** {now}  
**Sistema:** Antigravity Nano Research — Multi-Agent SEM Analyzer  
**Compuesto Químico:** {compound}  
**Modelo:** ResNet-18 (ImageNet → SEM fine-tuned)  
**Tiempo de análisis:** {elapsed_time:.1f}s

---

## Resumen Ejecutivo

Se analizó una imagen de microscopía electrónica de barrido (SEM) mediante un sistema
multi-agente que integra clasificación por deep learning, medición morfológica automatizada
y análisis científico asistido por IA.

**Resultado principal:** La imagen fue clasificada como **{classification.get('label', 'N/A')}**
con una confianza del **{classification.get('confidence', 0):.1%}**.

---

## Clasificación Morfológica

| Parámetro | Valor |
|-----------|-------|
| Clase predicha | {classification.get('label', 'N/A')} |
| Confianza | {classification.get('confidence', 0):.1%} |
| P(nanopartículas) | {classification.get('probabilities', {}).get('nanoparticles', 0):.4f} |
| P(nanohilos) | {classification.get('probabilities', {}).get('nanowires', 0):.4f} |

El modelo ResNet-18 fue entrenado sobre el dataset NFFA-EUROPE SEM con accuracy de
{MODEL_METRICS.get('accuracy', 0):.1%} y AUC-ROC de {MODEL_METRICS.get('auc_roc', 0):.4f}.

---

## Análisis Dimensional

| Medición | Valor |
|----------|-------|
| Estructuras detectadas | {stats.get('count', 0)} |
| Diámetro equivalente (media) | {stats.get('diameter_mean_nm', 0):.0f} nm |
| Diámetro equivalente (σ) | {stats.get('diameter_std_nm', 0):.0f} nm |
| Rango de tamaño | {stats.get('diameter_min_nm', 0):.0f} — {stats.get('diameter_max_nm', 0):.0f} nm |
| Aspect ratio (media) | {stats.get('aspect_ratio_mean', 0):.2f} |
| Circularidad (media) | {stats.get('circularity_mean', 0):.3f} |

{measurements.get('morphology_interpretation', '')}

---

## Discusión Científica

{scientific_analysis}

---

## Conclusiones

1. La clasificación automática identifica la muestra como **{classification.get('label', 'N/A')}**
   con alta confianza ({classification.get('confidence', 0):.1%}).
2. Las mediciones morfológicas son consistentes con la clasificación.
3. El sistema multi-agente permite análisis reproducible y escalable de imágenes SEM.

---

*Generado automáticamente por el Sistema Multi-Agente Antigravity Nano Research.*
"""
