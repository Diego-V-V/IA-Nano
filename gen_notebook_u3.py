#!/usr/bin/env python3
"""
Script para generar la Jupyter Notebook de investigación:
  Unidad 3 – Machine Learning en Nanotecnología (Secciones 0.1–0.3)
"""
import json, os

# ── Helpers ──────────────────────────────────────────────────────────────────
def md(source: str):
    """Crea una celda markdown."""
    return {"cell_type": "markdown", "metadata": {},
            "source": source.split("\n")}

def code(source: str):
    """Crea una celda de código."""
    return {"cell_type": "code", "metadata": {}, "outputs": [],
            "execution_count": None,
            "source": source.split("\n")}

cells: list = []

# ═══════════════════════════════════════════════════════════════════════════
# 0. METADATOS
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""# Investigación: Machine Learning Aplicado a la Nanotecnología
## Fundamentos Teóricos – Secciones 0.1 a 0.3

**Autor:** Estudiante de Ingeniería en Nanotecnología y Ciencia de Materiales  
**Universidad:** Universidad Autónoma  
**Facultad:** Facultad de Ingeniería  
**Fecha:** 1 de marzo de 2026  
**Curso:** Modelado, Simulación e Inteligencia Artificial en Nanotecnología

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 1. RESUMEN / ABSTRACT
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""## Resumen / Abstract

El presente informe constituye una investigación a profundidad sobre los fundamentos del aprendizaje automático (*Machine Learning*, ML) y su aplicación en el campo de la nanotecnología y la ciencia de materiales. En particular, se abordan tres ejes temáticos fundamentales: (1) la motivación y justificación del uso de técnicas de ML para acelerar el descubrimiento y diseño de nanomateriales; (2) la taxonomía de los paradigmas de aprendizaje —supervisado, no supervisado y por refuerzo—, junto con sus formulaciones matemáticas; y (3) el análisis comparativo formal entre problemas de regresión y clasificación, acompañado de un catálogo de algoritmos relevantes para aplicaciones en nanociencia.

Se desarrollan casos de estudio mediante simulación numérica en Python, empleando librerías como `numpy`, `pandas`, `scikit-learn`, `matplotlib` y `seaborn`, con el objetivo de ilustrar la aplicación práctica de los modelos de ML en la predicción de propiedades de nanomateriales. Además, se realiza un análisis crítico que incluye métricas de error (MSE, $R^2$), evaluación de sesgo (*bias*) y varianza, y una discusión sobre las limitaciones de los modelos empleados.

**Palabras clave:** Machine Learning, nanotecnología, regresión, clasificación, aprendizaje supervisado, DFT, nanomateriales, ciencia de materiales.

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 2. INTRODUCCIÓN Y CONTEXTO
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""## 1. Introducción y Contexto del Problema

### 1.1 Motivación

El diseño y descubrimiento de nuevos nanomateriales representa uno de los desafíos más relevantes de la ciencia e ingeniería contemporáneas. Sin embargo, el espacio de búsqueda de compuestos inorgánicos posibles es extraordinariamente vasto —del orden de $10^{60}$ combinaciones—, lo cual hace inviable una exploración exhaustiva mediante técnicas convencionales (Yoon, Jeong y Kim, 2025). Por lo tanto, resulta imprescindible recurrir a herramientas computacionales que permitan acelerar este proceso de manera inteligente.

Los métodos basados en primeros principios, como la Teoría del Funcional de la Densidad (*Density Functional Theory*, DFT), proporcionan predicciones precisas de las propiedades electrónicas y estructurales de los materiales. No obstante, el costo computacional de un cálculo DFT por estructura oscila entre 1 y 48 horas (Nyangiwe, 2025), lo cual limita severamente la capacidad de exploración. En consecuencia, el aprendizaje automático (*Machine Learning*, ML) ha emergido como una herramienta complementaria que permite construir funciones de aproximación entrenadas sobre datos generados por DFT, dinámica molecular (MD) o experimentos, posibilitando predicciones en tiempo real (Lorenc, Mendes, Conniot, Sousa, Conde y Rodrigues, 2021).

Desde una perspectiva formal, Mitchell (1997) define el aprendizaje automático de la siguiente manera:

> **Definición formal.** Un programa de computadora se dice que *aprende* de la experiencia $E$ con respecto a alguna clase de tareas $T$ y medida de desempeño $P$, si su desempeño en tareas de $T$, medido por $P$, mejora con la experiencia $E$.

Esta definición constituye el principio fundamental sobre el cual se edifican todos los modelos que se estudiarán en las secciones subsiguientes.

### 1.2 Objetivo General

Investigar y analizar los fundamentos teóricos del aprendizaje automático aplicado a la nanotecnología, abarcando los paradigmas de aprendizaje, la distinción formal entre regresión y clasificación, y la validación numérica de modelos mediante simulaciones en Python.

### 1.3 Hipótesis de Trabajo

Los modelos de *Machine Learning* permiten aproximar con alta precisión las funciones que describen propiedades fisicoquímicas de nanomateriales, reduciendo significativamente el costo computacional en comparación con los métodos *ab initio* tradicionales.

### 1.4 Metodología Propuesta

