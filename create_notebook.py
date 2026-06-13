"""Script to generate the research Jupyter notebook for Unit 3 Sections 0-0.3"""
import json

def md(source):
    """Create a markdown cell"""
    lines = source.split("\n")
    # Add newlines to all but last line (same as code cells)
    formatted = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "markdown", "metadata": {}, "source": formatted}

def code(source):
    """Create a code cell"""
    lines = source.split("\n")
    # Add newlines to all but last line
    formatted = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "code", "metadata": {}, "source": formatted, "outputs": [], "execution_count": None}

cells = []

# ============ TITLE ============
cells.append(md(
"""# 🔬 Investigación a Profundidad: Fundamentos de Machine Learning para Nanotecnología
## Unidad 3 — Secciones 0.1 a 0.3

**Curso:** Modelado, Simulación e IA en Nanotecnología  
**Nivel:** Intermedio  
**Autor:** Estudiante de Nanotecnología

---

> 📖 **Contenido de esta investigación:**
> - Sección 1: ¿Por qué Machine Learning en Nanotecnología?
> - Sección 2: Tipos de Aprendizaje (Supervisado, No Supervisado, Refuerzo)
> - Sección 3: Regresión vs Clasificación — Análisis Comparativo
> - Sección 4: Catálogo de Modelos con Fundamentos Matemáticos
> - Sección 5: Demostración Práctica y Conclusiones

> 📊 **Criterios de Evaluación:**
> 1. Rigor Matemático — Uso correcto de ecuaciones
> 2. Conexión con la Carrera — Ejemplos en Nanotecnología / Ciencia de Materiales
> 3. Calidad del Código — Limpio, comentado y funcional
> 4. Análisis Comparativo — Cuándo usar regresión frente a clasificación"""
))

# ============ SETUP ============
cells.append(md(
"""---
# ⚙️ Celda de Setup"""
))

cells.append(code(
"""# ============================================================
# SETUP — Importaciones y configuracion
# ============================================================
import sys, subprocess

def _install(pkg):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

# Verificar seaborn
try:
    import seaborn as sns
except ImportError:
    print("Instalando seaborn...")
    _install('seaborn')
    import seaborn as sns

# Verificar scikit-learn
try:
    import sklearn
except ImportError:
    print("Instalando scikit-learn...")
    _install('scikit-learn')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             accuracy_score, f1_score, classification_report,
                             confusion_matrix)
from sklearn.linear_model import Ridge, Lasso
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Configuracion de graficos
matplotlib.rcParams['figure.dpi'] = 120
matplotlib.rcParams['font.size'] = 11
sns.set_style("whitegrid")
np.random.seed(42)

print("Entorno listo. Todas las dependencias cargadas correctamente.")"""
))

# ============ SECTION 1 ============
cells.append(md(
r"""---

# 📚 Sección 1: ¿Por qué Machine Learning en Nanotecnología?

## 1.1 El Problema de Escala en la Ciencia de Materiales

El diseño de nuevos nanomateriales enfrenta un desafío fundamental: **el espacio de búsqueda es astronómicamente grande**. La cantidad de compuestos inorgánicos posibles se estima en el orden de $10^{60}$, mientras que los métodos tradicionales de cálculo son extremadamente costosos:

| Método | Tiempo por estructura | Precisión |
|--------|----------------------|-----------|
| DFT (*Density Functional Theory*) | 1–48 horas | Alta (meV/átomo) |
| Dinámica Molecular (MD) | Horas–días | Media |
| Síntesis experimental | Semanas–meses | Variable |

### El cuello de botella computacional

Para calcular la energía total de un sistema cuántico, se resuelve la ecuación de Kohn-Sham:

$$\left[-\frac{\hbar^2}{2m}\nabla^2 + V_{\text{eff}}(\mathbf{r})\right]\psi_i(\mathbf{r}) = \epsilon_i \psi_i(\mathbf{r})$$

donde $V_{\text{eff}}$ incluye los potenciales externo, de Hartree y de intercambio-correlación. Este cálculo escala como $\mathcal{O}(N^3)$ con el número de electrones $N$, lo que lo hace **prohibitivo** para sistemas grandes.

## 1.2 Machine Learning como Solución

La idea central es usar ML como una **función de interpolación inteligente** entrenada sobre datos DFT/MD/experimentales:

$$\text{DFT/MD} \rightarrow \text{Datos} \xrightarrow{\text{ML}} \hat{f}(\mathbf{x}) \approx f_{\text{real}}(\mathbf{x}) \rightarrow \text{Predicción instantánea}$$

El modelo ML aprende la relación entre **descriptores** (composición, estructura, condiciones) y **propiedades** (bandgap, energía de formación, estabilidad) sin resolver las ecuaciones cuánticas directamente.

### Ventajas clave:
- **Velocidad**: predicción en milisegundos vs horas de DFT
- **Escalabilidad**: screening de millones de candidatos
- **Descubrimiento**: identificar patrones no evidentes en datos complejos

## 1.3 Casos de Éxito Reales

| Proyecto | Año | Logro | Técnica ML |
|----------|-----|-------|------------|
| **AlphaFold 2** (DeepMind) | 2021 | Predicción de estructura de proteínas con precisión atómica | Deep Learning |
| **GNoME** (Google) | 2023 | Descubrió 2.2 millones de nuevos materiales estables | GNN |
| **Behler-Parrinello NNP** | 2007+ | Potenciales interatómicos con precisión DFT a velocidad clásica | Redes Neuronales |
| **Diseño de catalizadores** | 2020+ | Predicción de energías de adsorción en aleaciones | Random Forest, GBR |"""
))

