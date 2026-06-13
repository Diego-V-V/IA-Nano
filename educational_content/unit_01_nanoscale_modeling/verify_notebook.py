import json
import os

file_path = "TAREA_1.ipynb"

try:
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo {file_path} no existe.")
        exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cells = data.get('cells', [])
    print(f"JSON valido. Total de celdas: {len(cells)}")
    
    found_t2 = False
    found_t3 = False
    
    for i, cell in enumerate(cells):
        source = "".join(cell.get('source', []))
        if "TAREA 2" in source:
            print(f"Tarea 2 encontrada en celda {i}")
            found_t2 = True
        if "TAREA 3" in source:
            print(f"Tarea 3 encontrada en celda {i}")
            found_t3 = True
            
    if found_t2 and found_t3:
        print("\nCONCLUSION: El archivo contiene las nuevas tareas correctamente.")
    else:
        print("\nADVERTENCIA: Faltan tareas en el archivo.")

except json.JSONDecodeError as e:
    print(f"Error de JSON: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