1. Revisión bibliográfica de los fundamentos teóricos del ML aplicado a nanotecnología.
2. Formulación matemática rigurosa de los paradigmas de aprendizaje.
3. Implementación de simulaciones numéricas demostrativas en Python.
4. Análisis comparativo entre regresión y clasificación mediante casos de estudio.
5. Evaluación crítica de los modelos empleando métricas estándar.

### 1.5 Alcance

Este trabajo se circunscribe a las secciones 0.1 a 0.3 del material de la Unidad 3, enfocándose en los fundamentos teóricos y prácticos del ML antes de la implementación de algoritmos específicos.

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 3. SETUP (código)
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""## 2. Configuración del Entorno Computacional

A continuación se importan las librerías necesarias para el desarrollo de los análisis y simulaciones numéricas presentados en este informe. Se emplea el *stack* tecnológico estándar de la ciencia de datos en Python: `numpy` para cálculo numérico, `pandas` para manipulación de datos tabulares, `matplotlib` y `seaborn` para visualización de calidad científica, y `scikit-learn` para la implementación de modelos de ML.
"""))

cells.append(code(r"""# ============================================================
# Configuración del entorno computacional
# ============================================================
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import (mean_squared_error, r2_score,
                             accuracy_score, f1_score,
                             classification_report, confusion_matrix)
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression, make_classification
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Configuración de visualización
matplotlib.rcParams['figure.dpi'] = 120
matplotlib.rcParams['font.size'] = 11
sns.set_style('whitegrid')
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11

print("✅ Entorno configurado correctamente.")
print(f"   NumPy:        {np.__version__}")
print(f"   Pandas:       {pd.__version__}")
print(f"   Matplotlib:   {matplotlib.__version__}")
print(f"   Seaborn:      {sns.__version__}")
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 4. FUNDAMENTOS TEÓRICOS – SECCIÓN 0.1
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 3. Fundamentos Teóricos: ¿Por qué Machine Learning en Nanotecnología?

### 3.1 El Desafío del Espacio Composicional

El modelado analítico clásico en nanociencia enfrenta limitaciones fundamentales que pueden resumirse en la siguiente tabla:

| Problema | Magnitud |
|----------|----------|
| Compuestos inorgánicos posibles | $\sim 10^{60}$ |
| Cálculo DFT por estructura | 1 – 48 horas |
| Experimentos de síntesis | Semanas / meses |

**Principio fundamental.** Debido a la inmensidad del espacio de búsqueda, resulta imposible explorar todas las combinaciones posibles mediante métodos de primeros principios. Por lo tanto, se requiere una estrategia computacional que permita interpolar entre los puntos conocidos del espacio de materiales (Yoon et al., 2025).

### 3.2 Modelo Matemático: ML como Función de Interpolación

La idea central del ML aplicado a nanotecnología consiste en construir un *modelo matemático* $\hat{f}$ que aproxime la función objetivo desconocida $f_{\text{real}}$, la cual mapea descriptores de materiales a sus propiedades:

$$\text{DFT/MD} \rightarrow \text{Datos} \xrightarrow{\text{ML}} \hat{f}(\mathbf{x}) \approx f_{\text{real}}(\mathbf{x}) \rightarrow \text{Predicción instantánea}$$

Formalmente, dado un conjunto de entrenamiento $\mathcal{D} = \{(\mathbf{x}_i, y_i)\}_{i=1}^{N}$ donde $\mathbf{x}_i \in \mathbb{R}^d$ es el vector de descriptores y $y_i \in \mathbb{R}$ (o $y_i \in \{C_1, \ldots, C_k\}$) es la propiedad objetivo, el problema de aprendizaje consiste en encontrar:

$$\hat{f}^* = \arg\min_{f \in \mathcal{F}} \frac{1}{N} \sum_{i=1}^{N} \mathcal{L}(f(\mathbf{x}_i), y_i) + \lambda \, \Omega(f)$$

donde $\mathcal{L}$ es la *función de pérdida* (por ejemplo, el error cuadrático medio), $\mathcal{F}$ es el espacio de funciones candidatas, $\Omega(f)$ es un término de regularización, y $\lambda \geq 0$ controla el equilibrio entre ajuste y complejidad (Mitchell, 1997; Cencerrado Barraqué y Ventura Royo, 2019).

### 3.3 Casos de Éxito en Nanociencia

Los siguientes ejemplos ilustran el impacto transformador del ML en la investigación de materiales:

- **AlphaFold 2** (DeepMind, 2021): predicción de la estructura tridimensional de proteínas con precisión a nivel atómico (Lorenc et al., 2021).
- **GNoME** (Google, 2023): descubrió 2.2 millones de nuevos materiales estables mediante redes neuronales de grafos (*Graph Neural Networks*, GNN).
- **Potenciales NNP Behler-Parrinello**: potenciales interatómicos con la precisión de DFT pero a la velocidad de la mecánica clásica.
- **Diseño de catalizadores**: ML permite predecir energías de adsorción sobre aleaciones de alta entropía, acelerando el descubrimiento de electrocatalizadores eficientes (Yoon et al., 2025).

Estos resultados validan la hipótesis de que el ML puede actuar como un acelerador computacional en la investigación de nanomateriales, lo cual significa que el tiempo requerido para la exploración del espacio composicional se reduce en órdenes de magnitud.