cells.append(code(
"""# ============================================================
# DEMOSTRACIÓN 1: Por qué necesitamos ML en nanotecnología
# Generamos un dataset sintético que simula propiedades de
# nanopartículas metálicas (inspirado en datos reales)
# ============================================================

# Simulamos un espacio de materiales con propiedades correlacionadas
n_muestras = 500

# Descriptores de nanopartículas
radio_nm = np.random.uniform(1, 50, n_muestras)          # Radio (nm)
composicion_Au = np.random.uniform(0, 1, n_muestras)      # Fracción de Au
temperatura_K = np.random.uniform(200, 800, n_muestras)    # Temperatura (K)
num_atomos = (4/3 * np.pi * (radio_nm * 10)**3 * 0.059)   # Estimación de átomos

# Propiedad objetivo: Energía de formación (eV/átomo) — modelo físico simplificado
# Incluye contribución de superficie (1/r), composición, y ruido
E_formacion = (
    -3.5 * composicion_Au                     # Contribución composicional
    - 0.8 * (1 - composicion_Au)              # Contribución del segundo metal
    + 2.0 / radio_nm                          # Efecto de tamaño (energía superficial)
    + 0.001 * temperatura_K                   # Efecto térmico
    + np.random.normal(0, 0.1, n_muestras)    # Ruido experimental
)

# Crear DataFrame
df_nano = pd.DataFrame({
    'Radio (nm)': radio_nm,
    'Fracción Au': composicion_Au,
    'Temperatura (K)': temperatura_K,
    'N° átomos (aprox.)': num_atomos.astype(int),
    'E_formación (eV/átomo)': E_formacion
})

print("=" * 60)
print("📊 DATASET SINTÉTICO DE NANOPARTÍCULAS METÁLICAS")
print("=" * 60)
print(f"\\nMuestras: {n_muestras}")
print(f"Features: {list(df_nano.columns[:-1])}")
print(f"Target: {df_nano.columns[-1]}")
print(f"\\n{df_nano.describe().round(3)}")

# Visualización
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Radio vs Energía
axes[0].scatter(df_nano['Radio (nm)'], df_nano['E_formación (eV/átomo)'],
                c=df_nano['Fracción Au'], cmap='viridis', alpha=0.6, s=15)
axes[0].set_xlabel('Radio (nm)')
axes[0].set_ylabel('E_formación (eV/átomo)')
axes[0].set_title('Efecto del tamaño')
cb = plt.colorbar(axes[0].collections[0], ax=axes[0])
cb.set_label('Fracción Au')

# Composición vs Energía
axes[1].scatter(df_nano['Fracción Au'], df_nano['E_formación (eV/átomo)'],
                c=df_nano['Radio (nm)'], cmap='plasma', alpha=0.6, s=15)
axes[1].set_xlabel('Fracción Au')
axes[1].set_ylabel('E_formación (eV/átomo)')
axes[1].set_title('Efecto de la composición')
cb = plt.colorbar(axes[1].collections[0], ax=axes[1])
cb.set_label('Radio (nm)')

# Temperatura vs Energía
axes[2].scatter(df_nano['Temperatura (K)'], df_nano['E_formación (eV/átomo)'],
                c=df_nano['Fracción Au'], cmap='coolwarm', alpha=0.6, s=15)
axes[2].set_xlabel('Temperatura (K)')
axes[2].set_ylabel('E_formación (eV/átomo)')
axes[2].set_title('Efecto de la temperatura')
cb = plt.colorbar(axes[2].collections[0], ax=axes[2])
cb.set_label('Fracción Au')

plt.suptitle('Motivación: Relaciones complejas en las propiedades de nanopartículas',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

print("\\n💡 Estas relaciones no lineales entre descriptores y propiedades")
print("   son exactamente el tipo de problemas donde ML supera a los métodos analíticos.")"""
))

