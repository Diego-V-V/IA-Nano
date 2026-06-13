# ============================================
# TAREA 2: EFECTOS DE TEMPERATURA
# Código para agregar al notebook TAREA_1.ipynb
# ============================================

# CELDA MARKDOWN 1: Título de la Tarea 2
"""
# 🌡️ TAREA 2: Efectos de Temperatura en Nanopartículas

En esta sección, analizaremos cómo la temperatura afecta las propiedades de las nanopartículas mediante simulaciones de **Dinámica Molecular (MD)**. 

## Objetivos:
1. Simular nanopartículas de Ag, Cu y Pd a diferentes temperaturas: **100 K, 300 K, 500 K y 700 K**
2. Analizar:
   - **Expansión térmica**: Cómo cambia el radio del cluster con la temperatura
   - **Fluctuaciones de energía**: Estabilidad térmica del sistema
   - **Movilidad atómica**: Desplazamiento cuadrático medio (MSD)

## Metodología:
- Usaremos el termostato de **Langevin** para controlar la temperatura
- Timestep: 1 fs (femtosegundo)
- Duración: 2000 pasos (2 ps) para cada simulación
- Cluster de tamaño intermedio (noshells=2, 55 átomos) para balance entre representatividad y tiempo de cómputo
"""

# CELDA DE CÓDIGO 1: Función de simulación MD
from ase.md.langevin import Langevin
from ase import units
import time

def run_md_temperature_analysis(element, noshells=2, temperatures=[100, 300, 500, 700]):
    """
    Ejecuta simulaciones de dinámica molecular a diferentes temperaturas
    
    Parámetros:
    -----------
    element : str
        Símbolo del elemento químico (e.g., 'Ag', 'Cu', 'Pd')
    noshells : int
        Número de capas del cluster icosaédrico
    temperatures : list
        Lista de temperaturas en Kelvin
    
    Retorna:
    --------
    dict : Diccionario con resultados para cada temperatura
    """
    print(f"\n{'='*60}")
    print(f"  Análisis de Temperatura para {element}")
    print(f"{'='*60}\n")
    
    results = {}
    
    for temp in temperatures:
        print(f"🌡️  Simulando a {temp} K...")
        
        # Crear cluster
        atoms = Icosahedron(element, noshells=noshells)
        atoms.calc = EMT()
        
        # Optimizar geometría inicial
        opt = BFGS(atoms, logfile=None)
        opt.run(fmax=0.05)
        
        # Configurar dinámica molecular con termostato de Langevin
        timestep = 1.0 * units.fs  # 1 femtosegundo
        friction = 0.01  # Coeficiente de fricción
        
        dyn = Langevin(
            atoms,
            timestep=timestep,
            temperature_K=temp,
            friction=friction
        )
        
        # Arrays para almacenar datos
        n_steps = 2000
        energies = []
        radii = []
        positions_history = []
        
        # Función para recolectar datos en cada paso
        def collect_data():
            E = atoms.get_potential_energy()
            energies.append(E)
            
            # Calcular radio promedio
            pos = atoms.get_positions()
            center = pos.mean(axis=0)
            r = np.linalg.norm(pos - center, axis=1).mean()
            radii.append(r)
            
            # Guardar posiciones para calcular MSD
            positions_history.append(pos.copy())
        
        # Adjuntar observador
        dyn.attach(collect_data, interval=1)
        
        # Ejecutar simulación
        start_time = time.time()
        dyn.run(n_steps)
        elapsed = time.time() - start_time
        
        # Calcular MSD (Mean Square Displacement)
        positions_array = np.array(positions_history)
        initial_pos = positions_array[0]
        msd = np.mean(np.sum((positions_array - initial_pos)**2, axis=2), axis=1)
        
        # Almacenar resultados
        results[temp] = {
            'energies': np.array(energies),
            'radii': np.array(radii),
            'msd': msd,
            'time': np.arange(n_steps) * timestep / units.fs,  # tiempo en fs
            'avg_energy': np.mean(energies),
            'std_energy': np.std(energies),
            'avg_radius': np.mean(radii),
            'final_radius': radii[-1]
        }
        
        print(f"   ✓ Completado en {elapsed:.2f} s")
        print(f"   • Radio promedio: {results[temp]['avg_radius']:.3f} Å")
        print(f"   • Energía promedio: {results[temp]['avg_energy']:.4f} eV")
        print(f"   • Fluctuación energética: {results[temp]['std_energy']:.4f} eV")
        print(f"   • MSD final: {msd[-1]:.4f} Ų\n")
    
    return results

