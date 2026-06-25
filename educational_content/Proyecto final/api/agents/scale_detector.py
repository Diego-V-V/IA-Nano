"""
Agente Detector de Escala — Autocalibración de barra de escala en imágenes SEM.

Estrategia de detección:
1. Buscar la barra de escala blanca horizontal en la franja inferior de la imagen.
2. Medir la longitud de la barra en píxeles.
3. Intentar leer el texto asociado (ej. "200 nm", "1 μm") usando OCR o heurísticas.
4. Calcular la escala nm/pixel.
5. Si falla, retorna la escala por defecto (10 nm/px para el dataset NFFA-EUROPE).
"""
import numpy as np
from PIL import Image
from typing import Tuple, Optional, Dict, Any
import re
import math

# Intentar importar OpenCV
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

# Intentar importar pytesseract (OCR)
try:
    import pytesseract
    HAS_TESSERACT = True
    # Buscar el binario de Tesseract en rutas comunes de Windows
    import shutil
    _tess_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    _tess_found = shutil.which("tesseract")
    if _tess_found:
        pytesseract.pytesseract.tesseract_cmd = _tess_found
    else:
        for p in _tess_paths:
            import os
            if os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
                _tess_found = p
                break
    if not _tess_found:
        HAS_TESSERACT = False
except ImportError:
    HAS_TESSERACT = False


# Unidades SEM comunes y su equivalencia en nanómetros
UNIT_TO_NM = {
    "nm": 1.0,
    "μm": 1000.0,
    "um": 1000.0,
    "µm": 1000.0,
    "mm": 1_000_000.0,
}

# Patrón regex para detectar texto de escala: "200 nm", "1 μm", "500nm", etc.
SCALE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(nm|μm|um|µm|mm)",
    re.IGNORECASE
)


