import json

notebook_path = "TAREA_1.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

new_cells = []
seen_tarea2 = False
seen_tarea3 = False

for cell in notebook['cells']:
    source = "".join(cell.get('source', []))
    
    if "TAREA 2" in source:
        if seen_tarea2:
            continue # Skip duplicate
        seen_tarea2 = True
        
    if "TAREA 3" in source:
        if seen_tarea3:
            continue # Skip duplicate
        seen_tarea3 = True
        
    # Also filter the specific content cells to avoid dupes of those
    if "run_md_temperature_analysis" in source and "def" in source:
         # Check if we already have this function definition in new_cells
         # This is a bit heuristic but should work for this specific case
         is_dupe = False
         for existing_cell in new_cells:
             if "run_md_temperature_analysis" in "".join(existing_cell.get('source', [])):
                 is_dupe = True
                 break
         if is_dupe:
             continue

    new_cells.append(cell)

notebook['cells'] = new_cells

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=4, ensure_ascii=False)

print(f"Notebook limpiado. Total celdas: {len(new_cells)}")