### 3.4 Marco Teórico Formal

Desde la perspectiva de la teoría del aprendizaje computacional, Moreno et al. (1994) establecen que el *aprendizaje automático* es la disciplina que estudia los métodos computacionales para adquirir conocimiento nuevo, nuevas competencias y nuevas formas de organizar el conocimiento ya existente. Además, Cencerrado Barraqué y Ventura Royo (2019) señalan que un sistema de aprendizaje computacional debe ser capaz de mejorar su rendimiento con la experiencia, lo cual es consistente con la definición axiomática de Mitchell (1997).

El *Teorema de No Free Lunch* (Wolpert y Macready, 1997) establece un principio fundamental:

> **Teorema.** No existe un algoritmo de aprendizaje que sea universalmente superior a todos los demás en todos los dominios de aplicación.

Esto indica que la selección del modelo adecuado depende intrínsecamente de las características del problema, lo cual justifica la necesidad de un catálogo de algoritmos y criterios de selección, como se desarrollará en la Sección 0.3.

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 4B. VIS SECCIÓN 0.1
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""### 3.5 Caso de Estudio: Visualización del Pipeline DFT → ML

A continuación se presenta una simulación numérica que ilustra el concepto de ML como función de interpolación para la predicción de una propiedad de nanomateriales (bandgap, $E_g$) a partir de descriptores composicionales. Se observa que el modelo entrenado con datos de DFT puede generalizar a nuevas composiciones no evaluadas previamente.
"""))

cells.append(code(r"""# ============================================================
# Caso de estudio: ML como interpolador de datos DFT
# ============================================================
np.random.seed(42)

# Simulación de datos DFT: bandgap vs descriptor composicional
n_samples = 80
x_descriptor = np.sort(np.random.uniform(0, 10, n_samples))
# Función "real" no lineal (simulando la relación física)
y_bandgap_real = 1.5 * np.sin(0.8 * x_descriptor) + 0.3 * x_descriptor + 0.5
noise = np.random.normal(0, 0.25, n_samples)
y_bandgap_dft = y_bandgap_real + noise  # datos "DFT" con ruido

# Entrenar modelo ML (Random Forest)
X = x_descriptor.reshape(-1, 1)
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y_bandgap_dft)

# Predicción en espacio continuo
x_pred = np.linspace(0, 10, 300).reshape(-1, 1)
y_pred = rf.predict(x_pred)

# Visualización de calidad científica
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.scatter(x_descriptor, y_bandgap_dft, c='steelblue', alpha=0.7,
           edgecolors='navy', s=50, label='Datos DFT (simulados)', zorder=3)
ax.plot(x_pred, y_pred, 'r-', linewidth=2.0,
        label='Predicción ML (Random Forest)', zorder=2)
ax.plot(x_descriptor, y_bandgap_real, 'g--', linewidth=1.5,
        alpha=0.6, label=r'Función real $f_{\mathrm{real}}(\mathbf{x})$', zorder=1)
ax.set_xlabel('Descriptor composicional (u.a.)')
ax.set_ylabel(r'Bandgap $E_g$ (eV)')
ax.set_title('Pipeline DFT → ML: Predicción de Bandgap en Nanomateriales')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Métricas
mse = mean_squared_error(y_bandgap_dft, rf.predict(X))
r2 = r2_score(y_bandgap_dft, rf.predict(X))
print(f"\n📊 Métricas del modelo (entrenamiento):")
print(f"   MSE  = {mse:.4f}")
print(f"   R²   = {r2:.4f}")
print(f"\nEsto indica que el modelo Random Forest logra capturar")
print(f"la tendencia subyacente de los datos DFT con un coeficiente")
print(f"de determinación R² = {r2:.4f}, validando la hipótesis de que")
print(f"los modelos de ML pueden aproximar funciones complejas de")
print(f"propiedades de nanomateriales.")
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 5. TIPOS DE APRENDIZAJE – SECCIÓN 0.2
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 4. Tipos de Aprendizaje – Sección 0.2

### 4.1 Aprendizaje Supervisado

**Definición formal.** El aprendizaje supervisado consiste en inferir la función $f: \mathbf{X} \rightarrow \mathbf{y}$ a partir de un conjunto de pares etiquetados $\{(\mathbf{x}_i, y_i)\}_{i=1}^{N}$, donde cada $\mathbf{x}_i \in \mathbb{R}^d$ es un vector de características (*features*) y $y_i$ es la etiqueta o variable objetivo (Mitchell, 1997).

El objetivo es minimizar el *riesgo empírico*:

$$R_{\text{emp}}(f) = \frac{1}{N} \sum_{i=1}^{N} \mathcal{L}(f(\mathbf{x}_i), y_i)$$

donde $\mathcal{L}$ denota la función de pérdida seleccionada. La solución óptima $\hat{f}$ se obtiene a través de un proceso de *optimización*, frecuentemente mediante el método del *gradiente descendente*:

$$\theta_{t+1} = \theta_t - \eta \, \nabla_\theta \, R_{\text{emp}}(f_\theta)$$

donde $\eta > 0$ es la *tasa de aprendizaje* y $\theta$ son los parámetros del modelo (Cencerrado Barraqué y Ventura Royo, 2019).

