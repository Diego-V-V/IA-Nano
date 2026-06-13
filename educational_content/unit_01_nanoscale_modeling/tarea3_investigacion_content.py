# ============================================
# TAREA 3: INVESTIGACIÓN BIBLIOGRÁFICA
# Contenido para agregar al notebook TAREA_1.ipynb
# ============================================

# CELDA MARKDOWN 1: Título y referencia
"""
# 📚 TAREA 3: Investigación Bibliográfica

## Artículo de Referencia

**Baletto, F. & Ferrando, R.** (2005). *"Structural properties of nanoclusters: Energetic, thermodynamic, and kinetic effects."* **Reviews of Modern Physics**, 77, 371-423.

DOI: [10.1103/RevModPhys.77.371](https://doi.org/10.1103/RevModPhys.77.371)

---

Este artículo seminal es una revisión exhaustiva sobre las propiedades estructurales de nanoclusters metálicos, abordando aspectos energéticos, termodinámicos y cinéticos que determinan su morfología y estabilidad.

A continuación, respondemos las preguntas clave basándonos en los hallazgos del artículo:
"""

# CELDA MARKDOWN 2: Pregunta 1 - Estructuras estables
"""
## 🔷 Pregunta 1: ¿Qué estructuras son más estables para clusters metálicos de <100 átomos?

### Respuesta:

Para clusters metálicos pequeños (N < 100 átomos), las estructuras más estables **NO** son las estructuras cristalinas FCC (Face-Centered Cubic) o BCC que observamos en el material bulk. En su lugar, dominan **estructuras no cristalinas** debido a efectos de superficie.

### Estructuras Principales:

#### 1. **Icosaedros (Ih)**
- **Rango de estabilidad**: N = 13, 55, 147 átomos (magic numbers)
- **Características**:
  - Máxima coordinación superficial (cada átomo tiene más vecinos)
  - Simetría de 5 ejes → **NO compatible con periodicidad cristalina**
  - Energía superficial mínima para clusters muy pequeños
  - **Desventaja**: Contiene **strain elástico** interno (tensión) que aumenta con el tamaño

**Ejemplo**: Nuestros clusters de 55 átomos (noshells=2) son icosaedros perfectos.

#### 2. **Decaedros (Dh)**
- **Rango de estabilidad**: N ≈ 75-150 átomos (competitivo con Ih)
- **Características**:
  - Estructura de 5 planos gemelos (twin planes)
  - Menor strain que icosaedros para tamaños intermedios
  - Simetría pentagonal
  - Común en nanopartículas de Au y Ag

#### 3. **FCC truncado (TO - Truncated Octahedron)**
- **Rango de estabilidad**: N > 100-150 átomos
- **Características**:
  - Fragmento de la red cristalina bulk
  - Caras {111} y {100}
  - **Sin strain interno** → favorecido para clusters grandes
  - Transición gradual hacia estructura bulk

### Diagrama de Estabilidad (según Baletto & Ferrando):

```
N (átomos)     Estructura Dominante
─────────────────────────────────────
13             Icosaedro (Ih)
20-75          Icosaedro (Ih)
75-150         Competencia Ih ↔ Dh
150-500        Decaedro (Dh) o FCC
> 500          FCC (bulk-like)
```

### Factores que Determinan la Estructura:

1. **Energía superficial**: Favorece Ih (máxima coordinación)
2. **Strain elástico**: Favorece FCC (sin tensión)
3. **Temperatura**: A alta T, pueden aparecer estructuras amorfas
4. **Elemento químico**: 
   - Metales nobles (Au, Ag, Cu): Prefieren Ih/Dh
   - Metales de transición (Pt, Pd): Mayor tendencia a FCC

### Conexión con Nuestros Resultados:

En nuestras simulaciones, usamos **icosaedros** porque:
- Son óptimos para N = 13, 55, 147 (magic numbers)
- Representan la estructura de mínima energía para estos tamaños
- Son fácilmente generables con ASE
"""

