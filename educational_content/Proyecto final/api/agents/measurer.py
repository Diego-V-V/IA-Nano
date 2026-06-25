"""
Agente Medidor — Estimación de tamaño y morfología de partículas SEM.
Usa procesamiento de imagen (umbralización, contornos, bounding boxes).
Incluye autocalibración de barra de escala vía ScaleBarDetector.
"""
import numpy as np
from PIL import Image, ImageFilter
from typing import Dict, Any, List
import math

from agents.scale_detector import ScaleBarDetector


class MeasurerAgent:
    """Agente que mide partículas/estructuras en imágenes SEM."""

    def __init__(self, scale_bar_nm_per_px: float = 10.0):
        """
        Args:
            scale_bar_nm_per_px: Escala estimada nm/pixel (default para SEM ~10 nm/px).
        """
        self.scale_nm_per_px = scale_bar_nm_per_px
        self.scale_detector = ScaleBarDetector()

    def measure(self, image: Image.Image, predicted_class: str = "") -> Dict[str, Any]:
        """
        Analiza la imagen SEM para extraer mediciones morfológicas.
        Intenta autocalibrar la escala nm/px detectando la barra de escala.

        Returns:
            dict con conteo, tamaños, aspect ratios, estadísticas y calibración.
        """
        # ── Autocalibración de escala ──
        scale_info = self.scale_detector.detect_scale(image)
        self.scale_nm_per_px = scale_info["nm_per_px"]
        print(f"  📏 Escala: {self.scale_nm_per_px} nm/px "
              f"({scale_info['method']}, confianza: {scale_info['confidence']})")

        # Convertir a escala de grises
        gray = np.array(image.convert("L"), dtype=np.float64)
        h, w = gray.shape

        # --- Detección de estructuras por umbralización adaptativa ---
        # Normalizar intensidad
        gray_norm = (gray - gray.min()) / (gray.max() - gray.min() + 1e-8) * 255
        gray_uint8 = gray_norm.astype(np.uint8)

        # Umbralización de Otsu manual
        threshold = self._otsu_threshold(gray_uint8)
        binary = gray_uint8 > threshold

        # Limpiar: eliminar bordes (barras de escala SEM)
        margin = int(min(h, w) * 0.08)
        binary[:margin, :] = False
        binary[-margin:, :] = False
        binary[:, :margin] = False
        binary[:, -margin:] = False

        # Encontrar componentes conectados (flood fill simplificado)
        particles = self._find_connected_components(binary, min_area=50)

        # Medir cada partícula
        measurements = []
        for particle in particles:
            bbox = self._bounding_box(particle)
            area_px = len(particle)
            area_nm2 = area_px * (self.scale_nm_per_px ** 2)
            perimeter = self._estimate_perimeter(particle, gray.shape)
            bbox_w = bbox["width"]
            bbox_h = bbox["height"]
            aspect_ratio = max(bbox_w, bbox_h) / (min(bbox_w, bbox_h) + 1e-8)
            diameter_eq = 2 * math.sqrt(area_px / math.pi) * self.scale_nm_per_px
            circularity = (4 * math.pi * area_px) / (perimeter ** 2 + 1e-8)

            measurements.append({
                "area_px": area_px,
                "area_nm2": round(area_nm2, 1),
                "diameter_eq_nm": round(diameter_eq, 1),
                "aspect_ratio": round(aspect_ratio, 2),
                "circularity": round(min(circularity, 1.0), 3),
                "bbox": bbox,
            })

        # Ordenar por área descendente
        measurements.sort(key=lambda m: m["area_px"], reverse=True)

        # Limitar a las 20 partículas más grandes
        measurements = measurements[:20]

        # Estadísticas globales
        if measurements:
            diameters = [m["diameter_eq_nm"] for m in measurements]
            aspect_ratios = [m["aspect_ratio"] for m in measurements]
            circularities = [m["circularity"] for m in measurements]
            stats = {
                "count": len(measurements),
                "diameter_mean_nm": float(round(np.mean(diameters), 1)),
                "diameter_std_nm": float(round(np.std(diameters), 1)),
                "diameter_min_nm": float(round(min(diameters), 1)),
                "diameter_max_nm": float(round(max(diameters), 1)),
                "aspect_ratio_mean": float(round(np.mean(aspect_ratios), 2)),
                "circularity_mean": float(round(np.mean(circularities), 3)),
            }
        else:
            stats = {
                "count": 0,
                "diameter_mean_nm": 0, "diameter_std_nm": 0,
                "diameter_min_nm": 0, "diameter_max_nm": 0,
                "aspect_ratio_mean": 0, "circularity_mean": 0,
            }

        # Interpretación basada en morfología
        morphology = self._interpret_morphology(stats, predicted_class)

        return {
            "statistics": stats,
            "particles": measurements[:10],  # Top 10 para el JSON
            "morphology_interpretation": morphology,
            "image_size": {"width": w, "height": h},
            "scale_nm_per_px": float(self.scale_nm_per_px),
            "threshold_used": int(threshold),
            "scale_calibration": {
                "nm_per_px": float(scale_info["nm_per_px"]),
                "method": scale_info["method"],
                "confidence": scale_info["confidence"],
                "bar_length_px": scale_info.get("bar_length_px"),
                "scale_text": scale_info.get("scale_text"),
                "details": scale_info["details"],
            },
        }

    def _otsu_threshold(self, gray: np.ndarray) -> float:
        """Calcula el umbral óptimo de Otsu."""
        hist = np.zeros(256)
        for val in gray.flatten():
            hist[int(val)] += 1
        hist = hist / hist.sum()

        best_thresh = 0
        best_var = 0
        for t in range(1, 255):
            w0 = hist[:t].sum()
            w1 = hist[t:].sum()
            if w0 == 0 or w1 == 0:
                continue
            mu0 = np.sum(np.arange(t) * hist[:t]) / w0
            mu1 = np.sum(np.arange(t, 256) * hist[t:]) / w1
            var = w0 * w1 * (mu0 - mu1) ** 2
            if var > best_var:
                best_var = var
                best_thresh = t

        return best_thresh

    def _find_connected_components(
        self, binary: np.ndarray, min_area: int = 50
    ) -> List[List[tuple]]:
        """Encuentra componentes conectados en imagen binaria."""
        h, w = binary.shape
        visited = np.zeros_like(binary, dtype=bool)
        components = []

        for y in range(h):
            for x in range(w):
                if binary[y, x] and not visited[y, x]:
                    # BFS para encontrar el componente
                    component = []
                    stack = [(y, x)]
                    while stack:
                        cy, cx = stack.pop()
                        if (
                            0 <= cy < h and 0 <= cx < w
                            and binary[cy, cx]
                            and not visited[cy, cx]
                        ):
                            visited[cy, cx] = True
                            component.append((cy, cx))
                            if len(component) > 5000:
                                break  # Evitar componentes gigantes
                            stack.extend([
                                (cy - 1, cx), (cy + 1, cx),
                                (cy, cx - 1), (cy, cx + 1),
                            ])
                    if min_area <= len(component) <= 5000:
                        components.append(component)

        return components

    def _bounding_box(self, component: List[tuple]) -> Dict[str, int]:
        """Calcula el bounding box de un componente."""
        ys = [p[0] for p in component]
        xs = [p[1] for p in component]
        return {
            "x": min(xs), "y": min(ys),
            "width": max(xs) - min(xs) + 1,
            "height": max(ys) - min(ys) + 1,
        }

    def _estimate_perimeter(self, component: List[tuple], shape: tuple) -> float:
        """Estima el perímetro de un componente."""
        pixel_set = set(component)
        perimeter = 0
        for y, x in component:
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if (ny, nx) not in pixel_set:
                    perimeter += 1
        return perimeter

    def _interpret_morphology(self, stats: Dict, predicted_class: str) -> str:
        """Genera interpretación morfológica basada en las mediciones."""
        if stats["count"] == 0:
            return "No se detectaron estructuras suficientes para medición."

        interpretation = []

        if predicted_class == "nanoparticles":
            interpretation.append(
                f"Se detectaron {stats['count']} nanopartículas con diámetro "
                f"equivalente promedio de {stats['diameter_mean_nm']:.0f} ± "
                f"{stats['diameter_std_nm']:.0f} nm."
            )
            if stats["circularity_mean"] > 0.7:
                interpretation.append(
                    "La alta circularidad media indica morfología "
                    "predominantemente esférica, consistente con nanopartículas 0D."
                )
            else:
                interpretation.append(
                    "La circularidad moderada sugiere formas irregulares o aglomerados."
                )
        elif predicted_class == "nanowires":
            interpretation.append(
                f"Se detectaron {stats['count']} nanohilos con longitud "
                f"característica promedio de {stats['diameter_mean_nm']:.0f} nm."
            )
            if stats["aspect_ratio_mean"] > 3:
                interpretation.append(
                    f"El alto aspect ratio medio ({stats['aspect_ratio_mean']:.1f}) "
                    "confirma morfología elongada tipo 1D."
                )
            else:
                interpretation.append(
                    "El aspect ratio sugiere fragmentos o secciones transversales."
                )
        else:
            interpretation.append(
                f"Se detectaron {stats['count']} estructuras. "
                f"Tamaño promedio: {stats['diameter_mean_nm']:.0f} nm."
            )

        return " ".join(interpretation)
