"""Fix Section 3 markdown cell in the notebook by rewriting it with proper formatting"""
import json
import os

path = os.path.join(
    r"c:\IA Nanotecnologia" if False else "c:\\IA Nanotecnolog\u00eda",
    "Antigravity-Nano-Research-Multiagentic-Core-main",
    "educational_content",
    "unit_03_ml_nanomaterials",
    "Investigacion_Unidad3_Secciones_0_a_03.ipynb"
)

nb = json.load(open(path, encoding='utf-8'))

# The Section 3 cell is cell index 7
# Let's replace it with properly formatted source lines
new_source = [
    "---\n",
    "\n",
    "# Seccion 3: Regresion vs Clasificacion - Analisis Comparativo\n",
    "\n",
    "## 3.1 Definiciones Formales\n",
    "\n",
    "### Regresion\n",
    "\n",
    "La variable objetivo es **continua**: $y \\in \\mathbb{R}$\n",
    "\n",
    "$$\\hat{y} = f(\\mathbf{x}; \\boldsymbol{\\theta}), \\quad \\hat{y} \\in \\mathbb{R}$$\n",
    "\n",
    "**Funcion de perdida tipica - MSE (Error Cuadratico Medio):**\n",
    "\n",
    "$$\\mathcal{L}_{\\text{MSE}} = \\frac{1}{N}\\sum_{i=1}^{N}(y_i - \\hat{y}_i)^2$$\n",
    "\n",
    "**Metricas de evaluacion:**\n",
    "\n",
    "- $R^2 = 1 - \\frac{\\sum(y_i - \\hat{y}_i)^2}{\\sum(y_i - \\bar{y})^2}$ - proporcion de varianza explicada\n",
    "\n",
    "- $\\text{MAE} = \\frac{1}{N}\\sum|y_i - \\hat{y}_i|$ - error absoluto medio\n",
    "\n",
    "- $\\text{RMSE} = \\sqrt{\\frac{1}{N}\\sum(y_i - \\hat{y}_i)^2}$ - raiz del error cuadratico medio\n",
    "\n",
    "### Clasificacion\n",
    "\n",
    "La variable objetivo es **discreta**: $y \\in \\{C_1, C_2, \\ldots, C_k\\}$\n",
    "\n",
    "$$\\hat{y} = \\arg\\max_{k} P(C_k | \\mathbf{x}; \\boldsymbol{\\theta})$$\n",
    "\n",
    "**Funcion de perdida tipica - Cross-Entropy:**\n",
    "\n",
    "$$\\mathcal{L}_{\\text{CE}} = -\\sum_{i=1}^{N}\\sum_{k=1}^{K} y_{ik} \\log(\\hat{y}_{ik})$$\n",
    "\n",
    "**Metricas de evaluacion:**\n",
    "\n",
    "- Accuracy $= \\frac{\\text{predicciones correctas}}{\\text{total predicciones}}$\n",
    "\n",
    "- Precision $= \\frac{TP}{TP + FP}$, Recall $= \\frac{TP}{TP + FN}$\n",
    "\n",
    "- $F_1 = 2 \\cdot \\frac{\\text{Precision} \\cdot \\text{Recall}}{\\text{Precision} + \\text{Recall}}$\n",
    "\n",
    "---\n",
    "\n",
    "## 3.2 Cuando usar cada uno en Nanotecnologia?\n",
    "\n",
    "| Criterio | Regresion | Clasificacion |\n",
    "|----------|-----------|---------------|\n",
    "| **Variable objetivo** | Valor numerico continuo | Categoria discreta |\n",
    "| **Ejemplo nano** | Predecir $E_g = 2.43$ eV, $T_m = 1337$ K | Identificar fase FCC / BCC / HCP |\n",
    "| **Pregunta cientifica** | Cuanto vale la propiedad X? | A que categoria pertenece? |\n",
    "| **Funcion de perdida** | MSE, MAE, Huber | Cross-Entropy, Hinge |\n",
    "| **Metricas** | R2, MAE, RMSE | Accuracy, F1, AUC-ROC |\n",
    "| **Aplicaciones** | Energia de formacion, bandgap, modulo elastico | Estabilidad (si/no), tipo de estructura, conductor/aislante |\n",
    "\n",
    "> **Regla practica en Ciencia de Materiales:**\n",
    "\n",
    "> - Si la respuesta es un **numero** -> **Regresion**\n",
    "\n",
    "> - Si la respuesta es una **etiqueta/categoria** -> **Clasificacion**\n",
    "\n",
    "> - Si tienes un valor continuo pero necesitas una decision -> discretiza y usa **clasificacion**"
]

nb['cells'][7]['source'] = new_source

# Save
with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("OK - Section 3 cell fixed")
print(f"New source has {len(new_source)} lines")