# CELDA MARKDOWN 3: Pregunta 2 - Magic numbers
"""
## 🔷 Pregunta 2: ¿Cómo afecta el "magic number" a la estabilidad?

### Respuesta:

Los **"magic numbers"** son tamaños específicos de clusters que presentan **estabilidad excepcional** debido a que completan capas atómicas cerradas, maximizando la coordinación y minimizando la energía superficial.

### Definición de Magic Numbers:

Un magic number N* es un tamaño donde:
1. Se completa una **capa geométrica cerrada**
2. La **energía de cohesión** (por átomo) muestra un **máximo local**
3. La **energía de disociación** (para remover un átomo) es **máxima**

### Magic Numbers para Icosaedros:

La fórmula para icosaedros es:

**N(n) = (10n³ + 15n² + 11n + 3) / 3**

donde n = número de capas.

| n (capas) | N (átomos) | Tipo |
|-----------|------------|------|
| 1 | **13** | Magic number |
| 2 | **55** | Magic number |
| 3 | **147** | Magic number |
| 4 | **309** | Magic number |
| 5 | **561** | Magic number |

### ¿Por qué son tan estables?

#### 1. **Máxima Coordinación**
- Cada átomo tiene el **máximo número de vecinos** posible
- Minimiza los enlaces "colgantes" (dangling bonds)
- Ejemplo: En Ih₅₅, los átomos internos tienen 12 vecinos (coordinación FCC completa)

#### 2. **Cierre de Capas**
- Similar a los gases nobles en química atómica
- La última capa está **completamente llena**
- Agregar un átomo más requiere **iniciar una nueva capa** → energéticamente costoso

#### 3. **Barrera Energética**
- La energía de disociación D(N) = E(N-1) - E(N) muestra picos en magic numbers
- Ejemplo: Remover un átomo de Ih₅₅ requiere más energía que de Ih₅₄

### Evidencia Experimental:

Los magic numbers se observan en:
- **Espectroscopía de masas**: Picos de abundancia en N = 13, 55, 147...
- **Experimentos de colisión**: Mayor resistencia a fragmentación
- **Síntesis química**: Mayor probabilidad de formación

### Efecto en Propiedades:

| Propiedad | En Magic Numbers | Entre Magic Numbers |
|-----------|------------------|---------------------|
| Estabilidad térmica | ↑ Alta | ↓ Baja |
| Reactividad química | ↓ Baja (inertes) | ↑ Alta |
| Punto de fusión | ↑ Más alto | ↓ Más bajo |
| Energía de ionización | ↑ Máxima | ↓ Menor |

### Conexión con Nuestros Resultados:

En nuestro análisis:
- Usamos noshells = 1, 2, 3, 4 → N = 13, 55, 147, 309 (¡todos magic numbers!)
- Esto explica por qué las curvas de energía/átomo son tan suaves
- Si hubiéramos incluido N = 50 o N = 100, veríamos "saltos" en las curvas

### Aplicaciones Prácticas:

1. **Catálisis**: Clusters de magic numbers son menos reactivos → no ideales
2. **Óptica**: Plasmones más definidos en magic numbers (Au, Ag)
3. **Magnetismo**: Momentos magnéticos anómalos en magic numbers (Fe, Co)
"""

