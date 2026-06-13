from ase.cluster import Icosahedron
from ase.calculators.emt import EMT
from ase.md.langevin import Langevin
from ase import units
import numpy as np
import sys

def diag():
    print("--- Diagnostic Start ---")
    try:
        print("Checking Icosahedron creation...")
        atoms = Icosahedron('Ag', noshells=2)
        print(f"Atoms created: {len(atoms)}")
        
        print("Checking EMT calculator...")
        atoms.calc = EMT()
        e_init = atoms.get_potential_energy()
        print(f"Initial Potential Energy: {e_init:.4f} eV")
        
        print("Setting up Langevin dynamics...")
        dyn = Langevin(atoms, timestep=1.0*units.fs, temperature_K=300, friction=0.01)
        
        energies = []
        def collect():
            energies.append(atoms.get_potential_energy())
        
        dyn.attach(collect, interval=1)
        
        print("Running 50 steps of MD...")
        dyn.run(50)
        
        print(f"Steps scheduled: 50")
        print(f"Energies collected: {len(energies)}")
        
        if len(energies) == 50:
            print("✅ Data collection working correctly.")
        else:
            print(f"❌ Data collection mismatch: expected 50, got {len(energies)}")
            
    except Exception as e:
        print(f"❌ Error during diagnostic: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diag()