# ============ SECTION 2 ============
cells.append(md(
r"""---

# 📚 Sección 2: Tipos de Aprendizaje

## 2.1 Aprendizaje Supervisado

### Definición formal

El aprendizaje supervisado busca aprender una función $f$ que mapea entradas a salidas a partir de un conjunto de datos **etiquetados**:

$$f: \mathbf{X} \rightarrow \mathbf{y}, \quad \text{dado } \mathcal{D} = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \ldots, (\mathbf{x}_N, y_N)\}$$

El objetivo es encontrar los parámetros $\boldsymbol{\theta}$ que minimizan una **función de pérdida** $\mathcal{L}$:

$$\boldsymbol{\theta}^* = \arg\min_{\boldsymbol{\theta}} \frac{1}{N} \sum_{i=1}^{N} \mathcal{L}\left(y_i, f_{\boldsymbol{\theta}}(\mathbf{x}_i)\right)$$

### Funciones de pérdida comunes:

| Tipo | Función de pérdida | Expresión |
|------|-------------------|-----------|
| **Regresión** | MSE (Error Cuadrático Medio) | $\mathcal{L} = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat{y}_i)^2$ |
| **Clasificación** | Cross-Entropy | $\mathcal{L} = -\sum_{i=1}^{N}\left[y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)\right]$ |

### Aplicaciones en Nanotecnología:
- **Predecir bandgap** ($E_g$) de semiconductores a partir de la composición
- **Predecir temperatura de fusión** ($T_m$) de aleaciones
- **Predecir energía de adsorción** de moléculas en superficies catalíticas
- **Predecir actividad catalítica** de nanopartículas

**Requisito fundamental:** un dataset etiquetado, donde las propiedades han sido calculadas con DFT o medidas experimentalmente.

---

## 2.2 Aprendizaje No Supervisado

### Definición formal

El aprendizaje no supervisado encuentra **estructura oculta** en datos **sin etiquetas**:

$$\text{Dado } \mathcal{D} = \{\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_N\}, \quad \text{encontrar patrones o agrupaciones}$$

No hay una variable objetivo $y$. El modelo descubre por sí mismo las relaciones.

### Técnicas principales:
- **Clustering** (K-Means, DBSCAN): agrupar materiales similares
- **Reducción de dimensionalidad** (PCA, t-SNE): visualizar espacios de alta dimensión
- **Detección de anomalías**: identificar muestras atípicas

### Aplicaciones en Nanotecnología:
- Clustering de fases cristalinas
- Reducción de dimensionalidad de espectros de absorción
- Detección de anomalías en imágenes TEM
- Agrupación de materiales por similitud composicional

---

## 2.3 Aprendizaje por Refuerzo

### Definición formal

Un **agente** interactúa con un **entorno** y aprende una **política óptima** $\pi^*$ que maximiza la recompensa acumulada:

$$\pi^*(a|s) = \arg\max_{\pi} \mathbb{E}\left[\sum_{t=0}^{T} \gamma^t r_t \right]$$

donde:
- $s$ = estado del sistema
- $a$ = acción del agente
- $r_t$ = recompensa en el paso $t$
- $\gamma \in [0, 1]$ = factor de descuento

### Aplicaciones en Nanotecnología:
- Optimización de rutas de síntesis
- Diseño molecular iterativo
- Control de procesos de nanofabricación

---

## 2.4 Tabla Comparativa

| Paradigma | Datos | Salida | Ejemplo en Nanotecnología |
|-----------|-------|--------|---------------------------|
| **Supervisado** | $(\mathbf{x}, y)$ etiquetados | $\hat{y}$ (predicción) | Predecir $E_g$ del material |
| **No supervisado** | $\mathbf{x}$ sin etiqueta | Grupos / representaciones | Clustering de estructuras cristalinas |
| **Refuerzo** | (estado, acción, recompensa) | Política $\pi$ | Ruta de síntesis óptima |"""
))

