"""
Agente Clasificador — ResNet-18 fine-tuned para SEM.
Clasifica imágenes SEM en: nanopartículas (0D) vs nanohilos (1D).
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
from typing import Dict, Any

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    MODEL_PATH, IMAGE_SIZE, NUM_CLASSES, CLASSES,
    CLASS_LABELS, IMAGENET_MEAN, IMAGENET_STD,
)


class ClassifierAgent:
    """Agente que clasifica imágenes SEM usando ResNet-18 pre-entrenado."""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()
        self.transform = transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])

    def _load_model(self) -> nn.Module:
        """Carga el modelo ResNet-18 con pesos entrenados."""
        model = models.resnet18(weights=None)
        model.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(512, NUM_CLASSES),
        )
        if MODEL_PATH.exists():
            state_dict = torch.load(
                MODEL_PATH, map_location=self.device, weights_only=True
            )
            model.load_state_dict(state_dict)
            print(f"✓ Modelo cargado: {MODEL_PATH.name}")
        else:
            print(f"⚠ Modelo no encontrado: {MODEL_PATH}")
        model = model.to(self.device)
        model.eval()
        return model

    def classify(self, image: Image.Image) -> Dict[str, Any]:
        """
        Clasifica una imagen SEM.

        Returns:
            dict con predicted_class, label, confidence, probabilities
        """
        # Preprocesar
        img_rgb = image.convert("RGB")
        tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)

        # Inferencia
        with torch.no_grad():
            outputs = self.model(tensor)
            probs = F.softmax(outputs, dim=1)[0]
            confidence, predicted = probs.max(0)

        pred_idx = predicted.item()
        pred_class = CLASSES[pred_idx]

        return {
            "predicted_class": pred_class,
            "label": CLASS_LABELS[pred_class],
            "confidence": round(confidence.item(), 4),
            "probabilities": {
                CLASSES[i]: round(probs[i].item(), 4) for i in range(NUM_CLASSES)
            },
            "device": str(self.device),
        }

    def get_model(self) -> nn.Module:
        """Retorna el modelo para uso externo (Grad-CAM)."""
        return self.model

    def get_transform(self) -> transforms.Compose:
        """Retorna las transformaciones para uso externo."""
        return self.transform
