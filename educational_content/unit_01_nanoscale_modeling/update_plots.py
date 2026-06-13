import json
import numpy as np

notebook_path = "TAREA_1_COMPLETA.ipynb"

# Función robusta de ploteo para reemplazar la existente
new_plot_code = [
    "def plot_temperature_effects(results_dict, element):\n",
    "    \"\"\"\n",
    "    Genera gráficos de análisis de temperatura de forma robusta.\n",
    "    \"\"\"\n",
    "    # Verificación de datos\n",
    "    if not results_dict or not isinstance(results_dict, dict):\n",
    "        print(f\"⚠️ ADVERTENCIA: No hay datos simulados para {element}. Ejecuta la celda de simulación primero.\")\n",
    "        return\n",
    "    \n",
    "    try:\n",
    "        fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n",
    "        fig.suptitle(f'Efectos de Temperatura en Nanopartículas de {element}', \n",
    "                     fontsize=16, fontweight='bold')\n",
    "        \n",
    "        temperatures = sorted(results_dict.keys())\n",
    "        if not temperatures:\n",
    "            print(f\"⚠️ ADVERTENCIA: Diccionario de resultados vacío para {element}.\")\n",
    "            return\n",
    "            \n",
    "        colors = plt.cm.plasma(np.linspace(0, 0.9, len(temperatures)))\n",
    "        \n",
    "        # 1. Evolución de la energía\n",
    "        ax1 = axes[0, 0]\n",
    "        for i, temp in enumerate(temperatures):\n",
    "            data = results_dict[temp]\n",
    "            # Verificar que existan los datos esperados\n",
    "            if 'time' not in data or 'energies' not in data:\n",
    "                continue\n",
    "            ax1.plot(data['time'], data['energies'], \n",
    "                    label=f'{temp} K', color=colors[i], alpha=0.7, linewidth=1.5)\n",
    "        ax1.set_xlabel('Tiempo (fs)', fontsize=11)\n",
    "        ax1.set_ylabel('Energía Potencial (eV)', fontsize=11)\n",
    "        ax1.set_title('Evolución Temporal de la Energía', fontsize=12, fontweight='bold')\n",
    "        ax1.legend(loc='best', fontsize=9)\n",
    "        ax1.grid(True, alpha=0.3)\n",
    "        \n",
    "        # 2. Expansión térmica\n",
    "        ax2 = axes[0, 1]\n",
    "        avg_radii = [results_dict[t]['avg_radius'] for t in temperatures]\n",
    "        ax2.plot(temperatures, avg_radii, 'o-', color='crimson', \n",
    "                markersize=10, linewidth=2.5, markeredgecolor='darkred')\n",
    "        ax2.set_xlabel('Temperatura (K)', fontsize=11)\n",
    "        ax2.set_ylabel('Radio Promedio (Å)', fontsize=11)\n",
    "        ax2.set_title('Expansión Térmica', fontsize=12, fontweight='bold')\n",
    "        ax2.grid(True, alpha=0.3)\n",
    "        \n",
    "        # Ajuste lineal\n",
    "        if len(temperatures) > 1:\n",
    "            z = np.polyfit(temperatures, avg_radii, 1)\n",
    "            p = np.poly1d(z)\n",
    "            ax2.plot(temperatures, p(temperatures), \"--\", color='gray', alpha=0.7,\n",
    "                    label=f'Ajuste: α = {z[0]*1e4:.2f}×10⁻⁴ Å/K')\n",
    "            ax2.legend(fontsize=9)\n",
    "        \n",
    "        # 3. Fluctuaciones de energía\n",
    "        ax3 = axes[1, 0]\n",
    "        std_energies = [results_dict[t]['std_energy'] for t in temperatures]\n",
    "        ax3.bar(temperatures, std_energies, color=colors, alpha=0.8, \n",
    "               edgecolor='black', linewidth=1.5)\n",
    "        ax3.set_xlabel('Temperatura (K)', fontsize=11)\n",
    "        ax3.set_ylabel('Desviación Estándar de Energía (eV)', fontsize=11)\n",
    "        ax3.set_title('Fluctuaciones Térmicas', fontsize=12, fontweight='bold')\n",
    "        ax3.grid(True, alpha=0.3, axis='y')\n",
    "        \n",
    "        # 4. MSD (Movilidad atómica)\n",
    "        ax4 = axes[1, 1]\n",
    "        for i, temp in enumerate(temperatures):\n",
    "            data = results_dict[temp]\n",
    "            # Evitar log(0) sumando un pequeño epsilon o usando symlog\n",
    "            # Aquí optamos por filtrar el primer punto si es 0 exacto para log plot\n",
    "            msd_data = data['msd']\n",
    "            time_data = data['time']\n",
    "            \n",
    "            mask = msd_data > 0\n",
    "            if np.any(mask):\n",
    "                 ax4.plot(time_data[mask], msd_data[mask], \n",
    "                        label=f'{temp} K', color=colors[i], linewidth=2)\n",
    "            else:\n",
    "                 ax4.plot(time_data, msd_data, \n",
    "                        label=f'{temp} K', color=colors[i], linewidth=2)\n",
    "\n",
    "        ax4.set_xlabel('Tiempo (fs)', fontsize=11)\n",
    "        ax4.set_ylabel('MSD (Ų)', fontsize=11)\n",
    "        ax4.set_title('Desplazamiento Cuadrático Medio (Movilidad)', \n",
    "                     fontsize=12, fontweight='bold')\n",
    "        ax4.legend(loc='best', fontsize=9)\n",
    "        ax4.grid(True, alpha=0.3)\n",
    "        # Usar symlog para manejar mejor valores cercanos a cero\n",
    "        ax4.set_yscale('symlog', linthresh=1e-3)\n",
    "        \n",
    "        plt.tight_layout()\n",
    "        plt.savefig(f'temperatura_efectos_{element}.png', dpi=300, bbox_inches='tight')\n",
    "        plt.show()\n",
    "        print(f\"✅ Gráfica generada para {element}\")\n",
    "        \n",
    "    except Exception as e:\n",
    "        print(f\"❌ Error al graficar {element}: {str(e)}\")\n",
    "\n",
    "# Intentar graficar verificando que las variables existen\n",
    "try:\n",
    "    if 'results_Ag_temp' in globals(): plot_temperature_effects(results_Ag_temp, 'Ag')\n",
    "    elif 'results_Ag_temp' not in globals(): print(\"⚠️ Variable 'results_Ag_temp' no encontrada. Ejecuta la celda de simulación primero.\")\n",
    "    \n",
    "    if 'results_Cu_temp' in globals(): plot_temperature_effects(results_Cu_temp, 'Cu')\n",
    "    if 'results_Pd_temp' in globals(): plot_temperature_effects(results_Pd_temp, 'Pd')\n",
    "except NameError:\n",
    "    print(\"⚠️ No se encontraron las variables de resultados. Asegúrate de ejecutar la celda de simulación primero.\")\n"
]

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Buscar la celda que contiene "def plot_temperature_effects" y reemplazarla
found = False
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "def plot_temperature_effects" in source:
            cell['source'] = new_plot_code
            found = True
            break

if found:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=4, ensure_ascii=False)
    print("Notebook actualizado con función de gráfica robusta.")
else:
    print("No se encontró la celda de la gráfica para actualizar.")