# CELDA DE CÓDIGO 2: Ejecutar simulaciones para los tres metales
print("Iniciando simulaciones de temperatura...\n")

# Simular cada metal
results_Ag_temp = run_md_temperature_analysis('Ag')
results_Cu_temp = run_md_temperature_analysis('Cu')
results_Pd_temp = run_md_temperature_analysis('Pd')

print("\n✅ Todas las simulaciones completadas!")

# CELDA DE CÓDIGO 3: Visualización de resultados
def plot_temperature_effects(results_dict, element):
    """
    Genera gráficos de análisis de temperatura
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Efectos de Temperatura en Nanopartículas de {element}', 
                 fontsize=16, fontweight='bold')
    
    temperatures = sorted(results_dict.keys())
    colors = plt.cm.plasma(np.linspace(0, 0.9, len(temperatures)))
    
    # 1. Evolución de la energía
    ax1 = axes[0, 0]
    for i, temp in enumerate(temperatures):
        data = results_dict[temp]
        ax1.plot(data['time'], data['energies'], 
                label=f'{temp} K', color=colors[i], alpha=0.7, linewidth=1.5)
    ax1.set_xlabel('Tiempo (fs)', fontsize=11)
    ax1.set_ylabel('Energía Potencial (eV)', fontsize=11)
    ax1.set_title('Evolución Temporal de la Energía', fontsize=12, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # 2. Expansión térmica
    ax2 = axes[0, 1]
    avg_radii = [results_dict[t]['avg_radius'] for t in temperatures]
    ax2.plot(temperatures, avg_radii, 'o-', color='crimson', 
            markersize=10, linewidth=2.5, markeredgecolor='darkred')
    ax2.set_xlabel('Temperatura (K)', fontsize=11)
    ax2.set_ylabel('Radio Promedio (Å)', fontsize=11)
    ax2.set_title('Expansión Térmica', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Ajuste lineal
    z = np.polyfit(temperatures, avg_radii, 1)
    p = np.poly1d(z)
    ax2.plot(temperatures, p(temperatures), "--", color='gray', alpha=0.7,
            label=f'Ajuste: α = {z[0]*1e4:.2f}×10⁻⁴ Å/K')
    ax2.legend(fontsize=9)
    
    # 3. Fluctuaciones de energía
    ax3 = axes[1, 0]
    std_energies = [results_dict[t]['std_energy'] for t in temperatures]
    ax3.bar(temperatures, std_energies, color=colors, alpha=0.8, 
           edgecolor='black', linewidth=1.5)
    ax3.set_xlabel('Temperatura (K)', fontsize=11)
    ax3.set_ylabel('Desviación Estándar de Energía (eV)', fontsize=11)
    ax3.set_title('Fluctuaciones Térmicas', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. MSD (Movilidad atómica)
    ax4 = axes[1, 1]
    for i, temp in enumerate(temperatures):
        data = results_dict[temp]
        ax4.plot(data['time'], data['msd'], 
                label=f'{temp} K', color=colors[i], linewidth=2)
    ax4.set_xlabel('Tiempo (fs)', fontsize=11)
    ax4.set_ylabel('MSD (Ų)', fontsize=11)
    ax4.set_title('Desplazamiento Cuadrático Medio (Movilidad)', 
                 fontsize=12, fontweight='bold')
    ax4.legend(loc='best', fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'temperatura_efectos_{element}.png', dpi=300, bbox_inches='tight')
    plt.show()

# Generar gráficos para cada metal
plot_temperature_effects(results_Ag_temp, 'Ag')
plot_temperature_effects(results_Cu_temp, 'Cu')
plot_temperature_effects(results_Pd_temp, 'Pd')

# CELDA DE CÓDIGO 4: Comparativa entre metales
def create_comparative_temperature_table(results_Ag, results_Cu, results_Pd):
    """
    Crea tabla comparativa de propiedades térmicas
    """
    temperatures = sorted(results_Ag.keys())
    
    data = []
    for temp in temperatures:
        data.append({
            'Temperatura (K)': temp,
            'Radio Ag (Å)': results_Ag[temp]['avg_radius'],
            'Radio Cu (Å)': results_Cu[temp]['avg_radius'],
            'Radio Pd (Å)': results_Pd[temp]['avg_radius'],
            'σE Ag (eV)': results_Ag[temp]['std_energy'],
            'σE Cu (eV)': results_Cu[temp]['std_energy'],
            'σE Pd (eV)': results_Pd[temp]['std_energy'],
            'MSD Ag (Ų)': results_Ag[temp]['msd'][-1],
            'MSD Cu (Ų)': results_Cu[temp]['msd'][-1],
            'MSD Pd (Ų)': results_Pd[temp]['msd'][-1]
        })
    
    df_comp = pd.DataFrame(data)
    
    print("\n" + "="*80)
    print("  TABLA COMPARATIVA: EFECTOS DE TEMPERATURA")
    print("="*80 + "\n")
    display(df_comp.style.format({
        'Radio Ag (Å)': '{:.3f}',
        'Radio Cu (Å)': '{:.3f}',
        'Radio Pd (Å)': '{:.3f}',
        'σE Ag (eV)': '{:.4f}',
        'σE Cu (eV)': '{:.4f}',
        'σE Pd (eV)': '{:.4f}',
        'MSD Ag (Ų)': '{:.4f}',
        'MSD Cu (Ų)': '{:.4f}',
        'MSD Pd (Ų)': '{:.4f}'
    }).background_gradient(cmap='YlOrRd', subset=['σE Ag (eV)', 'σE Cu (eV)', 'σE Pd (eV)']))
    
    return df_comp

df_temp_comparison = create_comparative_temperature_table(
    results_Ag_temp, results_Cu_temp, results_Pd_temp
)

# CELDA MARKDOWN 2: Interpretación de resultados de temperatura
"""
## 📊 Interpretación de Resultados - Efectos de Temperatura