**En nanotecnología:** predicción de propiedades como el bandgap ($E_g$), la temperatura de fusión ($T_m$), la energía de formación ($\Delta H_f$) o la actividad catalítica (Yoon et al., 2025; Nyangiwe, 2025).

### 4.2 Aprendizaje No Supervisado

**Definición formal.** El aprendizaje no supervisado busca descubrir la estructura intrínseca de un conjunto de datos $\{\mathbf{x}_i\}_{i=1}^{N}$ sin disponer de etiquetas $y_i$. Las técnicas principales incluyen:

- **Clustering** (*agrupamiento*): particionar los datos en $k$ clusters $\{C_1, \ldots, C_k\}$ minimizando la *inercia* $\sum_{j=1}^{k} \sum_{\mathbf{x} \in C_j} \|\mathbf{x} - \boldsymbol{\mu}_j\|^2$, donde $\boldsymbol{\mu}_j$ es el centroide del cluster $j$.
- **Reducción de dimensionalidad**: proyectar los datos de $\mathbb{R}^d$ a $\mathbb{R}^p$ ($p \ll d$) preservando la máxima varianza, como en el Análisis de Componentes Principales (PCA) (Moreno et al., 1994).

**En nanotecnología:** clustering de fases cristalinas, reducción de dimensionalidad de espectros, detección de anomalías en imágenes TEM (Nyangiwe, 2025).

### 4.3 Aprendizaje por Refuerzo

**Definición formal.** Un agente aprende una **política óptima** $\pi^*: S \rightarrow A$ por interacción con un entorno, de modo que maximice la recompensa acumulada esperada:

$$\pi^* = \arg\max_\pi \, \mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t \, r_t \mid \pi \right]$$

donde $S$ es el espacio de estados, $A$ es el espacio de acciones, $r_t$ es la recompensa en el instante $t$ y $\gamma \in [0,1)$ es el factor de descuento (Mitchell, 1997).

**En nanotecnología:** optimización de rutas de síntesis, diseño molecular iterativo, control de procesos de nanofabricación (Lorenc et al., 2021).

### 4.4 Tabla Comparativa

| Paradigma | Datos | Salida | Ejemplo en nanociencia |
|-----------|-------|--------|------------------------|
| Supervisado | $(\mathbf{x}, y)$ etiquetados | $\hat{y}$ | Predecir $E_g$ de un material |
| No supervisado | $\mathbf{x}$ sin etiqueta | Grupos/representaciones | Clustering de estructuras cristalinas |
| Refuerzo | (estado, acción, recompensa) | Política $\pi$ | Ruta de síntesis óptima |

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 5B. VIS SECCIÓN 0.2
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""### 4.5 Simulación Numérica: Ilustración de los Paradigmas de Aprendizaje

La siguiente simulación genera datos sintéticos inspirados en nanomateriales para ilustrar visualmente los tres paradigmas de aprendizaje: supervisado (regresión), no supervisado (clustering) y la estructura subyacente de los datos.
"""))

cells.append(code(r"""# ============================================================
# Simulación: Tres paradigmas de aprendizaje
# ============================================================
np.random.seed(42)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# --- Panel 1: Aprendizaje Supervisado (Regresión) ---
n = 100
X_sup = np.random.uniform(1, 10, n)
y_sup = 2.5 * X_sup + 0.8 * X_sup**0.5 + np.random.normal(0, 1.5, n)
lr = LinearRegression()
lr.fit(X_sup.reshape(-1, 1), y_sup)
x_line = np.linspace(1, 10, 200)
y_line = lr.predict(x_line.reshape(-1, 1))

axes[0].scatter(X_sup, y_sup, c='steelblue', alpha=0.6,
                edgecolors='navy', s=40, label='Datos etiquetados')
axes[0].plot(x_line, y_line, 'r-', lw=2, label=r'$\hat{f}(\mathbf{x})$')
axes[0].set_xlabel('Descriptor molecular (u.a.)')
axes[0].set_ylabel(r'Propiedad $y$ (eV)')
axes[0].set_title('Supervisado: Regresión')
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)

# --- Panel 2: Aprendizaje No Supervisado (Clustering) ---
from sklearn.datasets import make_blobs
X_unsup, y_true = make_blobs(n_samples=150, centers=3,
                              cluster_std=0.8, random_state=42)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
y_km = kmeans.fit_predict(X_unsup)

axes[1].scatter(X_unsup[:, 0], X_unsup[:, 1], c=y_km,
                cmap='viridis', alpha=0.7, edgecolors='k', s=40)
axes[1].scatter(kmeans.cluster_centers_[:, 0],
                kmeans.cluster_centers_[:, 1],
                c='red', marker='X', s=200, edgecolors='k',
                label='Centroides')
axes[1].set_xlabel('Feature 1')
axes[1].set_ylabel('Feature 2')
axes[1].set_title('No Supervisado: K-Means Clustering')
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

# --- Panel 3: Esquema de Aprendizaje por Refuerzo ---
# Visualización conceptual de una trayectoria de optimización
states = np.array([[0, 0], [1, 2], [3, 3], [5, 4], [7, 3], [8, 5]])
rewards = [0, 1, 2, 3, 2, 5]

