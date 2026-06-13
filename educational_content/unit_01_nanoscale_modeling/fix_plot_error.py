import json
import os
import sys

notebook_filename = "TAREA_1_FINAL_AGENTS.ipynb"

print(f"Reading {notebook_filename}...")
if not os.path.exists(notebook_filename):
    print("Notebook not found!")
    sys.exit(1)

with open(notebook_filename, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell containing run_md_temperature and fix the time array definition
modified = False
print("Scanning cells...")
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        new_source = []
        cell_modified = False
        for line in cell['source']:
            if "'time': np.arange(1500) * 1.0," in line:
                print(f"Index {i}: Found error line. Fixing...")
                # Change to dynamically use len(energies)
                new_line = line.replace("np.arange(1500)", "np.arange(len(energies))")
                new_source.append(new_line)
                cell_modified = True
                modified = True
            else:
                new_source.append(line)
        
        if cell_modified:
            cell['source'] = new_source

if modified:
    print("Writing modified notebook...")
    with open(notebook_filename, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=4)
    print("Notebook updated successfully. Time array length fixed.")
else:
    print("Warning: Could not find the specific line to fix. It might already be correct or the pattern does not match.")