cells.append(code(
"""# ============================================================
# DEMOSTRACIÓN 2: Aprendizaje No Supervisado — K-Means
# Clustering de "fases cristalinas" a partir de descriptores
# ============================================================

# Generar datos sintéticos que simulan 3 fases cristalinas
np.random.seed(42)
n_per_phase = 100

# Fase FCC: alta coordinación, baja distancia interatómica
fcc_coord = np.random.normal(12, 0.5, n_per_phase)
fcc_dist = np.random.normal(2.55, 0.05, n_per_phase)

# Fase BCC: coordinación intermedia, distancia mayor
bcc_coord = np.random.normal(8, 0.5, n_per_phase)
bcc_dist = np.random.normal(2.87, 0.05, n_per_phase)

# Fase HCP: similar a FCC pero con diferente empaquetamiento
hcp_coord = np.random.normal(12, 0.5, n_per_phase)
hcp_dist = np.random.normal(2.70, 0.05, n_per_phase)

# Combinar datos
coords = np.concatenate([fcc_coord, bcc_coord, hcp_coord])
dists = np.concatenate([fcc_dist, bcc_dist, hcp_dist])
X_cluster = np.column_stack([coords, dists])
etiquetas_reales = np.array(['FCC'] * n_per_phase + ['BCC'] * n_per_phase + ['HCP'] * n_per_phase)

# Aplicar K-Means (sin usar las etiquetas — aprendizaje NO supervisado)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Datos reales
colores_reales = {'FCC': '#e74c3c', 'BCC': '#3498db', 'HCP': '#2ecc71'}
for fase in ['FCC', 'BCC', 'HCP']:
    mask = etiquetas_reales == fase
    axes[0].scatter(coords[mask], dists[mask], c=colores_reales[fase],
                    label=fase, alpha=0.6, s=30)
axes[0].set_xlabel('Número de coordinación')
axes[0].set_ylabel('Distancia interatómica (Å)')
axes[0].set_title('Fases cristalinas REALES')
axes[0].legend()

# Clusters K-Means
scatter = axes[1].scatter(coords, dists, c=clusters, cmap='Set1', alpha=0.6, s=30)
axes[1].set_xlabel('Número de coordinación')
axes[1].set_ylabel('Distancia interatómica (Å)')
axes[1].set_title('Clusters descubiertos por K-Means (no supervisado)')
plt.colorbar(scatter, ax=axes[1], label='Cluster ID')

plt.suptitle('Aprendizaje No Supervisado: Descubrimiento de fases cristalinas',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

print("\\n🔬 INTERPRETACIÓN:")
print("   K-Means identifica correctamente los 3 grupos (fases cristalinas)")
print("   SIN necesidad de etiquetas. Esto es útil cuando tenemos datos")
print("   estructurales de simulaciones y queremos descubrir fases automáticamente.")"""
))

# ============ SECTION 3 ============
cells.append(md(
r"""---

# 📚 Sección 3: Regresión vs Clasificación — Análisis Comparativo

## 3.1 Definiciones Formales

### Regresión
La variable objetivo es **continua**: $y \in \mathbb{R}$

$$\hat{y} = f(\mathbf{x}; \boldsymbol{\theta}), \quad \hat{y} \in \mathbb{R}$$

**Función de pérdida típica — MSE (Error Cuadrático Medio):**

$$\mathcal{L}_{\text{MSE}} = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat{y}_i)^2$$

**Métricas de evaluación:**
- $R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$ — proporción de varianza explicada
- $\text{MAE} = \frac{1}{N}\sum|y_i - \hat{y}_i|$ — error absoluto medio
- $\text{RMSE} = \sqrt{\frac{1}{N}\sum(y_i - \hat{y}_i)^2}$ — raíz del error cuadrático medio

### Clasificación
La variable objetivo es **discreta**: $y \in \{C_1, C_2, \ldots, C_k\}$

$$\hat{y} = \arg\max_{k} P(C_k | \mathbf{x}; \boldsymbol{\theta})$$

**Función de pérdida típica — Cross-Entropy:**

$$\mathcal{L}_{\text{CE}} = -\sum_{i=1}^{N}\sum_{k=1}^{K} y_{ik} \log(\hat{y}_{ik})$$

**Métricas de evaluación:**
- Accuracy $= \frac{\text{predicciones correctas}}{\text{total predicciones}}$
- Precision $= \frac{TP}{TP + FP}$, Recall $= \frac{TP}{TP + FN}$
- $F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$

---

## 3.2 ¿Cuándo usar cada uno en Nanotecnología?

| Criterio | Regresión | Clasificación |
|----------|-----------|---------------|
| **Variable objetivo** | Valor numérico continuo | Categoría discreta |
| **Ejemplo nano** | Predecir $E_g = 2.43$ eV, $T_m = 1337$ K | Identificar fase FCC / BCC / HCP |
| **Pregunta científica** | *¿Cuánto vale la propiedad X?* | *¿A qué categoría pertenece?* |
| **Función de pérdida** | MSE, MAE, Huber | Cross-Entropy, Hinge |
| **Métricas** | R², MAE, RMSE | Accuracy, F1, AUC-ROC |
| **Aplicaciones** | Energía de formación, bandgap, módulo elástico | Estabilidad (sí/no), tipo de estructura, conductor/aislante |

> **Regla práctica en Ciencia de Materiales:**
> - Si la respuesta es un **número** → **Regresión**
> - Si la respuesta es una **etiqueta/categoría** → **Clasificación**
> - Si tienes un valor continuo pero necesitas una decisión → discretiza y usa **clasificación**"""
))