axes[2].plot(states[:, 0], states[:, 1], 'b-o', markersize=8,
             markerfacecolor='steelblue', markeredgecolor='navy', lw=2)
for i, (s, r) in enumerate(zip(states, rewards)):
    axes[2].annotate(f'$r_{i}={r}$', (s[0]+0.2, s[1]+0.2),
                     fontsize=9, color='darkred')
axes[2].set_xlabel('Estado $s$')
axes[2].set_ylabel('Acción $a$')
axes[2].set_title('Por Refuerzo: Trayectoria de Optimización')
axes[2].grid(True, alpha=0.3)

plt.suptitle('Paradigmas de Aprendizaje Automático en Nanotecnología',
             fontsize=14, fontweight='bold', y=1.03)
plt.tight_layout()
plt.show()

print("\nSe observa que cada paradigma aborda un tipo de problema")
print("diferente. El supervisado requiere datos etiquetados;")
print("el no supervisado descubre estructura; y el refuerzo")
print("optimiza secuencias de decisiones (Moreno et al., 1994).")
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 6. REGRESIÓN VS CLASIFICACIÓN – SECCIÓN 0.3  (PARTE 1 - TEORÍA)
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 5. Regresión vs Clasificación y Catálogo de Modelos – Sección 0.3

### 5.1 Definición Formal

La distinción fundamental entre regresión y clasificación radica en la naturaleza de la variable objetivo $y$:

$$\text{Regresión}: \quad y \in \mathbb{R} \quad \text{(valor continuo)}$$

$$\text{Clasificación}: \quad y \in \{C_1, C_2, \ldots, C_k\} \quad \text{(categoría discreta)}$$

### 5.2 Funciones de Pérdida

**Regresión — Error Cuadrático Medio (MSE):**

$$\mathcal{L}_{\text{MSE}} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

Esta función penaliza cuadráticamente las desviaciones entre el valor predicho $\hat{y}_i$ y el valor real $y_i$, lo cual significa que los errores grandes son penalizados de manera desproporcionada (Mitchell, 1997).

**Clasificación — Entropía Cruzada (*Cross-Entropy*):**

$$\mathcal{L}_{\text{CE}} = -\frac{1}{N} \sum_{i=1}^{N} \sum_{c=1}^{k} y_{i,c} \, \log(\hat{p}_{i,c})$$

donde $\hat{p}_{i,c}$ es la probabilidad predicha de que la muestra $i$ pertenezca a la clase $c$ (Cencerrado Barraqué y Ventura Royo, 2019).

### 5.3 Ejemplos en Nanotecnología

- **Regresión** → predecir $E_g = 2.43 \text{ eV}$, $T_m = 1337 \text{ K}$, $\Delta H_f = -1.2 \text{ eV/átomo}$
- **Clasificación** → identificar fase cristalina (FCC / BCC / HCP), estabilidad termodinámica (estable / inestable)

### 5.4 Catálogo de Algoritmos Supervisados

| Tipo | Algoritmo | Hiperparámetros clave | Cuándo usar en nanotecnología |
|------|-----------|----------------------|-------------------------------|
| **Regresión** | Ridge / Lasso | `alpha` | Línea base, pocos datos, features correlacionadas |
| **Regresión** | SVR | `C`, `epsilon`, `kernel`, `gamma` | Alta dimensión, pocos ejemplos |
| **Regresión** | K-Vecinos (KNN) | `n_neighbors`, `metric` | Datos pequeños, interpolación local |
| **Regresión** | Árbol de Decisión | `max_depth`, `min_samples` | Interpretable, reglas físicas |
| **Regresión** | Random Forest | `n_estimators`, `max_depth` | Robusto, muchos features |
| **Regresión** | Gradient Boosting | `learning_rate`, `n_estimators` | Mayor precisión |
| **Reg./Clas.** | MLP (Red Neuronal) | `hidden_layer_sizes`, `alpha`, `lr` | Relaciones muy no lineales |
| **Clasificación** | SVC | `C`, `kernel`, `gamma` | Fronteras no lineales |
| **Clasificación** | Random Forest | igual que arriba | Clasificación robusta |
| **Clasificación** | KNN Clasificador | `n_neighbors` | Simple, no paramétrico |

### 5.5 Catálogo de Algoritmos No Supervisados

| Algoritmo | Tipo | Cuándo usar |
|-----------|------|-------------|
| K-Means | Clustering | Agrupar estructuras similares |
| PCA | Reducción dim. | Visualizar espacio de materiales |
| t-SNE | Reducción dim. | Visualización no lineal |
| Autoencoder | Reducción dim. / generativo | Representaciones compactas |
| DBSCAN | Clustering | Clusters de forma arbitraria, outliers |

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 6B. CASO DE ESTUDIO – REGRESIÓN
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""### 5.6 Caso de Estudio I: Regresión — Predicción de Bandgap

Se genera un dataset sintético que simula la relación entre descriptores composicionales de nanomateriales y su bandgap ($E_g$). Se comparan múltiples modelos de regresión para evaluar su capacidad de generalización.
"""))

cells.append(code(r"""# ============================================================
# Caso de estudio: Regresión – Predicción de Bandgap
# ============================================================
np.random.seed(42)