# CELDA MARKDOWN 4: Pregunta 3 - Transición icosaédrica-decaédrica
"""
## 🔷 Pregunta 3: ¿Qué es la transición icosaédrica-decaédrica?

### Respuesta:

La **transición icosaédrica-decaédrica (Ih → Dh)** es un **cambio estructural** que ocurre en nanoclusters metálicos cuando el tamaño aumenta, pasando de una morfología icosaédrica (Ih) a una decaédrica (Dh).

### Descripción del Fenómeno:

#### Estructura Icosaédrica (Ih)
- **Geometría**: 20 caras triangulares, 12 vértices
- **Simetría**: Icosaédrica (Ih) - 5 ejes de rotación
- **Ventaja**: Máxima coordinación superficial → mínima energía superficial
- **Desventaja**: **Strain elástico interno** debido a la incompatibilidad con redes cristalinas

#### Estructura Decaédrica (Dh)
- **Geometría**: 5 tetraedros gemelos (twin tetrahedra) unidos
- **Simetría**: Pentagonal (D₅h)
- **Ventaja**: **Menor strain** que Ih para tamaños intermedios
- **Desventaja**: Menor coordinación superficial que Ih

### ¿Por qué ocurre la transición?

La competencia entre dos energías:

**E_total = E_superficie + E_strain**

- **Clusters pequeños (N < 75)**:
  - E_superficie domina
  - Ih minimiza E_superficie → **Ih es estable**

- **Clusters intermedios (75 < N < 150)**:
  - E_strain crece con N³ (volumen)
  - E_superficie crece con N²/³ (área)
  - **Crossover**: Dh tiene mejor balance → **Dh es estable**

- **Clusters grandes (N > 150)**:
  - E_strain domina completamente
  - FCC (sin strain) es óptimo → **FCC es estable**

### Tamaño Crítico de Transición:

Según Baletto & Ferrando, el tamaño crítico depende del metal:

| Metal | N_crítico (Ih → Dh) | Observación |
|-------|---------------------|-------------|
| **Au** | ~75-80 átomos | Transición gradual |
| **Ag** | ~80-90 átomos | Similar a Au |
| **Cu** | ~70-75 átomos | Transición más temprana |
| **Pt** | ~100 átomos | Prefiere FCC antes |
| **Pd** | ~90-100 átomos | Transición tardía |

### Factores que Influencian la Transición:

#### 1. **Temperatura**
- **T baja**: Estructura de mínima energía (Ih o Dh según N)
- **T alta**: Pueden coexistir múltiples isómeros
- **T muy alta**: Fusión superficial → estructuras amorfas

#### 2. **Elemento Químico**
- **Metales nobles** (Au, Ag, Cu): Clara transición Ih → Dh
- **Metales de transición** (Pt, Pd): Tendencia a FCC más temprana
- **Parámetro clave**: Relación entre energía superficial y módulo elástico

#### 3. **Método de Síntesis**
- **Síntesis química**: Cinética puede atrapar estructuras metaestables
- **Deposición en fase vapor**: Favorece estructuras de equilibrio
- **Enfriamiento rápido**: Puede "congelar" estructuras de alta T

### Evidencia Experimental:

La transición Ih → Dh se ha observado mediante:
- **Microscopía electrónica de transmisión (TEM)**: Imágenes directas
- **Difracción de electrones**: Patrones de simetría
- **Espectroscopía de masas**: Cambios en abundancia relativa

### Diagrama de Fases Estructurales:

```
Tamaño (N) →
────────────────────────────────────────────
     Ih         Ih/Dh        Dh         FCC
  (N<75)     (75<N<150)  (150<N<500)  (N>500)
    │            │           │          │
    └─ Máxima ──┴─ Balance ─┴─ Mínimo ─┘
       coord.      óptimo      strain
```

### Conexión con Nuestros Resultados:

En nuestras simulaciones:
- Usamos **solo icosaedros** (N = 13, 55, 147, 309)
- N = 147 está **cerca del límite** de estabilidad Ih
- Para N = 309, en la realidad podría ser **decaédrico** o incluso FCC
- EMT no captura perfectamente el strain → puede sobrestimar estabilidad de Ih

### Implicaciones Prácticas:

1. **Catálisis**: 
   - Ih tiene más sitios activos (vértices, aristas)
   - Dh tiene caras {111} más extensas → diferente selectividad

2. **Óptica (Plasmones)**:
   - Ih: Resonancia más aguda
   - Dh: Resonancia más ancha (múltiples modos)

3. **Magnetismo**:
   - Estructura afecta acoplamiento de espines
   - Transición puede cambiar propiedades magnéticas

### Conclusión:

La transición Ih → Dh es un ejemplo fascinante de cómo la **competencia entre efectos superficiales y volumétricos** determina la estructura de nanomateriales. Entender esta transición es crucial para diseñar nanopartículas con propiedades específicas.
"""