cells.append(code(
"""# ============================================================
# DEMOSTRACIÓN 3: Regresión vs Clasificación en Nanotecnología
# Mismo dataset — dos problemas distintos
# ============================================================

# --- Preparar datos ---
# Reutilizamos el dataset de nanopartículas (df_nano)
features = ['Radio (nm)', 'Fracción Au', 'Temperatura (K)']
X = df_nano[features].values

# TARGET DE REGRESIÓN: Energía de formación (continua)
y_reg = df_nano['E_formación (eV/átomo)'].values

# TARGET DE CLASIFICACIÓN: ¿Material estable o inestable?
# Criterio: E_formación < -2.0 eV/átomo → estable
y_clf = (y_reg < -2.0).astype(int)  # 0 = inestable, 1 = estable

# División train/test
X_train, X_test, y_reg_train, y_reg_test = train_test_split(
    X, y_reg, test_size=0.2, random_state=42)
_, _, y_clf_train, y_clf_test = train_test_split(
    X, y_clf, test_size=0.2, random_state=42)

# Escalar features
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

# --- REGRESIÓN: Random Forest ---
rf_reg = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf_reg.fit(X_train_sc, y_reg_train)
y_pred_reg = rf_reg.predict(X_test_sc)

r2 = r2_score(y_reg_test, y_pred_reg)
mae = mean_absolute_error(y_reg_test, y_pred_reg)
rmse = np.sqrt(mean_squared_error(y_reg_test, y_pred_reg))

# --- CLASIFICACIÓN: SVC ---
svc_clf = SVC(kernel='rbf', C=10, gamma='scale', random_state=42)
svc_clf.fit(X_train_sc, y_clf_train)
y_pred_clf = svc_clf.predict(X_test_sc)

acc = accuracy_score(y_clf_test, y_pred_clf)
f1 = f1_score(y_clf_test, y_pred_clf)

# --- Visualización comparativa ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel izquierdo: Regresión
axes[0].scatter(y_reg_test, y_pred_reg, alpha=0.5, s=20, c='#3498db')
lims = [min(y_reg_test.min(), y_pred_reg.min()),
        max(y_reg_test.max(), y_pred_reg.max())]
axes[0].plot(lims, lims, 'r--', lw=2, label='Predicción perfecta')
axes[0].set_xlabel('E_formación real (eV/átomo)')
axes[0].set_ylabel('E_formación predicha (eV/átomo)')
axes[0].set_title(f'REGRESIÓN (Random Forest)\\nR² = {r2:.4f} | MAE = {mae:.4f} eV/átomo')
axes[0].legend()

# Panel derecho: Clasificación — Matriz de confusión
cm = confusion_matrix(y_clf_test, y_pred_clf)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1],
            xticklabels=['Inestable', 'Estable'],
            yticklabels=['Inestable', 'Estable'])
axes[1].set_xlabel('Predicción')
axes[1].set_ylabel('Real')
axes[1].set_title(f'CLASIFICACIÓN (SVC)\\nAccuracy = {acc:.4f} | F1 = {f1:.4f}')

plt.suptitle('Comparación: Regresión vs Clasificación en Nanopartículas',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# Resultados tabulares
print("\\n" + "=" * 60)
print("📊 RESUMEN COMPARATIVO: REGRESIÓN vs CLASIFICACIÓN")
print("=" * 60)
print(f"\\n{'Aspecto':<25} {'Regresión':<20} {'Clasificación':<20}")
print("-" * 65)
print(f"{'Modelo':<25} {'Random Forest':<20} {'SVC (RBF)':<20}")
print(f"{'Target':<25} {'E_formación (cont.)':<20} {'Estable/Inestable':<20}")
print(f"{'Métrica principal':<25} {'R² = ' + f'{r2:.4f}':<20} {'F1 = ' + f'{f1:.4f}':<20}")
print(f"{'Métrica secundaria':<25} {'MAE = ' + f'{mae:.4f}':<20} {'Acc = ' + f'{acc:.4f}':<20}")
print(f"{'Interpretación':<25} {'Valor numérico':<20} {'Decisión binaria':<20}")
print("\\n💡 La regresión da un VALOR PRECISO de la propiedad.")
print("   La clasificación da una DECISIÓN rápida (estable o no).")
print("   Ambos son útiles según la pregunta científica.")"""
))