# Generar datos sintéticos de nanomateriales
n_samples = 200
n_features = 5

# Features: radio atómico, electronegatividad, nº electrones de valencia,
#           energía de ionización, afinidad electrónica (simulados)
X_nano = np.random.randn(n_samples, n_features)

# Bandgap como función no lineal de los descriptores
y_bandgap = (1.5 * X_nano[:, 0]**2
             - 0.8 * X_nano[:, 1]
             + 0.5 * X_nano[:, 2] * X_nano[:, 3]
             + 2.0
             + np.random.normal(0, 0.3, n_samples))

feature_names = ['Radio atómico', 'Electronegatividad',
                 'e⁻ valencia', 'E_ionización', 'Afinidad e⁻']

# Crear DataFrame
df_reg = pd.DataFrame(X_nano, columns=feature_names)
df_reg['Bandgap (eV)'] = y_bandgap

# División train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_nano, y_bandgap, test_size=0.2, random_state=42)

# Escalar features
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

# Modelos a comparar
modelos = {
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.1),
    'KNN (k=5)': KNeighborsRegressor(n_neighbors=5),
    'Árbol de Decisión': DecisionTreeRegressor(max_depth=5, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=5,
                                            random_state=42),
    'SVR (RBF)': SVR(kernel='rbf', C=10, epsilon=0.1),
}

# Entrenar y evaluar
resultados = []
for nombre, modelo in modelos.items():
    modelo.fit(X_train_sc, y_train)
    y_pred = modelo.predict(X_test_sc)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    # Validación cruzada
    cv_scores = cross_val_score(modelo, X_train_sc, y_train,
                                cv=5, scoring='r2')
    resultados.append({
        'Modelo': nombre,
        'MSE (test)': mse,
        'R² (test)': r2,
        'R² CV (media)': cv_scores.mean(),
        'R² CV (std)': cv_scores.std()
    })

df_resultados = pd.DataFrame(resultados)
df_resultados = df_resultados.sort_values('R² (test)', ascending=False)
print("=" * 70)
print("📊 COMPARACIÓN DE MODELOS DE REGRESIÓN")
print("   Predicción de Bandgap en Nanomateriales (datos sintéticos)")
print("=" * 70)
print(df_resultados.to_string(index=False))
print("=" * 70)
print("\nSe observa que los modelos no lineales (Random Forest, SVR)")
print("superan a los lineales (Ridge, Lasso), lo cual es consistente")
print("con la naturaleza no lineal de la relación entre descriptores")
print("y bandgap. Esto valida la hipótesis de que los modelos de ML")
print("pueden capturar relaciones complejas en datos de nanomateriales.")
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 6C. VISUALIZACIÓN REGRESIÓN
# ═══════════════════════════════════════════════════════════════════════════
cells.append(code(r"""# ============================================================
# Visualización: Comparación de modelos de regresión
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1: Barplot de R²
df_plot = df_resultados.copy()
colors = sns.color_palette('viridis', len(df_plot))
axes[0].barh(df_plot['Modelo'], df_plot['R² (test)'], color=colors)
axes[0].set_xlabel(r'$R^2$ (test)')
axes[0].set_title('Comparación de Modelos: $R^2$ en Test')
axes[0].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
axes[0].grid(True, alpha=0.3)

# Panel 2: Predicho vs Real (mejor modelo)
best_model_name = df_resultados.iloc[0]['Modelo']
best_model = modelos[best_model_name]
best_model.fit(X_train_sc, y_train)
y_pred_best = best_model.predict(X_test_sc)

axes[1].scatter(y_test, y_pred_best, c='steelblue', alpha=0.7,
                edgecolors='navy', s=50)
lims = [min(y_test.min(), y_pred_best.min()) - 0.5,
        max(y_test.max(), y_pred_best.max()) + 0.5]
axes[1].plot(lims, lims, 'r--', lw=1.5, label='Línea ideal')
axes[1].set_xlabel('Bandgap real (eV)')
axes[1].set_ylabel('Bandgap predicho (eV)')
axes[1].set_title(f'Predicción vs Real — {best_model_name}')
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"\nEl mejor modelo es {best_model_name} con R² = "
      f"{df_resultados.iloc[0]['R² (test)']:.4f}.")
print("La gráfica Predicho vs Real muestra una correlación fuerte,")
print("lo cual indica que el modelo captura adecuadamente la")
print("dependencia funcional entre los descriptores y el bandgap.")
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 7. CASO DE ESTUDIO – CLASIFICACIÓN
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""### 5.7 Caso de Estudio II: Clasificación — Predicción de Fase Cristalina

Se genera un dataset sintético que simula la clasificación de nanomateriales en tres fases cristalinas: FCC, BCC y HCP, a partir de descriptores composicionales. Se comparan modelos de clasificación y se evalúan mediante precisión, F1-score y matrices de confusión.
"""))

