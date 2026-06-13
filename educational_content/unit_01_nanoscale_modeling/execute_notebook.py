import sys
import os

try:
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
except ImportError:
    print("Error: nbformat or nbconvert not installed.")
    sys.exit(1)

notebook_path = "c:/IA Nanotecnología/Antigravity-Nano-Research-Multiagentic-Core-main/educational_content/unit_01_nanoscale_modeling/TAREA_1_COMPLETA.ipynb"
output_path = notebook_path

print(f"Executing notebook: {notebook_path}")

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    try:
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
    except Exception as e:
        print(f"Error executing the notebook: {e}")
        # Save even if error to inspect partial results
        pass
    
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
        
    print(f"Notebook executed and saved to {output_path}")

except Exception as e:
    print(f"Fatal error: {e}")
    sys.exit(1)
