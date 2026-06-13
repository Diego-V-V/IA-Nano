from ase.cluster import Icosahedron
from ase.calculators.emt import EMT
from ase.md.langevin import Langevin
from ase import units
import numpy as np
import time

def test_md():
    print("Probando simulación MD ultra-rápida (100 pasos)...")
    atoms = Icosahedron('Ag', noshells=2)
    atoms.calc = EMT()
    dyn = Langevin(atoms, timestep=1.0*units.fs, temperature_K=300, friction=0.01)
    
    energies = []
    def collect():
        energies.append(atoms.get_potential_energy())
    
    dyn.attach(collect, interval=1)
    start = time.time()
    dyn.run(100)
    end = time.time()
    print(f"Prueba exitosa. 100 pasos en {end-start:.2f} segundos.")
    print(f"Datos recolectados: {len(energies)}")

if __name__ == "__main__":
    test_md()
