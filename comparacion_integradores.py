import numpy as np
import matplotlib.pyplot as plt

def lennard_jones_force(r, epsilon=1.0, sigma=1.0):
    """Fuerza de Lennard-Jones: F = -dV/dr"""
    return 48 * epsilon * (sigma**12 / r**13 - 0.5 * sigma**6 / r**7)

def verlet_step(r, r_old, f, m, dt):
    """Un paso del algoritmo de Verlet"""
    r_new = 2*r - r_old + (f/m) * dt**2
    return r_new

def velocity_verlet_step(r, v, f, m, dt, force_func):
    """Un paso de Velocity Verlet"""
    # Actualizar posición
    r_new = r + v*dt + 0.5*(f/m)*dt**2
    
    # Calcular nueva fuerza
    f_new = force_func(r_new)
    
    # Actualizar velocidad
    v_new = v + 0.5*(f + f_new)/m * dt
    
    return r_new, v_new, f_new

# Simular oscilador armónico simple (dos átomos con LJ)
m = 1.0
dt = 0.001
n_steps = 5000

# Condiciones iniciales
r0 = 1.5  # Posición inicial (cerca del equilibrio en 2^(1/6) ≈ 1.12)
v0 = 0.0  # Velocidad inicial

# Arrays para almacenar resultados
time = np.arange(n_steps) * dt
r_verlet = np.zeros(n_steps)
r_vverlet = np.zeros(n_steps)
v_vverlet = np.zeros(n_steps)
energy_verlet = np.zeros(n_steps)
energy_vverlet = np.zeros(n_steps)

# Inicializar
r_verlet[0] = r0
r_verlet[1] = r0 + v0*dt  # Primer paso con Euler
r_vverlet[0] = r0
v_vverlet[0] = v0

# Función de energía potencial LJ
def lj_potential(r):
    return 4 * ((1/r)**12 - (1/r)**6)

# Simulación con Verlet
for i in range(1, n_steps-1):
    f = lennard_jones_force(r_verlet[i])
    r_verlet[i+1] = verlet_step(r_verlet[i], r_verlet[i-1], f, m, dt)
    
    # Calcular energía (aproximando velocidad)
    v_approx = (r_verlet[i+1] - r_verlet[i-1]) / (2*dt)
    energy_verlet[i] = 0.5*m*v_approx**2 + lj_potential(r_verlet[i])

# Simulación con Velocity Verlet
f = lennard_jones_force(r_vverlet[0])
for i in range(n_steps-1):
    r_vverlet[i+1], v_vverlet[i+1], f = velocity_verlet_step(
        r_vverlet[i], v_vverlet[i], f, m, dt, lennard_jones_force
    )
    energy_vverlet[i] = 0.5*m*v_vverlet[i]**2 + lj_potential(r_vverlet[i])

# Visualización
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Trayectorias
axes[0,0].plot(time, r_verlet, 'b-', label='Verlet', alpha=0.7)
axes[0,0].plot(time, r_vverlet, 'r--', label='Velocity Verlet', alpha=0.7)
axes[0,0].set_xlabel('Tiempo')
axes[0,0].set_ylabel('Posición r')
axes[0,0].set_title('Comparación de Trayectorias')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# Diferencia entre métodos
axes[0,1].plot(time, np.abs(r_verlet - r_vverlet), 'g-')
axes[0,1].set_xlabel('Tiempo')
axes[0,1].set_ylabel('|r_Verlet - r_VVerlet|')
axes[0,1].set_title('Diferencia entre Métodos')
axes[0,1].set_yscale('log')
axes[0,1].grid(True, alpha=0.3)

# Conservación de energía
axes[1,0].plot(time[1:-1], energy_verlet[1:-1], 'b-', label='Verlet')
axes[1,0].plot(time[:-1], energy_vverlet[:-1], 'r--', label='Velocity Verlet')
axes[1,0].set_xlabel('Tiempo')
axes[1,0].set_ylabel('Energía Total')
axes[1,0].set_title('Conservación de Energía')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# Deriva de energía
E0_verlet = energy_verlet[100]
E0_vverlet = energy_vverlet[100]
axes[1,1].plot(time[1:-1], (energy_verlet[1:-1] - E0_verlet)/E0_verlet, 'b-', label='Verlet')
axes[1,1].plot(time[:-1], (energy_vverlet[:-1] - E0_vverlet)/E0_vverlet, 'r--', label='Velocity Verlet')
axes[1,1].set_xlabel('Tiempo')
axes[1,1].set_ylabel('ΔE/E₀')
axes[1,1].set_title('Deriva Relativa de Energía')
axes[1,1].legend()
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comparacion_integradores.png', dpi=300)
# plt.show()

print(f"Deriva de energía final:")
print(f"  Verlet: {(energy_verlet[-100] - E0_verlet)/E0_verlet * 100:.6f}%")
print(f"  Velocity Verlet: {(energy_vverlet[-100] - E0_vverlet)/E0_vverlet * 100:.6f}%")