# ============ SECTION 4 ============
cells.append(md(
r"""---

# 📚 Sección 4: Catálogo de Modelos con Fundamentos Matemáticos

## 4.1 Modelos Supervisados — Regresión

### Ridge Regression (Regresión de Cresta)

Minimiza el MSE con regularización L2 para evitar sobreajuste:

$$\boldsymbol{\theta}^* = \arg\min_{\boldsymbol{\theta}} \left[\sum_{i=1}^{N}(y_i - \mathbf{x}_i^T\boldsymbol{\theta})^2 + \alpha \|\boldsymbol{\theta}\|_2^2\right]$$

- **Hiperparámetro clave:** $\alpha$ (fuerza de regularización)
- **En nano:** línea base para datos con pocos features; útil cuando hay features correlacionadas (como propiedades termodinámicas)

### Lasso Regression

Similar a Ridge pero con regularización L1, que produce **selección de features** (fuerza coeficientes a cero):

$$\boldsymbol{\theta}^* = \arg\min_{\boldsymbol{\theta}} \left[\sum_{i=1}^{N}(y_i - \mathbf{x}_i^T\boldsymbol{\theta})^2 + \alpha \|\boldsymbol{\theta}\|_1\right]$$

- **En nano:** útil para identificar qué descriptores moleculares son realmente relevantes

### Support Vector Regression (SVR)

Busca un hiperplano que contenga el máximo número de puntos dentro de un margen $\epsilon$:

$$\min \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^{N}(\xi_i + \xi_i^*)$$

sujeto a: $|y_i - \mathbf{w}^T\phi(\mathbf{x}_i) - b| \leq \epsilon + \xi_i$

- **Hiperparámetros:** $C$ (regularización), $\epsilon$ (ancho del tubo), kernel, $\gamma$
- **En nano:** funciona bien con alta dimensión y pocos ejemplos

### Random Forest Regressor

Ensemble de $B$ árboles de decisión entrenados con bootstrap:

$$\hat{y} = \frac{1}{B}\sum_{b=1}^{B} T_b(\mathbf{x})$$

- **Hiperparámetros:** `n_estimators` ($B$), `max_depth`, `min_samples_split`
- **En nano:** robusto, maneja muchos features sin sobreajuste

### Gradient Boosting Regressor

Construye árboles secuencialmente, cada uno corrigiendo los errores del anterior:

$$\hat{y}^{(m)} = \hat{y}^{(m-1)} + \eta \cdot T_m(\mathbf{x})$$

donde $\eta$ es la tasa de aprendizaje y $T_m$ se ajusta al **gradiente negativo** de la pérdida.

- **Hiperparámetros:** `learning_rate` ($\eta$), `n_estimators`, `max_depth`
- **En nano:** mayor precisión que Random Forest, pero mayor riesgo de sobreajuste

---

## 4.2 Modelos Supervisados — Clasificación

### SVC (Support Vector Classifier)

Encuentra el hiperplano que maximiza el **margen** entre clases:

$$\min \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^{N}\xi_i$$

sujeto a: $y_i(\mathbf{w}^T\phi(\mathbf{x}_i) + b) \geq 1 - \xi_i$

- **En nano:** fronteras de decisión no lineales con kernel RBF

### KNN (K-Nearest Neighbors)

Clasifica por mayoría de votos de los $k$ vecinos más cercanos:

$$\hat{y} = \text{mode}\{y_j : \mathbf{x}_j \in \mathcal{N}_k(\mathbf{x})\}$$

- **En nano:** simple, no paramétrico, útil para interpolación local

---

## 4.3 Modelos No Supervisados

### K-Means

Minimiza la inercia (suma de distancias al centroide):

$$J = \sum_{k=1}^{K}\sum_{\mathbf{x}_i \in C_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2$$

### PCA (Análisis de Componentes Principales)

Proyecta los datos en las direcciones de máxima varianza:

$$\mathbf{z} = \mathbf{W}^T(\mathbf{x} - \boldsymbol{\mu})$$

donde $\mathbf{W}$ contiene los eigenvectores de la matriz de covarianza.

- **En nano:** visualizar espacios de materiales de alta dimensión

---

## 4.4 Tabla Resumen del Catálogo

| Tipo | Algoritmo | Hiperparámetros clave | Cuándo usar en nano |
|------|-----------|----------------------|---------------------|
| Regresión | Ridge / Lasso | $\alpha$ | Línea base, pocos datos, features correlacionadas |
| Regresión | SVR | $C$, $\epsilon$, kernel, $\gamma$ | Alta dimensión, pocos ejemplos |
| Regresión | KNN Reg. | `n_neighbors`, `metric` | Datos pequeños, interpolación local |
| Regresión | Árbol de Decisión | `max_depth`, `min_samples` | Interpretable, reglas físicas |
| Regresión | Random Forest | `n_estimators`, `max_depth` | Robusto, muchos features |
| Regresión | Gradient Boosting | `learning_rate`, `n_estimators` | Mayor precisión |
| Clasificación | SVC | $C$, kernel, $\gamma$ | Fronteras no lineales |
| Clasificación | Random Forest | igual | Clasificación robusta |
| Clasificación | KNN Clasif. | `n_neighbors` | Simple, no paramétrico |
| No Supervisado | K-Means | $K$ | Agrupar estructuras similares |
| No Supervisado | PCA | `n_components` | Visualizar espacio de materiales |"""
))