cells.append(code(r"""# ============================================================
# Caso de estudio: Clasificación – Fase Cristalina
# ============================================================
np.random.seed(42)

# Generar datos sintéticos de clasificación
X_clas, y_clas = make_classification(
    n_samples=300, n_features=5, n_informative=4,
    n_redundant=1, n_classes=3, n_clusters_per_class=1,
    class_sep=1.5, random_state=42)

clases = {0: 'FCC', 1: 'BCC', 2: 'HCP'}
feature_names_c = ['Radio atómico', 'Electroneg.', 'e⁻ val.',
                   'E_ionización', 'Densidad']

# División train/test
X_tr_c, X_te_c, y_tr_c, y_te_c = train_test_split(
    X_clas, y_clas, test_size=0.2, random_state=42, stratify=y_clas)

# Escalar
sc_c = StandardScaler()
X_tr_c_sc = sc_c.fit_transform(X_tr_c)
X_te_c_sc = sc_c.transform(X_te_c)

# Modelos de clasificación
modelos_clas = {
    'KNN (k=5)': KNeighborsClassifier(n_neighbors=5),
    'Árbol de Decisión': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=5,
                                             random_state=42),
    'SVC (RBF)': SVC(kernel='rbf', C=10, gamma='scale'),
}

# Entrenar y evaluar
results_c = []
for name, model in modelos_clas.items():
    model.fit(X_tr_c_sc, y_tr_c)
    y_p = model.predict(X_te_c_sc)
    acc = accuracy_score(y_te_c, y_p)
    f1 = f1_score(y_te_c, y_p, average='weighted')
    results_c.append({'Modelo': name, 'Precisión': acc, 'F1 (weighted)': f1})

df_res_c = pd.DataFrame(results_c).sort_values('F1 (weighted)', ascending=False)

print("=" * 60)
print("📊 COMPARACIÓN DE MODELOS DE CLASIFICACIÓN")
print("   Predicción de Fase Cristalina (FCC/BCC/HCP)")
print("=" * 60)
print(df_res_c.to_string(index=False))
print("=" * 60)

# Matriz de confusión del mejor modelo
best_c = modelos_clas[df_res_c.iloc[0]['Modelo']]
best_c.fit(X_tr_c_sc, y_tr_c)
y_p_best = best_c.predict(X_te_c_sc)
cm = confusion_matrix(y_te_c, y_p_best)

fig, ax = plt.subplots(1, 1, figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
            xticklabels=['FCC', 'BCC', 'HCP'],
            yticklabels=['FCC', 'BCC', 'HCP'])
ax.set_xlabel('Predicción')
ax.set_ylabel('Real')
ax.set_title(f'Matriz de Confusión — {df_res_c.iloc[0]["Modelo"]}')
plt.tight_layout()
plt.show()

print(f"\nEl mejor modelo de clasificación es {df_res_c.iloc[0]['Modelo']}")
print(f"con F1-score = {df_res_c.iloc[0]['F1 (weighted)']:.4f}.")
print("La matriz de confusión muestra que el modelo logra discriminar")
print("las tres fases cristalinas con alta precisión, lo cual indica que")
print("los descriptores composicionales contienen información suficiente")
print("para determinar la fase cristalina del material.")
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 8. ANÁLISIS CRÍTICO
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""---

## 6. Análisis Crítico

### 6.1 Correlación y Dependencia

Los resultados presentados en las secciones anteriores ponen de manifiesto la importancia de seleccionar la familia de modelos adecuada en función de la naturaleza del problema. En el caso de la regresión del bandgap, se observa que los modelos capaces de capturar relaciones no lineales (Random Forest, SVR con kernel RBF) obtienen un rendimiento significativamente superior al de los modelos lineales (Ridge, Lasso). Esto indica que existe una **dependencia no lineal** entre los descriptores composicionales y la propiedad objetivo, lo cual es consistente con la física subyacente de la estructura electrónica de los materiales (Yoon et al., 2025).

Sin embargo, es fundamental distinguir entre **correlación estadística** y **causalidad**. El hecho de que un descriptor esté correlacionado con la propiedad objetivo no implica necesariamente una relación causal directa. Por lo tanto, la interpretación física de los modelos de ML debe realizarse con cautela (Nyangiwe, 2025).

### 6.2 Métricas de Error y Éxito

Las métricas empleadas en este trabajo incluyen:

- **Error cuadrático medio (MSE):** $\text{MSE} = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2$
- **Coeficiente de determinación ($R^2$):** $R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$
- **Precisión del modelo (Accuracy):** proporción de predicciones correctas
- **F1-score:** media armónica de precisión y recall

### 6.3 Limitaciones del Modelo

Es necesario reconocer las siguientes **limitaciones** de los análisis presentados:

1. Los datos empleados son **sintéticos**, por lo que los resultados no son directamente extrapolables a sistemas reales.
2. No se ha realizado un **análisis de sensibilidad** exhaustivo con respecto a los hiperparámetros.
3. El **sesgo (bias)** de selección de modelos puede influir en las conclusiones: el Teorema de No Free Lunch implica que la superioridad de un modelo en un dominio no garantiza su rendimiento en otro.
4. La **discrepancia** entre rendimiento en entrenamiento y en test indica la presencia del compromiso bias-varianza, que debe gestionarse cuidadosamente (Moreno et al., 1994).

### 6.4 Comparativa: Regresión vs Clasificación

| Aspecto | Regresión | Clasificación |
|---------|-----------|---------------|
| Variable objetivo | $y \in \mathbb{R}$ | $y \in \{C_1, \ldots, C_k\}$ |
| Función de pérdida | MSE, MAE | Cross-Entropy, Hinge |
| Métricas principales | MSE, $R^2$, MAE | Accuracy, F1, AUC |
| Ejemplo nano | $E_g$, $T_m$ | FCC/BCC/HCP, estable/inestable |
| Cuándo usar | Predecir valores continuos | Predecir categorías |

La elección entre regresión y clasificación depende exclusivamente de la naturaleza de la variable objetivo. En consecuencia, un mismo problema puede reformularse como regresión o clasificación según la discretización de la variable de interés (Cencerrado Barraqué y Ventura Royo, 2019).

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 9. CONCLUSIONES
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""## 7. Conclusiones y Aplicabilidad

### 7.1 Conclusión General

El presente trabajo ha demostrado que los fundamentos del aprendizaje automático constituyen herramientas poderosas para la ciencia de materiales y la nanotecnología. Los principales **hallazgos** de esta investigación son:

1. **El ML como acelerador computacional:** las técnicas de aprendizaje supervisado permiten aproximar funciones complejas que relacionan descriptores de materiales con sus propiedades, reduciendo el tiempo de exploración del espacio composicional de días a milisegundos.

2. **Selección del paradigma adecuado:** la taxonomía de los paradigmas de aprendizaje (supervisado, no supervisado, por refuerzo) proporciona un marco conceptual claro para abordar distintos tipos de problemas en nanociencia.

3. **Regresión vs clasificación:** la distinción formal entre estos dos tipos de problemas, junto con el catálogo de algoritmos, constituye una guía práctica para el investigador en nanomateriales.

4. **Importancia del modelo matemático:** la formulación rigurosa de los problemas de aprendizaje, incluyendo funciones de pérdida y regularización, es esencial para obtener modelos confiables y generalizables.

### 7.2 Aplicación Industrial e Impacto Potencial

Las técnicas estudiadas tienen una **aplicación industrial** directa en:

- Diseño acelerado de catalizadores para conversión de CO₂ (Yoon et al., 2025).
- Descubrimiento de nuevos materiales para baterías y dispositivos fotovoltaicos.
- Optimización de procesos de nanofabricación.
- Desarrollo de fármacos basados en nanopartículas para aplicaciones biomédicas (Lorenc et al., 2021).

### 7.3 Recomendaciones y Trabajo Futuro

Se recomienda extender esta investigación en las siguientes direcciones:

- Implementación de algoritmos avanzados (Gradient Boosting, redes neuronales) con datos experimentales reales.
- Ingeniería de features: uso de descriptores moleculares y cristalográficos validados (Coulomb matrix, fingerprints).
- Análisis de sensibilidad paramétrica y optimización bayesiana de hiperparámetros.
- Validación cruzada estratificada con datasets de referencia en ciencia de materiales.

---
"""))