class ScaleBarDetector:
    """
    Detecta automáticamente la barra de escala en imágenes SEM
    y calcula la escala nm/pixel para calibrar las mediciones.
    """

    DEFAULT_SCALE = 10.0  # nm/px por defecto para NFFA-EUROPE

    def __init__(self):
        self.method_used = "default"

    def detect_scale(self, image: Image.Image) -> Dict[str, Any]:
        """
        Detecta la escala de la imagen SEM.

        Returns:
            dict con:
                - nm_per_px: escala en nm por píxel
                - method: método utilizado ("ocr", "bar_detection", "default")
                - bar_length_px: longitud de la barra detectada en píxeles (si aplica)
                - scale_text: texto de escala detectado (si aplica)
                - confidence: nivel de confianza ("high", "medium", "low")
        """
        result = {
            "nm_per_px": self.DEFAULT_SCALE,
            "method": "default",
            "bar_length_px": None,
            "scale_text": None,
            "confidence": "low",
            "details": "Usando escala por defecto (10 nm/px, calibración NFFA-EUROPE).",
        }

        if not HAS_CV2:
            result["details"] = "OpenCV no disponible. Usando escala por defecto."
            return result

        # Convertir PIL → OpenCV
        img_array = np.array(image.convert("RGB"))
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # ── Paso 1: Aislar la franja inferior de la imagen (donde está la barra) ──
        # La barra de escala SEM típicamente ocupa el 15-20% inferior
        bottom_fraction = 0.20
        roi_y_start = int(h * (1 - bottom_fraction))
        roi = gray[roi_y_start:, :]
        roi_color = img_cv[roi_y_start:, :]

        # ── Paso 2: Detectar la barra blanca horizontal ──
        bar_info = self._detect_white_bar(roi, w)

        if bar_info is None:
            # Intentar con un ROI más amplio (25%)
            roi_y_start = int(h * 0.75)
            roi = gray[roi_y_start:, :]
            roi_color = img_cv[roi_y_start:, :]
            bar_info = self._detect_white_bar(roi, w)

        if bar_info is not None:
            bar_length_px = bar_info["length_px"]
            result["bar_length_px"] = bar_length_px

            # ── Paso 3: Intentar leer el texto de escala ──
            scale_value_nm = None

            # 3a. OCR si Tesseract está disponible
            if HAS_TESSERACT:
                scale_value_nm, scale_text = self._ocr_scale_text(roi_color)
                if scale_value_nm:
                    result["scale_text"] = scale_text
                    result["method"] = "ocr"

            # 3b. Heurística basada en la longitud de la barra
            if scale_value_nm is None:
                scale_value_nm, scale_text = self._heuristic_scale(
                    bar_length_px, w
                )
                if scale_value_nm:
                    result["scale_text"] = scale_text
                    result["method"] = "bar_heuristic"

            # ── Paso 4: Calcular nm/px ──
            if scale_value_nm and bar_length_px > 0:
                nm_per_px = scale_value_nm / bar_length_px
                # Sanity check: la escala debería estar entre 0.1 y 500 nm/px
                if 0.1 <= nm_per_px <= 500:
                    result["nm_per_px"] = round(nm_per_px, 3)
                    result["confidence"] = "high" if result["method"] == "ocr" else "medium"
                    result["details"] = (
                        f"Barra detectada: {bar_length_px} px → "
                        f"{scale_text}. Escala: {nm_per_px:.2f} nm/px."
                    )
                else:
                    result["details"] = (
                        f"Barra detectada ({bar_length_px} px) pero escala "
                        f"calculada fuera de rango ({nm_per_px:.2f} nm/px). "
                        f"Usando escala por defecto."
                    )
            else:
                result["details"] = (
                    f"Barra detectada ({bar_length_px} px) pero no se pudo "
                    f"determinar el valor de escala. Usando escala por defecto."
                )
        else:
            result["details"] = (
                "No se detectó barra de escala en la imagen. "
                "Usando escala por defecto (10 nm/px)."
            )

        return result

    def _detect_white_bar(
        self, roi_gray: np.ndarray, full_width: int
    ) -> Optional[Dict]:
        """
        Detecta la barra de escala blanca horizontal en el ROI inferior.
        """
        h_roi, w_roi = roi_gray.shape

        # Umbralizar para encontrar píxeles brillantes (la barra de escala es blanca)
        thresh_value = max(200, int(np.percentile(roi_gray, 95)))
        _, binary = cv2.threshold(roi_gray, thresh_value, 255, cv2.THRESH_BINARY)

        # Operación morfológica: dilatar horizontalmente para unir segmentos de barra
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
        dilated = cv2.dilate(binary, kernel_h, iterations=2)

        # Encontrar contornos
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Filtrar candidatos a barra de escala:
        # - Debe ser horizontal (ancho >> alto)
        # - Longitud entre 5% y 50% del ancho de la imagen
        # - Alto menor a 15 px (barra delgada)
        candidates = []
        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            if bh > 12:
                continue  # Demasiado alto para ser una barra
            if bw < full_width * 0.03:
                continue  # Demasiado corto
            if bw > full_width * 0.55:
                continue  # Demasiado largo (probablemente borde)
            aspect = bw / (bh + 1e-8)
            if aspect < 4:
                continue  # No es lo suficientemente horizontal

            candidates.append({
                "x": x, "y": y,
                "length_px": bw,
                "height_px": bh,
                "aspect": aspect,
            })

        if not candidates:
            return None

        # Seleccionar la barra más probable (la más horizontal y con longitud razonable)
        candidates.sort(key=lambda c: c["aspect"], reverse=True)
        best = candidates[0]

        return best

    def _ocr_scale_text(
        self, roi_color: np.ndarray
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        Usa OCR (Tesseract) para leer el texto de la barra de escala.
        """
        try:
            # Pre-procesar para OCR: invertir colores (texto blanco sobre negro)
            gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

            # OCR con configuración para texto corto
            text = pytesseract.image_to_string(
                binary,
                config="--psm 7 -c tessedit_char_whitelist=0123456789.nmμuµmM "
            )

            # Buscar patrón de escala
            match = SCALE_PATTERN.search(text)
            if match:
                value = float(match.group(1))
                unit = match.group(2).lower()
                nm_value = value * UNIT_TO_NM.get(unit, 1.0)
                scale_text = f"{value} {match.group(2)}"
                return nm_value, scale_text

        except Exception as e:
            print(f"  [ScaleDetector] OCR error: {e}")

        return None, None

    def _heuristic_scale(
        self, bar_length_px: int, image_width: int
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        Estima el valor de la barra de escala usando heurísticas basadas
        en la proporción de la barra respecto al ancho de la imagen.

        En imágenes SEM típicas (1024x768 o 512x512):
        - Barra ~5% del ancho → suele ser 100 nm
        - Barra ~10% del ancho → suele ser 200 nm
        - Barra ~15% del ancho → suele ser 500 nm
        - Barra ~20% del ancho → suele ser 1 μm
        - Barra ~25%+ del ancho → suele ser 2 μm o más
        """
        ratio = bar_length_px / image_width

        # Tabla de heurísticas basada en proporciones comunes de SEM
        scale_table = [
            (0.03, 50, "~50 nm (estimado)"),
            (0.06, 100, "~100 nm (estimado)"),
            (0.10, 200, "~200 nm (estimado)"),
            (0.15, 500, "~500 nm (estimado)"),
            (0.22, 1000, "~1 μm (estimado)"),
            (0.30, 2000, "~2 μm (estimado)"),
            (0.40, 5000, "~5 μm (estimado)"),
            (1.00, 10000, "~10 μm (estimado)"),
        ]

        for max_ratio, nm_value, text in scale_table:
            if ratio <= max_ratio:
                return float(nm_value), text

        return None, None
