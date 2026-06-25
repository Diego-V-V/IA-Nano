"""
Orquestador LangGraph — Coordina el pipeline multi-agente para análisis SEM.
Flujo: classify → measure → visualize → analyze → report
"""
import time
from typing import Dict, Any, Optional
from PIL import Image

from agents.classifier import ClassifierAgent
from agents.measurer import MeasurerAgent
from agents.visualizer import VisualizerAgent
from agents.scientist import ScientistAgent
from agents.reporter import ReporterAgent


class SEMAnalysisPipeline:
    """
    Pipeline unificado que orquesta los 5 agentes para análisis completo
    de imágenes SEM.

    Agentes:
    1. Clasificador (ResNet-18) — Clasifica nanopartículas vs nanohilos
    2. Medidor (Image Processing) — Mide tamaños y morfología
    3. Visualizador (Grad-CAM) — Genera mapas de interpretabilidad
    4. Científico (LLM) — Interpreta resultados
    5. Reportero (LLM) — Genera reporte final
    """

    def __init__(self):
        print("=" * 60)
        print("INICIALIZANDO SISTEMA MULTI-AGENTE SEM")
        print("=" * 60)

        # Inicializar agentes
        print("\n[1/5] Cargando Agente Clasificador...")
        self.classifier = ClassifierAgent()

        print("[2/5] Cargando Agente Medidor...")
        self.measurer = MeasurerAgent()

        print("[3/5] Cargando Agente Visualizador...")
        self.visualizer = VisualizerAgent(
            self.classifier.get_model(),
            self.classifier.device,
        )

        print("[4/5] Cargando Agente Científico...")
        self.scientist = ScientistAgent()

        print("[5/5] Cargando Agente Reportero...")
        self.reporter = ReporterAgent()

        print("\n" + "=" * 60)
        print("✓ SISTEMA MULTI-AGENTE LISTO")
        print("=" * 60)

    def analyze(self, image: Image.Image, compound: str = "Desconocido") -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo de análisis sobre una imagen SEM.

        Args:
            image: Imagen PIL a analizar.
            compound: Compuesto químico proporcionado por el usuario.

        Returns:
            Dict con todos los resultados del análisis.
        """
        start_time = time.time()
        results = {
            "status": "running",
            "agents_completed": [],
            "errors": [],
            "compound": compound,
        }

        # ── Paso 1: Clasificación ──────────────────────────────────
        try:
            print("\n▸ Agente Clasificador ejecutando...")
            t0 = time.time()
            classification = self.classifier.classify(image)
            classification["elapsed_s"] = round(time.time() - t0, 2)
            results["classification"] = classification
            results["agents_completed"].append("classifier")
            print(f"  ✓ {classification['label']} ({classification['confidence']:.1%}) "
                  f"[{classification['elapsed_s']}s]")
        except Exception as e:
            results["errors"].append(f"Clasificador: {e}")
            classification = {"predicted_class": "", "label": "Error", "confidence": 0}
            results["classification"] = classification
            print(f"  ✗ Error: {e}")

        # ── Paso 2: Medición ───────────────────────────────────────
        try:
            print("▸ Agente Medidor ejecutando...")
            t0 = time.time()
            measurements = self.measurer.measure(
                image,
                predicted_class=classification.get("predicted_class", ""),
            )
            measurements["elapsed_s"] = round(time.time() - t0, 2)
            results["measurements"] = measurements
            results["agents_completed"].append("measurer")
            stats = measurements["statistics"]
            print(f"  ✓ {stats['count']} estructuras, "
                  f"Ø={stats['diameter_mean_nm']:.0f}nm "
                  f"[{measurements['elapsed_s']}s]")
        except Exception as e:
            results["errors"].append(f"Medidor: {e}")
            measurements = {"statistics": {}, "morphology_interpretation": ""}
            results["measurements"] = measurements
            print(f"  ✗ Error: {e}")

        # ── Paso 3: Visualización Grad-CAM ─────────────────────────
        try:
            print("▸ Agente Visualizador ejecutando...")
            t0 = time.time()
            visualization = self.visualizer.visualize(
                image, self.classifier.get_transform()
            )
            visualization["elapsed_s"] = round(time.time() - t0, 2)
            results["visualization"] = visualization
            results["agents_completed"].append("visualizer")
            print(f"  ✓ Grad-CAM generado [{visualization['elapsed_s']}s]")
        except Exception as e:
            results["errors"].append(f"Visualizador: {e}")
            results["visualization"] = {
                "activation_analysis": {},
                "heatmap_base64": "",
                "overlay_base64": "",
                "original_base64": "",
            }
            print(f"  ✗ Error: {e}")

        # ── Paso 4: Análisis Científico (LLM) ─────────────────────
        try:
            print("▸ Agente Científico ejecutando...")
            t0 = time.time()
            activation = results.get("visualization", {}).get(
                "activation_analysis", {}
            )
            science = self.scientist.analyze(
                classification, measurements, activation, compound
            )
            science["elapsed_s"] = round(time.time() - t0, 2)
            results["scientific_analysis"] = science
            results["agents_completed"].append("scientist")
            print(f"  ✓ Análisis científico completado "
                  f"(modelo: {science.get('llm_model', 'N/A')}) "
                  f"[{science['elapsed_s']}s]")
        except Exception as e:
            results["errors"].append(f"Científico: {e}")
            results["scientific_analysis"] = {
                "scientific_analysis": "Error en análisis.",
                "llm_model": "error",
            }
            print(f"  ✗ Error: {e}")

        # ── Paso 5: Reporte Final (LLM) ───────────────────────────
        try:
            print("▸ Agente Reportero ejecutando...")
            t0 = time.time()
            total_elapsed = time.time() - start_time
            report = self.reporter.generate_report(
                classification,
                measurements,
                results["scientific_analysis"].get("scientific_analysis", ""),
                elapsed_time=total_elapsed,
            )
            report_elapsed = round(time.time() - t0, 2)
            results["report"] = report
            results["report_elapsed_s"] = report_elapsed
            results["agents_completed"].append("reporter")
            print(f"  ✓ Reporte generado [{report_elapsed}s]")
        except Exception as e:
            results["errors"].append(f"Reportero: {e}")
            results["report"] = "Error generando reporte."
            print(f"  ✗ Error: {e}")

        # ── Finalizar ──────────────────────────────────────────────
        total_time = time.time() - start_time
        results["total_elapsed_s"] = round(total_time, 2)
        results["status"] = "completed"
        results["agents_total"] = 5
        results["agents_success"] = len(results["agents_completed"])

        print(f"\n{'=' * 60}")
        print(f"✓ ANÁLISIS COMPLETADO — {results['agents_success']}/5 agentes OK")
        print(f"  Tiempo total: {total_time:.1f}s")
        print(f"{'=' * 60}")

        return results


# Singleton global del pipeline
_pipeline_instance: Optional[SEMAnalysisPipeline] = None


def get_pipeline() -> SEMAnalysisPipeline:
    """Obtiene la instancia singleton del pipeline."""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = SEMAnalysisPipeline()
    return _pipeline_instance