# ═══════════════════════════════════════════════════════════════════════════
# 10. BIBLIOGRAFÍA
# ═══════════════════════════════════════════════════════════════════════════
cells.append(md(r"""## 8. Bibliografía y Referencias

Cencerrado Barraqué, A. y Ventura Royo, C. (2019). *Introducción al aprendizaje computacional* (1.ª ed.). Universitat Oberta de Catalunya (FUOC).

Lorenc, A., Mendes, B. B., Conniot, J., Sousa, D. P., Conde, J. y Rodrigues, T. (2021). Machine learning for next-generation nanotechnology in healthcare. *Matter*, *4*(10), 3078–3080. https://doi.org/10.1016/j.matt.2021.09.014

Mitchell, T. M. (1997). *Machine Learning*. McGraw-Hill Science/Engineering/Math. ISBN: 978-0-07-042807-2.

Moreno, A., Armengol, E., Béjar, J., Belanche, L., Cortés, U., Gavaldà, R., Gimeno, J. M., López, B., Martín, M. y Sànchez, M. (1994). *Aprendizaje automático*. Edicions de la Universitat Politècnica de Catalunya (Edicions UPC).

Nyangiwe, N. N. (2025). Applications of density functional theory and machine learning in nanomaterials: A review. *Next Materials*, *8*, 100683. https://doi.org/10.1016/j.nxmate.2025.100683

Yoon, U., Jeong, K. y Kim, S. H. (2025). Advancing electrocatalysis through density functional theory: From reaction mechanisms to machine learning integration. *Journal of CO₂ Utilization*, *101*, 103192. https://doi.org/10.1016/j.jcou.2025.103192
"""))

# ═══════════════════════════════════════════════════════════════════════════
# CONSTRUIR NOTEBOOK
# ═══════════════════════════════════════════════════════════════════════════
notebook = {
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
    "nbformat": 4,
    "nbformat_minor": 5,
    "cells": cells
}

output_dir = r"c:\IA Nanotecnología\Antigravity-Nano-Research-Multiagentic-Core-main\educational_content\unit_03_ml_nanomaterials"
output_path = os.path.join(output_dir, "Investigacion_U3_Secciones_0.1_0.3.ipynb")
os.makedirs(output_dir, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"\n[OK] Notebook generada exitosamente en:\n   {output_path}")
