"""
Agente Visualizador — Grad-CAM para interpretabilidad del clasificador SEM.
Genera mapas de calor que muestran qué regiones de la imagen activan la clasificación.
"""
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from typing import Dict, Any, Tuple
import base64
import io

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMAGENET_MEAN, IMAGENET_STD, IMAGE_SIZE


class GradCAM:
    """Implementación de Grad-CAM para ResNet-18."""

    def __init__(self, model, target_layer):
        self.model = model
        self.gradients = None
        self.activations = None
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, input_tensor, target_class=None):
        """Genera mapa Grad-CAM."""
        self.model.eval()
        output = self.model(input_tensor)

        if target_class is None:
            target_class = output.argmax(dim=1).item()

        self.model.zero_grad()
        one_hot = torch.zeros_like(output)
        one_hot[0, target_class] = 1.0
        output.backward(gradient=one_hot)

        weights = self.gradients.mean(dim=[2, 3], keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = F.relu(cam)
        cam = F.interpolate(
            cam, size=input_tensor.shape[2:],
            mode="bilinear", align_corners=False,
        )
        cam = cam.squeeze()
        if cam.max() > 0:
            cam = (cam - cam.min()) / (cam.max() - cam.min())

        probs = F.softmax(output, dim=1)[0].detach().cpu().numpy()
        return cam.cpu().numpy(), target_class, probs


class VisualizerAgent:
    """Agente que genera visualizaciones Grad-CAM para imágenes SEM."""

    def __init__(self, model, device):
        self.model = model
        self.device = device
        # Grad-CAM en la última capa convolucional de ResNet-18
        self.grad_cam = GradCAM(model, model.layer4[-1])

    def visualize(self, image: Image.Image, transform) -> Dict[str, Any]:
        """
        Genera visualización Grad-CAM para la imagen.

        Returns:
            dict con heatmap_base64, overlay_base64, activations info.
        """
        img_rgb = image.convert("RGB").resize((IMAGE_SIZE, IMAGE_SIZE))
        tensor = transform(img_rgb).unsqueeze(0).to(self.device)

        # Generar Grad-CAM
        cam, pred_class, probs = self.grad_cam.generate(tensor)

        # Crear heatmap con colormap jet manual
        heatmap_colored = self._apply_jet_colormap(cam)
        heatmap_img = Image.fromarray(heatmap_colored)

        # Crear overlay sobre la imagen original
        img_array = np.array(img_rgb)
        overlay = self._create_overlay(img_array, heatmap_colored, alpha=0.4)
        overlay_img = Image.fromarray(overlay)

        # Crear imagen de la original redimensionada
        original_b64 = self._pil_to_base64(img_rgb)

        # Análisis de regiones de activación
        activation_analysis = self._analyze_activations(cam)

        return {
            "original_base64": original_b64,
            "heatmap_base64": self._pil_to_base64(heatmap_img),
            "overlay_base64": self._pil_to_base64(overlay_img),
            "activation_analysis": activation_analysis,
        }

    def _apply_jet_colormap(self, cam: np.ndarray) -> np.ndarray:
        """Aplica colormap jet a un mapa de calor [0,1] → RGB."""
        h, w = cam.shape
        colored = np.zeros((h, w, 3), dtype=np.uint8)

        for i in range(h):
            for j in range(w):
                v = cam[i, j]
                r, g, b = self._jet_color(v)
                colored[i, j] = [r, g, b]

        return colored

    def _jet_color(self, v: float) -> Tuple[int, int, int]:
        """Convierte valor [0,1] a color jet RGB."""
        v = max(0.0, min(1.0, v))
        if v < 0.125:
            r, g, b = 0, 0, 0.5 + v * 4
        elif v < 0.375:
            r, g, b = 0, (v - 0.125) * 4, 1
        elif v < 0.625:
            r, g, b = (v - 0.375) * 4, 1, 1 - (v - 0.375) * 4
        elif v < 0.875:
            r, g, b = 1, 1 - (v - 0.625) * 4, 0
        else:
            r, g, b = 1 - (v - 0.875) * 4, 0, 0
        return (
            int(max(0, min(255, r * 255))),
            int(max(0, min(255, g * 255))),
            int(max(0, min(255, b * 255))),
        )

    def _create_overlay(
        self, img: np.ndarray, heatmap: np.ndarray, alpha: float = 0.4
    ) -> np.ndarray:
        """Superpone heatmap sobre imagen con transparencia."""
        h, w = img.shape[:2]
        # Redimensionar heatmap si es necesario
        if heatmap.shape[:2] != (h, w):
            heatmap_pil = Image.fromarray(heatmap).resize((w, h))
            heatmap = np.array(heatmap_pil)
        overlay = ((1 - alpha) * img + alpha * heatmap).astype(np.uint8)
        return overlay

    def _pil_to_base64(self, img: Image.Image) -> str:
        """Convierte imagen PIL a string base64."""
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def _analyze_activations(self, cam: np.ndarray) -> Dict[str, Any]:
        """Analiza las regiones de mayor activación."""
        # Umbral alto para regiones de interés
        high_activation = cam > 0.7
        medium_activation = (cam > 0.4) & (cam <= 0.7)

        total_pixels = cam.shape[0] * cam.shape[1]
        high_pct = high_activation.sum() / total_pixels * 100
        medium_pct = medium_activation.sum() / total_pixels * 100

        # Centro de masa de las activaciones altas
        if high_activation.sum() > 0:
            ys, xs = np.where(high_activation)
            center_y = ys.mean() / cam.shape[0]
            center_x = xs.mean() / cam.shape[1]
            region = self._describe_region(center_x, center_y)
        else:
            region = "difusa"

        return {
            "high_activation_pct": float(round(high_pct, 1)),
            "medium_activation_pct": float(round(medium_pct, 1)),
            "mean_activation": float(round(cam.mean(), 3)),
            "max_activation": float(round(cam.max(), 3)),
            "primary_region": region,
            "interpretation": (
                f"El modelo enfoca {float(high_pct):.1f}% de la imagen con alta activación, "
                f"concentrada en la región {region}. "
                f"Activación media global: {float(cam.mean()):.2f}."
            ),
        }

    def _describe_region(self, cx: float, cy: float) -> str:
        """Describe la región del centro de masa."""
        v = "superior" if cy < 0.33 else ("central" if cy < 0.66 else "inferior")
        h = "izquierda" if cx < 0.33 else ("central" if cx < 0.66 else "derecha")
        if v == "central" and h == "central":
            return "central"
        return f"{v}-{h}"
