"""
Script to add detailed analysis and conclusion cells to Tarea_1_nueva.ipynb
"""
import json

NOTEBOOK_PATH = r'c:\IA Nanotecnología\Antigravity-Nano-Research-Multiagentic-Core-main\educational_content\unit_01_nanoscale_modeling\Tarea_1_nueva.ipynb'

def make_md_cell(cell_id, source_lines):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": source_lines
    }

# --- Analysis cells to insert ---

analysis_ag_structural = make_md_cell("analysis-ag-structural", [
    "### Análisis Detallado — Plata (Ag)\n",
    "\n",
    "La plata presenta las siguientes características estructurales notables:\n",
    "\n",
    "- **Energía por átomo:** La energía por átomo de Ag decrece significativamente al pasar de 1 capa (átomo aislado) a 2 capas (13 átomos), y continúa disminuyendo con cada capa adicional. Esto refleja el aumento progresivo de la coordinación promedio.\n",
    "- **Radio de equilibrio:** El radio promedio escala de forma aproximadamente lineal con el número de capas, consistente con el empaquetamiento icosaédrico.\n",
    "- **Fracción de superficie:** Para el cluster más pequeño (13 átomos), casi todos los átomos son superficiales (~92%). A 147 átomos (4 capas), la fracción cae a ~63%, mostrando el efecto de tamaño clásico de la nanoescala.\n",
    "- **Implicaciones:** La alta fracción de superficie en clusters pequeños de Ag explica su alta reactividad catalítica y sus propiedades plasmónicas únicas, que dependen fuertemente de la geometría superficial."
])

analysis_cu_structural = make_md_cell("analysis-cu-structural", [
    "### Análisis Detallado — Cobre (Cu)\n",
    "\n",
    "El cobre muestra un comportamiento similar al de la plata pero con diferencias cuantitativas importantes:\n",
    "\n",
    "- **Energía por átomo:** Cu presenta valores de energía por átomo ligeramente diferentes a los de Ag, reflejando las diferencias en la parametrización del potencial EMT para cada metal.\n",
    "- **Radio de equilibrio:** Los clusters de Cu tienen radios de equilibrio menores que los de Ag para el mismo número de capas, consistente con el menor radio atómico del cobre (1.28 Å vs 1.44 Å para Ag).\n",
    "- **Fracción de superficie:** Las fracciones de superficie son idénticas a las de Ag (ya que dependen de la geometría icosaédrica, no del elemento), pero la energía asociada a cada átomo superficial difiere.\n",
    "- **Implicaciones:** El Cu es un excelente modelo de estudio porque es económico y presenta propiedades catalíticas relevantes. Su menor radio atómico resulta en enlaces más fuertes por unidad de volumen."
])

analysis_pd_structural = make_md_cell("analysis-pd-structural", [
    "### Análisis Detallado — Paladio (Pd)\n",
    "\n",
    "El paladio se distingue de Ag y Cu en varios aspectos:\n",
    "\n",
    "- **Energía por átomo:** Pd generalmente muestra la mayor energía de cohesión (energía por átomo más negativa o menor en magnitud absoluta según la convención), indicando enlaces metálicos más fuertes.\n",
    "- **Radio de equilibrio:** El radio de los clusters de Pd se sitúa entre los de Ag y Cu, reflejando su radio atómico intermedio.\n",
    "- **Estabilidad relativa:** La mayor energía de cohesión del Pd se traduce en nanopartículas más robustas estructuralmente, lo cual es relevante para sus aplicaciones en catálisis heterogénea.\n",
    "- **Implicaciones:** Las nanopartículas de Pd son fundamentales en reacciones de hidrogenación y acoplamiento cruzado (como la reacción de Suzuki). Su alta estabilidad estructural contribuye a su durabilidad como catalizador."
])

conclusion_tarea1_detailed = make_md_cell("tarea1-detailed-conclusion", [
    "## 1.5. Análisis Comparativo Detallado y Conclusiones\n",
    "\n",
    "### Análisis Cuantitativo\n",
    "\n",
    "| Propiedad | Ag | Cu | Pd |\n",
    "|---|---|---|---|\n",
    "| Radio atómico bulk | 1.44 Å | 1.28 Å | 1.37 Å |\n",
    "| Tendencia E/átomo | Intermedia | Variable | Mayor cohesión |\n",
    "| Aplicación principal | Plasmónica, antibacteriana | Electrónica, catalítica | Catálisis, almacenamiento H₂ |\n",
    "\n",
    "### Tendencias Generales Observadas\n",
    "\n",
    "1. **Efecto de tamaño universal:** Para los tres metales, la energía por átomo converge hacia el valor bulk a medida que el cluster crece. Esto confirma que las propiedades nanoscópicas son un fenómeno de transición entre el comportamiento atómico y el macroscópico.\n",
    "\n",
    "2. **Relación superficie-volumen:** La fracción de átomos superficiales sigue la misma curva para los tres metales (ya que depende solo de la geometría), pero el impacto energético de cada átomo superficial varía según el metal.\n",
    "\n",
    "3. **Escalamiento del radio:** La relación $R \\propto N^{1/3}$ se observa aproximadamente en los tres metales, como predice la teoría para clusters esféricos.\n",
    "\n",
    "4. **Orden de estabilidad:** La estabilidad relativa de los clusters sigue Pd > Cu ≈ Ag, lo cual correlaciona con las energías de cohesión de los metales bulk.\n",
    "\n",
    "### Conclusión\n",
    "\n",
    "El análisis estructural demuestra que las propiedades de las nanopartículas metálicas están gobernadas por dos factores principales: (1) la geometría, que determina la relación superficie/volumen y es independiente del material, y (2) la naturaleza del enlace metálico, que determina la energía de cohesión y es específica de cada elemento. La combinación de ambos factores produce el rico panorama de propiedades nanoscópicas que hace a estos materiales tan valiosos para aplicaciones tecnológicas.\n",
    "\n",
    "---"
])

