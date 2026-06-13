import json

notebook_path = "TAREA_1_COMPLETA.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find the first code cell (usually imports)
found = False
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        # Check if %matplotlib inline is already there
        source = "".join(cell['source'])
        if "%matplotlib inline" in source:
            print("El notebook ya tiene %matplotlib inline")
            found = True
            break
        
        # Add it to the top of the imports
        print("Agregando %matplotlib inline a la primera celda de código...")
        cell['source'].insert(0, "%matplotlib inline\n")
        found = True
        break

if not found:
    print("No se encontró ninguna celda de código para arreglar.")
else:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=4, ensure_ascii=False)
    print("Corrección aplicada exitosamente.")
