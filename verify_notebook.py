import json
import os

path = os.path.join(
    r"c:\IA Nanotecnología",
    "Antigravity-Nano-Research-Multiagentic-Core-main",
    "educational_content",
    "unit_03_ml_nanomaterials",
    "Investigacion_Unidad3_Secciones_0_a_03.ipynb"
)

nb = json.load(open(path, encoding='utf-8'))
print(f"Cells: {len(nb['cells'])}")

md_count = sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown')
code_count = sum(1 for c in nb['cells'] if c['cell_type'] == 'code')
print(f"Markdown: {md_count}, Code: {code_count}")

for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    ctype = c['cell_type']
    preview = src[:80].replace('\n', ' ')
    print(f"  Cell {i}: [{ctype:8s}] {preview}...")

print("Valid notebook format: OK")
