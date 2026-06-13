from ase.cluster import Icosahedron
from ase.calculators.emt import EMT
from ase.md.langevin import Langevin
from ase import units
import numpy as np
import json

def run_headless():
    print("Iniciando simulación headless...")
    try:
        atoms = Icosahedron('Ag', noshells=2)
        atoms.calc = EMT()
        dyn = Langevin(atoms, timestep=1.0*units.fs, temperature_K=300, friction=0.01)
        
        energies = []
        def collect():
            energies.append(float(atoms.get_potential_energy()))
        
        dyn.attach(collect, interval=1)
        dyn.run(50)
        
        data = {
            "energies_len": len(energies),
            "energies_sample": energies[:5],
            "is_nan": any(np.isnan(energies))
        }
        
        with open("debug_data.json", "w") as f:
            json.dump(data, f)
        print("Datos guardados en debug_data.json")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        with open("debug_error.txt", "w") as f:
            f.write(str(e))

if __name__ == "__main__":
    run_headless()