# CELDA MARKDOWN 5: Conclusiones finales de la investigación
"""
## 📝 Conclusiones de la Investigación Bibliográfica

### Síntesis de Hallazgos Clave (Baletto & Ferrando, 2005):

1. **Estructuras de Clusters Pequeños**:
   - Dominan morfologías no cristalinas (Ih, Dh)
   - Magic numbers (13, 55, 147...) muestran estabilidad excepcional
   - La estructura depende del balance energía superficial vs. strain

2. **Transiciones Estructurales**:
   - Ih → Dh ocurre alrededor de N ≈ 75-100 átomos
   - Dh → FCC ocurre alrededor de N ≈ 150-500 átomos
   - Las transiciones son sensibles a temperatura y elemento químico

3. **Efectos Termodinámicos**:
   - Temperatura induce fluctuaciones estructurales
   - Pueden coexistir múltiples isómeros a T alta
   - Fusión superficial precede a fusión completa

4. **Efectos Cinéticos**:
   - Barreras energéticas pueden atrapar estructuras metaestables
   - Método de síntesis influye en morfología final
   - Recocido térmico puede inducir transiciones estructurales

### Conexión con Nuestro Trabajo Computacional:

| Aspecto | Artículo de Referencia | Nuestras Simulaciones |
|---------|------------------------|----------------------|
| **Estructuras** | Ih, Dh, FCC | Solo Ih (simplificación) |
| **Tamaños** | 10-10000 átomos | 13-309 átomos (magic numbers) |
| **Método** | DFT, potenciales empíricos | EMT (potencial empírico) |
| **Temperatura** | 0-1000 K | 100-700 K (Tarea 2) |
| **Metales** | Au, Ag, Cu, Pt, Pd, Ni | Ag, Cu, Pd, Au |

### Validación de Nuestros Resultados:

✅ **Confirmado**:
- Energía/átomo disminuye con tamaño (efecto de superficie)
- Magic numbers (13, 55, 147) son estables
- Expansión térmica aumenta con T
- Pd es más estable térmicamente que Cu

⚠️ **Limitaciones de EMT**:
- No captura transiciones Ih → Dh (requiere DFT)
- Subestima efectos cuánticos en clusters muy pequeños
- No incluye efectos relativistas (importantes para Au)

### Recomendaciones para Estudios Futuros:

1. **Explorar estructuras Dh y FCC** para N > 100
2. **Usar DFT** para clusters pequeños (N < 20) para mayor precisión
3. **Simular recocido térmico** (heating/cooling cycles) para observar transiciones
4. **Incluir efectos de soporte** (clusters depositados en superficies)
5. **Estudiar reactividad química** (adsorción de moléculas)

### Reflexión Final:

El artículo de Baletto & Ferrando (2005) sigue siendo una referencia fundamental en nanociencia. Nuestras simulaciones, aunque simplificadas, capturan las tendencias esenciales y nos permiten comprender los principios físicos que gobiernan el comportamiento de nanoclusters metálicos.

**Mensaje clave**: La estructura de nanopartículas es el resultado de una delicada competencia entre efectos superficiales, volumétricos y térmicos. Controlar esta competencia es la clave para diseñar nanomateriales con propiedades a medida.

---

**Referencias Adicionales Recomendadas**:
- Cleveland, C. L., et al. (1997). "Structural transitions in nanoclusters." *Phys. Rev. Lett.* 79, 1873.
- Doye, J. P. K., & Wales, D. J. (1998). "Global minima for transition metal clusters." *J. Chem. Soc., Faraday Trans.* 93, 4233.
- Marks, L. D. (1994). "Experimental studies of small particle structures." *Rep. Prog. Phys.* 57, 603.
"""