cells.append(code(
"""# ============================================================
# DEMOSTRACIÓN 4: Pipeline comparativo de regresores
# Entrenamos 5 modelos sobre los mismos datos y comparamos
# ============================================================

# Preparar datos (reutilizamos X_train_sc, X_test_sc, y_reg_train, y_reg_test)
modelos = {
    'Ridge (α=1.0)': Ridge(alpha=1.0),
    'Lasso (α=0.01)': Lasso(alpha=0.01),
    'SVR (RBF)': SVR(kernel='rbf', C=10, epsilon=0.1),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,
                                                    max_depth=5, random_state=42),
}

resultados = []
predicciones = {}

for nombre, modelo in modelos.items():
    # Entrenar
    modelo.fit(X_train_sc, y_reg_train)
    y_pred = modelo.predict(X_test_sc)
    predicciones[nombre] = y_pred

    # Validación cruzada
    cv_scores = cross_val_score(modelo, X_train_sc, y_reg_train, cv=5, scoring='r2')

    # Métricas en test
    r2_test = r2_score(y_reg_test, y_pred)
    mae_test = mean_absolute_error(y_reg_test, y_pred)
    rmse_test = np.sqrt(mean_squared_error(y_reg_test, y_pred))

    resultados.append({
        'Modelo': nombre,
        'R² (CV)': f"{cv_scores.mean():.4f} ± {cv_scores.std():.4f}",
        'R² (test)': round(r2_test, 4),
        'MAE (test)': round(mae_test, 4),
        'RMSE (test)': round(rmse_test, 4),
    })

# Tabla de resultados
df_resultados = pd.DataFrame(resultados)
print("=" * 80)
print("📊 COMPARACIÓN DE MODELOS DE REGRESIÓN — Predicción de E_formación")
print("=" * 80)
print(f"\\n{df_resultados.to_string(index=False)}")

# Visualización: predicciones de cada modelo
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

colores = ['#e74c3c', '#e67e22', '#9b59b6', '#3498db', '#2ecc71']

for i, (nombre, y_pred) in enumerate(predicciones.items()):
    ax = axes[i]
    r2_val = r2_score(y_reg_test, y_pred)
    mae_val = mean_absolute_error(y_reg_test, y_pred)

    ax.scatter(y_reg_test, y_pred, alpha=0.5, s=15, c=colores[i])
    lims = [min(y_reg_test.min(), y_pred.min()), max(y_reg_test.max(), y_pred.max())]
    ax.plot(lims, lims, 'k--', lw=1.5)
    ax.set_xlabel('Real (eV/átomo)')
    ax.set_ylabel('Predicho (eV/átomo)')
    ax.set_title(f'{nombre}\\nR²={r2_val:.4f} | MAE={mae_val:.4f}')

# Ocultar el sexto panel
axes[5].axis('off')

plt.suptitle('Comparación de 5 Regresores para predicción de E_formación de nanopartículas',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

# Barplot de R²
fig, ax = plt.subplots(figsize=(10, 5))
nombres = [r['Modelo'] for r in resultados]
r2_vals = [r['R² (test)'] for r in resultados]
bars = ax.barh(nombres, r2_vals, color=colores)
ax.set_xlabel('R² (test)')
ax.set_title('Coeficiente de Determinación R² por Modelo', fontweight='bold')
for bar, val in zip(bars, r2_vals):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val:.4f}', va='center', fontsize=10)
ax.set_xlim(0, 1.05)
plt.tight_layout()
plt.show()

print("\\n💡 ANÁLISIS:")
print("   • Los modelos lineales (Ridge, Lasso) capturan bien la relación")
print("     porque el dataset sintético tiene componentes lineales fuertes.")
print("   • Random Forest y Gradient Boosting tienen excelente desempeño")
print("     gracias a su capacidad de capturar relaciones no lineales.")
print("   • SVR también funciona bien con el kernel RBF.")
print("   • En datos REALES de materiales, los modelos de ensemble (RF, GBR)")
print("     suelen ser la mejor opción por su robustez.")"""
))