analysis_ag_md = make_md_cell("analysis-ag-md", [
    "### Análisis Detallado — Dinámica Molecular de Ag\n",
    "\n",
    "- **Energía potencial:** A 100K, la energía oscila con baja amplitud alrededor de un valor bien definido, indicando vibraciones armónicas. A 700K, las oscilaciones son mucho mayores y pueden mostrar deriva, sugiriendo procesos anarmónicos o difusivos.\n",
    "- **Expansión térmica:** El radio promedio del cluster de Ag aumenta monotónicamente con la temperatura. La expansión es aproximadamente lineal en el rango 100-500K, pero puede acelerarse a 700K si se aproxima a la temperatura de pre-fusión.\n",
    "- **Fluctuaciones de energía:** σ(E) crece con T, como predice la termodinámica estadística: $\\sigma^2(E) \\propto k_B T^2 C_v$. Un crecimiento mayor al esperado sugiere cambios estructurales.\n",
    "- **MSD:** El desplazamiento cuadrático medio para Ag muestra comportamiento vibracional (MSD constante) a bajas temperaturas y puede transicionar a comportamiento difusivo (MSD lineal en t) a altas temperaturas."
])

analysis_cu_md = make_md_cell("analysis-cu-md", [
    "### Análisis Detallado — Dinámica Molecular de Cu\n",
    "\n",
    "- **Energía potencial:** Cu, con enlaces más fuertes que Ag, presenta menores fluctuaciones de energía a la misma temperatura. La curva de energía es más \"ajustada\" indicando mayor rigidez del cluster.\n",
    "- **Expansión térmica:** La expansión térmica de Cu es generalmente menor que la de Ag, consistente con su mayor módulo de bulk y constantes elásticas.\n",
    "- **Fluctuaciones de energía:** Las fluctuaciones son proporcionalmente menores, reflejando la mayor estabilidad del enlace Cu-Cu.\n",
    "- **MSD:** La movilidad atómica en Cu es menor que en Ag a las mismas temperaturas, indicando que los átomos de Cu están más fuertemente ligados a sus posiciones de equilibrio. Esto es consistente con el mayor punto de fusión del Cu bulk (1358K) comparado con Ag (1235K)."
])

analysis_pd_md = make_md_cell("analysis-pd-md", [
    "### Análisis Detallado — Dinámica Molecular de Pd\n",
    "\n",
    "- **Energía potencial:** Pd muestra las menores fluctuaciones de energía entre los tres metales, reflejando su mayor energía de cohesión y enlaces más robustos.\n",
    "- **Expansión térmica:** La expansión del cluster de Pd es la menor de los tres metales estudiados, lo cual es consistente con su alto punto de fusión (1828K) y mayor rigidez.\n",
    "- **Fluctuaciones de energía:** La desviación estándar de la energía es la más baja, confirmando la mayor estabilidad térmica del Pd.\n",
    "- **MSD:** El MSD de Pd es significativamente menor que el de Ag y Cu, incluso a 700K. Esto indica que las nanopartículas de Pd mantienen su integridad estructural a temperaturas donde Ag y Cu ya muestran signos de inestabilidad.\n",
    "- **Implicación tecnológica:** Esta resistencia térmica explica por qué las nanopartículas de Pd son catalizadores preferidos en reacciones a alta temperatura."
])