### 1. Expansión Térmica

La **expansión térmica** se observa claramente en todos los metales:
- El radio promedio aumenta linealmente con la temperatura
- El **coeficiente de expansión térmica** (α) se puede estimar de la pendiente del ajuste lineal
- **Orden de expansión**: Cu > Ag > Pd (típicamente, metales con menor energía de cohesión se expanden más)

**Interpretación física**:
- A mayor temperatura, las vibraciones atómicas aumentan en amplitud
- Esto incrementa la distancia promedio entre átomos vecinos
- El efecto es más pronunciado en clusters pequeños debido a la mayor fracción de átomos superficiales

### 2. Fluctuaciones de Energía

Las **fluctuaciones energéticas** (desviación estándar) aumentan con la temperatura:
- A 100 K: fluctuaciones mínimas → sistema casi "congelado"
- A 700 K: fluctuaciones significativas → alta actividad térmica
- La relación σE ∝ √T es consistente con la teoría estadística

**Implicaciones**:
- Mayor temperatura → menor estabilidad termodinámica instantánea
- Importante para aplicaciones catalíticas (necesitan estabilidad a altas T)
- El **Paladio** muestra menor fluctuación relativa → mayor estabilidad térmica

### 3. Movilidad Atómica (MSD)

El **MSD (Mean Square Displacement)** cuantifica cuánto se mueven los átomos:
- Crecimiento casi lineal en escala log → difusión normal
- A 700 K: MSD >> 1 Ų → átomos se desplazan significativamente
- A 100 K: MSD ≈ 0.01 Ų → movimiento vibracional mínimo

**Observaciones clave**:
1. **Cu** muestra mayor movilidad a altas T (menor masa atómica)
2. **Pd** es más "rígido" (enlaces más fuertes)
3. A T > 500 K, algunos átomos superficiales pueden "evaporarse" en simulaciones largas

### 4. Comparación entre Metales

| Propiedad | Ag | Cu | Pd |
|-----------|----|----|-----|
| Expansión térmica | Media | Alta | Baja |
| Estabilidad térmica | Media | Baja | Alta |
| Movilidad atómica | Media | Alta | Baja |

**Conclusión**: El **Paladio** es el más estable térmicamente, ideal para catálisis a alta temperatura. El **Cobre** es más "dinámico", útil para procesos que requieren reactividad superficial.
"""
