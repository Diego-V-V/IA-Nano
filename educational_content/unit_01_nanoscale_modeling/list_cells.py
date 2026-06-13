"""
Script to add result explanation cells after every code cell that produces output.
"""
import json

NOTEBOOK_PATH = r'c:\IA Nanotecnología\Antigravity-Nano-Research-Multiagentic-Core-main\educational_content\unit_01_nanoscale_modeling\Tarea_1_nueva.ipynb'

with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Print current cell structure
for i, c in enumerate(nb['cells']):
    t = c['cell_type'][:4]
    cid = c['id']
    print(f"{i:3d} [{t}] id={cid}")