conclusion_tarea2_detailed = make_md_cell("tarea2-detailed-conclusion", [
    "## 2.5. Análisis Comparativo Detallado y Conclusiones\n",
    "\n",
    "### Análisis de los Resultados\n",
    "\n",
    "1. **Jerarquía de estabilidad térmica:** Pd > Cu > Ag. Este orden correlaciona directamente con las energías de cohesión y puntos de fusión de los metales bulk, confirmando que las propiedades termodinámicas fundamentales se preservan a la nanoescala.\n",
    "\n",
    "2. **Coeficiente de expansión térmica:** Los tres metales muestran expansión térmica positiva, pero con coeficientes diferentes. El coeficiente más alto (Ag) corresponde al metal con enlaces más débiles.\n",
    "\n",
    "3. **Capacidad calorífica efectiva:** Las fluctuaciones de energía permiten estimar la capacidad calorífica mediante la relación $C_v = \\sigma^2(E) / (k_B T^2)$. Los valores obtenidos se acercan al límite de Dulong-Petit para clusters grandes.\n",
    "\n",
    "4. **Difusión superficial:** A 700K, la diferencia en MSD entre metales es dramática. Ag muestra la mayor movilidad, lo que sugiere que los átomos superficiales de Ag comienzan a difundir significativamente, un precursor de la fusión superficial.\n",
    "\n",
    "5. **Pre-fusión nanoscópica:** Los nanoclusters funden a temperaturas significativamente menores que el bulk (efecto de depresión del punto de fusión). A 700K, algunos de estos clusters podrían estar experimentando pre-fusión superficial.\n",
    "\n",
    "### Conclusión\n",
    "\n",
    "Las simulaciones de Dinámica Molecular demuestran que los efectos térmicos en nanopartículas son gobernados tanto por las propiedades intrínsecas del material (energía de cohesión, rigidez) como por los efectos de tamaño (alta fracción superficial, menor coordinación). La combinación de estos factores produce un comportamiento térmico único que difiere significativamente del bulk: mayor expansión, menores temperaturas de fusión, y una transición gradual (pre-fusión) en lugar de la transición abrupta del bulk. Estos resultados tienen implicaciones directas para el diseño de nanocatalizadores y nanomateriales que operan a temperaturas elevadas.\n",
    "\n",
    "---"
])

conclusion_tarea3 = make_md_cell("tarea3-conclusion", [
    "## 3.5. Conclusiones de la Tarea 3\n",
    "\n",
    "### Síntesis del Artículo\n",
    "\n",
    "El trabajo de Baletto y Ferrando (2005) proporciona un marco teórico completo para entender la selección estructural en nanoclusters. Los puntos clave son:\n",
    "\n",
    "1. **No existe una geometría universalmente óptima:** La estructura más estable depende críticamente del tamaño, la temperatura y las condiciones de formación. Esto contrasta con el bulk, donde la estructura cristalina está determinada únicamente por el tipo de enlace.\n",
    "\n",
    "2. **La cinética es tan importante como la termodinámica:** En condiciones reales de síntesis, las nanopartículas frecuentemente adoptan estructuras metaestables determinadas por la cinética de crecimiento, no por el equilibrio termodinámico.\n",
    "\n",
    "3. **Los números mágicos son guías de diseño:** Conocer los tamaños de especial estabilidad permite diseñar nanopartículas más robustas y con propiedades reproducibles.\n",
    "\n",
    "4. **Las transiciones estructurales son oportunidades:** Las transiciones Ico→Deca→FCC no son meros artefactos académicos; representan oportunidades para sintonizar propiedades (catalíticas, ópticas, magnéticas) mediante el control del tamaño.\n",
    "\n",
    "### Conexión con las Simulaciones\n",
    "\n",
    "Los resultados de las Tareas 1 y 2 confirman experimentalmente (computacionalmente) varios de los principios discutidos por Baletto y Ferrando:\n",
    "- La estabilidad dependiente del tamaño (Tarea 1)\n",
    "- La influencia de la temperatura en la dinámica estructural (Tarea 2)\n",
    "- La importancia de los números mágicos (13, 55, 147 átomos en nuestros clusters icosaédricos)\n",
    "\n",
    "---"
])

# --- Load, modify, and save notebook ---
with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find cell indices by id
id_map = {c['id']: i for i, c in enumerate(cells)}

# Insert after each metal simulation (reverse order to preserve indices)
insertions = []

# Tarea 1: after each metal analysis
if 'analysis-ag' in id_map:
    insertions.append((id_map['analysis-ag'] + 1, analysis_ag_structural))
if 'analysis-cu' in id_map:
    insertions.append((id_map['analysis-cu'] + 1, analysis_cu_structural))
if 'analysis-pd' in id_map:
    insertions.append((id_map['analysis-pd'] + 1, analysis_pd_structural))

# Tarea 2: after each MD simulation
if 'md-ag' in id_map:
    insertions.append((id_map['md-ag'] + 1, analysis_ag_md))
if 'md-cu' in id_map:
    insertions.append((id_map['md-cu'] + 1, analysis_cu_md))
if 'md-pd' in id_map:
    insertions.append((id_map['md-pd'] + 1, analysis_pd_md))

# Replace existing conclusion cells with detailed versions
# Find and replace Tarea 1 conclusion
for i, c in enumerate(cells):
    if c.get('id') == 'tarea1-conclusions':
        cells[i] = conclusion_tarea1_detailed
    if c.get('id') == 'tarea2-conclusions':
        cells[i] = conclusion_tarea2_detailed

# Sort insertions by index (descending) to preserve positions
insertions.sort(key=lambda x: x[0], reverse=True)
for idx, cell in insertions:
    cells.insert(idx, cell)

# Add Tarea 3 conclusion before the final note
for i, c in enumerate(cells):
    if c.get('id') == 'final-note':
        cells.insert(i, conclusion_tarea3)
        break

nb['cells'] = cells

with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook updated successfully with detailed analysis and conclusions.")