# ============ SECTION 5 ============
cells.append(md(
r"""---

# 📚 Sección 5: Conclusiones y Reflexiones

## 5.1 Hallazgos Principales

1. **Machine Learning resuelve el cuello de botella computacional** de la nanociencia. Mientras que un cálculo DFT puede tomar horas, un modelo ML predice propiedades en milisegundos una vez entrenado.

2. **Los tres paradigmas de aprendizaje** tienen aplicaciones directas en nanotecnología:
   - *Supervisado*: predicción de propiedades cuando tenemos datos etiquetados (DFT, experimentos)
   - *No supervisado*: descubrimiento de patrones (fases, clusters de materiales)
   - *Refuerzo*: optimización de procesos de síntesis

3. **Regresión y Clasificación** son herramientas complementarias:

| Situación | Enfoque recomendado |
|-----------|-------------------|
| Necesito el **valor exacto** de una propiedad (bandgap, energía) | **Regresión** |
| Necesito **clasificar/categorizar** un material (estable/inestable, fase) | **Clasificación** |
| Tengo un valor continuo pero necesito tomar una **decisión** | Discretizar → **Clasificación** |
| Quiero **explorar** datos sin etiquetas | **Clustering** (No supervisado) |

4. **El catálogo de modelos** proporciona opciones para cada escenario:
   - Pocos datos → Ridge/SVR
   - Muchos features → Random Forest
   - Máxima precisión → Gradient Boosting
   - Interpretabilidad → Árboles de decisión

## 5.2 El Trade-off Bias-Varianza

Un concepto fundamental que conecta todos los modelos:

$$\text{Error total} = \underbrace{\text{Bias}^2}_{\text{error sistemático}} + \underbrace{\text{Varianza}}_{\text{sensibilidad al ruido}} + \underbrace{\sigma^2_{\text{ruido}}}_{\text{irreducible}}$$

- **Alto Bias (underfitting):** modelo demasiado simple → no captura la física
- **Alta Varianza (overfitting):** modelo demasiado complejo → memoriza el ruido
- **Objetivo:** encontrar el balance óptimo mediante validación cruzada e hiperparámetros

## 5.3 Impacto en el Futuro de la Nanotecnología

El Machine Learning está transformando la ciencia de materiales desde un paradigma de *prueba y error* a uno de *diseño dirigido por datos*. La combinación de:

$$\text{Simulación (DFT/MD)} + \text{ML} + \text{Experimentación} = \text{Descubrimiento Acelerado}$$

promete reducir el tiempo de desarrollo de nuevos nanomateriales de **décadas a años**, habilitando soluciones para energía limpia, medicina personalizada y electrónica de próxima generación.

---

## 📚 Referencias

1. **Goodfellow, I., Bengio, Y., & Courville, A.** (2016). *Deep Learning*. MIT Press.
2. **Géron, A.** (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*. O'Reilly.
3. **Butler, K. T., et al.** (2018). "Machine learning for molecular and materials science." *Nature*, 559, 547–555.
4. **Schleder, G. R., et al.** (2019). "From DFT to machine learning: recent approaches to materials science – a review." *Journal of Physics: Materials*, 2(3), 032001.
5. **Behler, J. & Parrinello, M.** (2007). "Generalized Neural-Network Representation of High-Dimensional Potential-Energy Surfaces." *Physical Review Letters*, 98, 146401.
6. **Merchant, A., et al.** (2023). "Scaling deep learning for materials discovery." *Nature*, 624, 80–85. (GNoME)"""
))

# ============ BUILD NOTEBOOK ============
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "cells": cells
}

output_path = r"c:\IA Nanotecnología\Antigravity-Nano-Research-Multiagentic-Core-main\educational_content\unit_03_ml_nanomaterials\Investigacion_Unidad3_Secciones_0_a_03.ipynb"

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"OK - Notebook creado exitosamente en:\n{output_path}")
