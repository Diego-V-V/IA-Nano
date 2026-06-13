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

# Find plot_individual_analysis and plot_comparative_final
modified = False

# Function to patch plot line
# Current: axes[0].plot(results_dict[t]['time'], results_dict[t]['energies'], ...)
# New: axes[0].plot(np.arange(len(results_dict[t]['energies'])), results_dict[t]['energies'], ...)
# OR even simpler: just fix it inside the loop

print("Scanning cells...")
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        new_source = []
        cell_modified = False
        source_str = "".join(cell['source'])
        
        # Patching plot_individual_analysis
        if "def plot_individual_analysis" in source_str:
            print(f"Index {i}: Found plot_individual_analysis. Patching...")
            for line in cell['source']:
                # The critical line causing error
                if "axes[0].plot(results_dict[t]['time'], results_dict[t]['energies']" in line:
                    # Replace with dynamic range
                    new_line = line.replace("results_dict[t]['time']", "np.arange(len(results_dict[t]['energies']))")
                    new_source.append(new_line)
                    cell_modified = True
                    modified = True
                
                # Also check MSD plot just in case
                elif "axes[2].plot(results_dict[t]['time'], results_dict[t]['msd']" in line:
                    new_line = line.replace("results_dict[t]['time']", "np.arange(len(results_dict[t]['msd']))")
                    new_source.append(new_line)
                    cell_modified = True
                    modified = True
                else:
                    new_source.append(line)
            
            if cell_modified:
                cell['source'] = new_source

print("Scanning for comparative plot...")
# We need to re-scan because we might have modified the list in place if we were iterating directly, 
# but here we iterate enumerate(nb['cells']) which is safe for modification of *content* of cells, but let's be safe.
# Actually the loop finishes for one cell before moving to next.

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        # Skip if already modified in this loop (unlikely since functions are in different cells usually)
        # Patching plot_comparative_final
        # The comparative plot uses `results_ag` etc directly.
        pass 
        # Actually comparative plot uses 'avg_e' which is calculated from mean.
        # It plots `temps` vs `avg_e`. `temps` comes from keys. `avg_e` comes from values.
        # So comparative plot shouldn't have dimension mismatch unless `temps` and `avg_e` mismatch?
        # `temps = sorted(res.keys())`
        # `avg_e = [np.mean(res[t]['energies'])/55 for t in temps]`
        # This part is safe from the specific array dimension error we saw.
        # The error was in `axes[0].plot(..., 'energies')`.
        
if modified:
    print("Writing modified notebook...")
    with open(notebook_filename, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=4)
    print("Notebook updated successfully. Plotting functions patched for robustness.")
else:
    print("Warning: Could not find the specific plotting lines to fix. They might already be patched.")
