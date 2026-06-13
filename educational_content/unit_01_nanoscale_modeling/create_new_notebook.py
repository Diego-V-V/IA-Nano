import json
import os

source_path = "TAREA_1.ipynb"
dest_path = "TAREA_1_COMPLETA.ipynb"

if not os.path.exists(source_path):
    print(f"Error: {source_path} no existe.")
    exit(1)

with open(source_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Optional: Add a small markdown cell at the top indicating this is the unified version
intro_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# TAREA 1 COMPLETA: Análisis, Temperatura e Investigación\n",
        "\n",
        "Este notebook consolida todo el trabajo realizado:\n",
        "1. **Tarea 1**: Análisis de nanopartículas (Ag, Cu, Pd, Au)\n",
        "2. **Tarea 2**: Efectos de Temperatura (MD)\n",
        "3. **Tarea 3**: Investigación Bibliográfica\n",
        "\n",
        "Generado automáticamente para asegurar la integridad del contenido."
    ]
}

# Insert intro cell at index 0
data['cells'].insert(0, intro_cell)

with open(dest_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Creado nuevo notebook: {dest_path}")
print(f"Total celdas: {len(data['cells'])}")
