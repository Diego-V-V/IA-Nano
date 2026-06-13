"""
Script to add explanation cells after every code cell that produces results.
Inserts markdown cells explaining what the results/output mean.
"""
import json

NOTEBOOK_PATH = r'c:\IA Nanotecnologia\Antigravity-Nano-Research-Multiagentic-Core-main\educational_content\unit_01_nanoscale_modeling\Tarea_1_nueva.ipynb'

# Try with tilde
try:
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)
except FileNotFoundError:
    NOTEBOOK_PATH = r'c:\IA Nanotecnología\Antigravity-Nano-Research-Multiagentic-Core-main\educational_content\unit_01_nanoscale_modeling\Tarea_1_nueva.ipynb'
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

def make_md(cell_id, lines):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": lines
    }

# Cells to insert AFTER specific code cell IDs
new_cells = {
    "imports-cell": make_md("explain-imports", [
        "### Sobre las librerías utilizadas\n",
        "\n",
        "- **ASE (Atomic Simulation Environment):** Librería principal para crear y manipular estructuras atómicas. Proporciona los módulos `Icosahedron` para crear clusters, `EMT` como calculadora de energía, `BFGS` para optimización y `Langevin` para dinámica molecular.\n",
        "- **NumPy:** Para cálculos numéricos eficientes (vectores de posiciones, promedios, desviaciones).\n",
        "- **Matplotlib:** Para generar todas las gráficas de resultados.\n",
        "- **Pandas:** Para organizar datos en tablas comparativas legibles.\n",
        "\n",
        "Si esta celda imprime el mensaje de confirmación, todas las dependencias están instaladas correctamente y podemos proceder."
    ]),

    "comparative-analysis": make_md("explain-comp-table", [
        "### Interpretación de la Tabla Comparativa\n",
        "\n",
        "La tabla anterior muestra las propiedades estructurales de los tres metales lado a lado. Aspectos clave a observar:\n",
        "\n",
        "- **Columna `E_per_atom`:** Valores más bajos (más negativos) indican mayor estabilidad. Compare cómo cada metal se estabiliza a medida que aumenta el número de átomos. El gradiente de color (rojo = más alto, verde = más bajo) facilita identificar rápidamente cuál metal es más estable.\n",
        "- **Columna `surface_fraction`:** Note que esta fracción es idéntica para los tres metales al mismo número de capas, porque depende solo de la geometría icosaédrica, no del elemento.\n",
        "- **Columna `radius`:** Los diferentes radios reflejan los radios atómicos intrínsecos de cada metal: Ag > Pd > Cu.\n",
        "\n",
        "**Conclusión clave:** La tabla confirma que mientras la geometría es universal, la energética es específica de cada material."
    ]),

    "comparative-plots": make_md("explain-comp-plots", [
        "### Interpretación de los Gráficos Comparativos\n",
        "\n",
        "Los tres paneles muestran:\n",
        "\n",
        "1. **Estabilidad Energética (izquierda):** Las tres curvas descienden con el tamaño del cluster. La separación vertical entre curvas indica diferencias en la energía de cohesión entre metales. Un metal cuya curva está más abajo es intrínsecamente más estable.\n",
        "\n",
        "2. **Radio de Equilibrio (centro):** Las curvas son paralelas pero desplazadas verticalmente según el radio atómico de cada metal. Ag tiene el mayor radio, Cu el menor. Esto afecta directamente la densidad y el área superficial de las nanopartículas.\n",
        "\n",
        "3. **Fracción de Superficie (derecha):** Las tres curvas se superponen casi perfectamente, confirmando que la fracción de átomos superficiales depende exclusivamente de la geometría (número de capas), no del material. Esta es una propiedad puramente geométrica del icosaedro.\n",
        "\n",
        "**Mensaje principal:** A escala nanométrica, la geometría dicta la estructura, pero la química del material dicta la energía."
    ]),

    "md-ag": make_md("explain-md-ag", [
        "### Interpretación de los Resultados MD — Plata (Ag)\n",
        "\n",
        "Los cuatro paneles muestran el comportamiento de la nanopartícula de Ag bajo diferentes temperaturas:\n",
        "\n",
        "1. **Energía Potencial (arriba izq.):** Cada línea de color es una temperatura distinta. A 100K la energía oscila suavemente (átomos vibran poco). A 700K las oscilaciones son amplias y pueden mostrar saltos, indicando que los átomos se mueven significativamente de sus posiciones.\n",
        "\n",
        "2. **Expansión Térmica (arriba der.):** Cada punto rojo es el radio promedio del cluster a esa temperatura. Si la curva sube de izquierda a derecha, el cluster se expande al calentarse — esto es la expansión térmica a nanoescala.\n",
        "\n",
        "3. **Fluctuaciones de Energía (abajo izq.):** Las barras muestran cuánto oscila la energía a cada temperatura. Barras más altas = más agitación térmica. Un aumento desproporcionado a temperaturas altas puede indicar el inicio de fusión.\n",
        "\n",
        "4. **MSD — Movilidad Atómica (abajo der.):** El MSD (Mean Square Displacement) mide cuánto se han movido los átomos desde su posición inicial. Si la curva se aplana, los átomos solo vibran. Si sube continuamente, los átomos están difundiendo — un signo de que el cluster se está fundiendo."
    ]),

    "md-cu": make_md("explain-md-cu", [
        "### Interpretación de los Resultados MD — Cobre (Cu)\n",
        "\n",
        "Compare estos resultados con los de Ag:\n",
        "\n",
        "1. **Energía Potencial:** Las oscilaciones deberían ser de menor amplitud que en Ag a la misma temperatura, porque Cu tiene enlaces más fuertes. Esto se traduce en mayor estabilidad térmica.\n",
        "\n",
        "2. **Expansión Térmica:** El radio promedio de Cu debería expandirse menos que Ag al mismo rango de temperaturas. Esto refleja la mayor rigidez del enlace Cu-Cu.\n",
        "\n",
        "3. **Fluctuaciones de Energía:** Las barras deberían ser más bajas que las de Ag, confirmando que Cu requiere más energía para desestabilizarse.\n",
        "\n",
        "4. **MSD:** La movilidad de los átomos de Cu debería ser menor que en Ag. Si a 700K el MSD de Ag muestra difusión pero el de Cu no, esto indica que el cluster de Cu todavía mantiene su estructura a esa temperatura.\n",
        "\n",
        "**Punto importante:** El punto de fusión del Cu bulk (1358K) es mayor que el de Ag (1235K), y esta diferencia se refleja en los nanoclusters."
    ]),

    "md-pd": make_md("explain-md-pd", [
        "### Interpretación de los Resultados MD — Paladio (Pd)\n",
        "\n",
        "Pd debería mostrar el comportamiento más estable de los tres metales:\n",
        "\n",
        "1. **Energía Potencial:** Las oscilaciones deberían ser las de menor amplitud entre los tres metales. Pd tiene la mayor energía de cohesión, por lo que sus átomos están más firmemente ligados.\n",
        "\n",
        "2. **Expansión Térmica:** La menor expansión entre los tres metales. El alto punto de fusión del Pd (1828K) significa que 700K representa solo ~38% de su temperatura de fusión, así que el cluster debería permanecer estructuralmente intacto.\n",
        "\n",
        "3. **Fluctuaciones de Energía:** Las barras más bajas de los tres metales, confirmando la mayor estabilidad.\n",
        "\n",
        "4. **MSD:** El MSD más bajo a todas las temperaturas. Incluso a 700K, los átomos de Pd probablemente solo vibren alrededor de sus posiciones de equilibrio sin difundir.\n",
        "\n",
        "**Aplicación práctica:** Esta resistencia térmica es exactamente la razón por la cual las nanopartículas de Pd se usan como catalizadores en reacciones a alta temperatura (como los convertidores catalíticos en automóviles)."
    ]),

    "temp-comparative": make_md("explain-temp-comparative", [
        "### Interpretación de los Resultados Comparativos de Temperatura\n",
        "\n",
        "**Gráfico de 3 paneles:**\n",
        "\n",
        "1. **Estabilidad (izq.):** Las tres curvas muestran la energía promedio por átomo en función de la temperatura. La pendiente de cada curva está relacionada con la capacidad calorífica del nanocluster. Una pendiente mayor indica que el material absorbe más energía por grado de temperatura.\n",
        "\n",
        "2. **Expansión Térmica Relativa (centro):** Este gráfico normaliza la expansión respecto al valor a 100K, permitiendo comparar directamente qué material se expande más proporcionalmente. El metal con la curva más empinada es el más sensible térmicamente.\n",
        "\n",
        "3. **Movilidad a 700K (der.):** Las barras comparan directamente la movilidad atómica al punto más caliente. El metal con la barra más alta tiene los átomos más móviles y, por lo tanto, es el más cercano a fundirse.\n",
        "\n",
        "**Tabla Comparativa:**\n",
        "\n",
        "La tabla con gradiente de colores permite identificar rápidamente:\n",
        "- **Colores fríos (amarillo claro):** Valores bajos de fluctuación = mayor estabilidad\n",
        "- **Colores cálidos (rojo):** Valores altos = mayor inestabilidad/movilidad\n",
        "\n",
        "**Orden de estabilidad térmica:** Pd > Cu > Ag. Este resultado es consistente con los puntos de fusión bulk: Pd (1828K) > Cu (1358K) > Ag (1235K)."
    ])
}

# Build id-to-index map
cells = nb['cells']
id_map = {c['id']: i for i, c in enumerate(cells)}

# Collect insertions (in reverse order to preserve indices)
insertions = []
for target_id, new_cell in new_cells.items():
    if target_id in id_map:
        # Check if the next cell already is our explanation (avoid duplicates)
        idx = id_map[target_id]
        next_idx = idx + 1
        if next_idx < len(cells) and cells[next_idx]['id'] == new_cell['id']:
            print(f"  Skipping {new_cell['id']} (already exists)")
            continue
        insertions.append((next_idx, new_cell))
        print(f"  Will insert '{new_cell['id']}' after '{target_id}' (position {next_idx})")
    else:
        print(f"  WARNING: target cell '{target_id}' not found!")

# Sort reverse by index and insert
insertions.sort(key=lambda x: x[0], reverse=True)
for idx, cell in insertions:
    cells.insert(idx, cell)

nb['cells'] = cells
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\nDone! Notebook now has {len(cells)} cells.")
