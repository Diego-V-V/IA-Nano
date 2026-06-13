"""
╔══════════════════════════════════════════════════════════════════════╗
║   🚀 GPU vs CPU Benchmark — Simulación de Nanomateriales con IA   ║
║   Antigravity Nano Research Multiagentic Core                      ║
╚══════════════════════════════════════════════════════════════════════╝

Este script entrena una red neuronal profunda para predecir propiedades
cuánticas de nanopartículas (energía de cohesión, band gap, estabilidad)
y compara el rendimiento CPU vs GPU en tiempo real.
"""

import time
import sys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# 🎨 Configuración visual premium
# ═══════════════════════════════════════════════════════════════
plt.rcParams.update({
    'figure.facecolor': '#0a0a1a',
    'axes.facecolor': '#0d1117',
    'axes.edgecolor': '#30363d',
    'axes.labelcolor': '#c9d1d9',
    'text.color': '#c9d1d9',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'grid.color': '#21262d',
    'font.family': 'sans-serif',
    'font.size': 10,
})

CYAN = '#58a6ff'
MAGENTA = '#f778ba'
GREEN = '#3fb950'
ORANGE = '#d29922'
PURPLE = '#bc8cff'
RED = '#f85149'

# ═══════════════════════════════════════════════════════════════
# 🧬 Generador de datos de nanopartículas sintéticas
# ═══════════════════════════════════════════════════════════════
def generate_nanoparticle_dataset(n_samples=100_000, n_features=128):
    """
    Genera un dataset sintético de nanopartículas con propiedades
    que simulan descriptores atómicos complejos:
    - Funciones de distribución radial (RDF)
    - Descriptores de simetría angular (ACSFs)
    - Propiedades electrónicas (DOS parciales)
    """
    print("🧬 Generando dataset de nanopartículas...")
    print(f"   • {n_samples:,} muestras × {n_features} descriptores atómicos")

    X = np.random.randn(n_samples, n_features).astype(np.float32)

    # Simular correlaciones físicas realistas
    correlation_matrix = np.random.randn(n_features, n_features) * 0.3
    correlation_matrix = correlation_matrix @ correlation_matrix.T / n_features
    np.fill_diagonal(correlation_matrix, 1.0)
    L = np.linalg.cholesky(correlation_matrix)
    X = X @ L.T

    # Targets: propiedades cuánticas (3 propiedades a predecir)
    # 1. Energía de cohesión (eV/átomo) — relación no lineal
    e_cohesion = np.sin(X[:, :10].sum(axis=1)) * 2 + X[:, 10:20].sum(axis=1)**2 * 0.1
    # 2. Band gap (eV) — siempre positivo
    band_gap = np.abs(np.tanh(X[:, 20:40].sum(axis=1)) * 3 + X[:, 40:50].mean(axis=1))
    # 3. Estabilidad térmica (K) — escala logarítmica
    stability = 300 + np.exp(np.clip(X[:, 50:70].mean(axis=1) * 2, -3, 3)) * 100

    y = np.stack([e_cohesion, band_gap, stability], axis=1).astype(np.float32)

    # Normalizar
    X = (X - X.mean(0)) / (X.std(0) + 1e-8)
    y = (y - y.mean(0)) / (y.std(0) + 1e-8)

    print(f"   ✓ Dataset generado ({X.nbytes / 1e6:.1f} MB)")
    return torch.tensor(X), torch.tensor(y)


# ═══════════════════════════════════════════════════════════════
# 🧠 Red Neuronal Profunda para Propiedades de Nanomateriales
# ═══════════════════════════════════════════════════════════════
class NanoPropertyPredictor(nn.Module):
    """
    Red neuronal profunda con atención y conexiones residuales
    para predecir propiedades cuánticas de nanopartículas.
    ~2.5 millones de parámetros (pesado para CPU, rápido en GPU)
    """
    def __init__(self, input_dim=128, hidden_dim=512, output_dim=3):
        super().__init__()

        self.input_proj = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.1),
        )

        # Bloques residuales profundos
        self.res_blocks = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim * 2),
                nn.LayerNorm(hidden_dim * 2),
                nn.GELU(),
                nn.Dropout(0.1),
                nn.Linear(hidden_dim * 2, hidden_dim),
                nn.LayerNorm(hidden_dim),
            ) for _ in range(8)  # 8 bloques residuales
        ])

        # Mecanismo de atención simple
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 4),
            nn.Tanh(),
            nn.Linear(hidden_dim // 4, 1),
            nn.Sigmoid(),
        )

        # Cabezas de predicción (una por propiedad)
        self.head_cohesion = nn.Sequential(
            nn.Linear(hidden_dim, 128), nn.GELU(), nn.Linear(128, 1)
        )
        self.head_bandgap = nn.Sequential(
            nn.Linear(hidden_dim, 128), nn.GELU(), nn.Linear(128, 1)
        )
        self.head_stability = nn.Sequential(
            nn.Linear(hidden_dim, 128), nn.GELU(), nn.Linear(128, 1)
        )

    def forward(self, x):
        h = self.input_proj(x)

        for block in self.res_blocks:
            residual = h
            h = block(h) + residual  # Conexión residual
            h = torch.relu(h)

        # Atención
        attn_weights = self.attention(h)
        h = h * attn_weights

        # Predicciones multi-tarea
        e_coh = self.head_cohesion(h)
        bg = self.head_bandgap(h)
        stab = self.head_stability(h)

        return torch.cat([e_coh, bg, stab], dim=1)


# ═══════════════════════════════════════════════════════════════
# ⚡ Motor de Benchmark
# ═══════════════════════════════════════════════════════════════
def train_benchmark(device_name, X, y, n_epochs=20, batch_size=2048):
    """Entrena el modelo en el dispositivo especificado y mide rendimiento."""
    device = torch.device(device_name)

    model = NanoPropertyPredictor().to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=n_epochs)
    criterion = nn.HuberLoss()

    n_params = sum(p.numel() for p in model.parameters())
    X_dev, y_dev = X.to(device), y.to(device)

    # Warmup (excluido del benchmark)
    model.train()
    idx = torch.randperm(len(X_dev))[:batch_size]
    _ = model(X_dev[idx])
    if device_name == 'cuda':
        torch.cuda.synchronize()

    losses = []
    epoch_times = []
    samples_per_sec = []

    print(f"\n{'='*60}")
    device_label = "🖥️  CPU" if device_name == 'cpu' else "🎮 GPU CUDA"
    print(f" {device_label} — {n_params:,} parámetros")
    print(f"{'='*60}")

    total_start = time.perf_counter()

    for epoch in range(n_epochs):
        epoch_start = time.perf_counter()
        epoch_loss = 0.0
        n_batches = 0

        # Mezclar datos
        perm = torch.randperm(len(X_dev), device=device)
        X_shuffled = X_dev[perm]
        y_shuffled = y_dev[perm]

        for i in range(0, len(X_dev), batch_size):
            xb = X_shuffled[i:i+batch_size]
            yb = y_shuffled[i:i+batch_size]

            optimizer.zero_grad()
            pred = model(xb)
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            n_batches += 1

        scheduler.step()

        if device_name == 'cuda':
            torch.cuda.synchronize()

        epoch_time = time.perf_counter() - epoch_start
        avg_loss = epoch_loss / n_batches
        sps = len(X_dev) / epoch_time

        losses.append(avg_loss)
        epoch_times.append(epoch_time)
        samples_per_sec.append(sps)

        bar_len = int(30 * (epoch + 1) / n_epochs)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"  Época {epoch+1:2d}/{n_epochs} [{bar}] "
              f"Loss: {avg_loss:.4f} | {epoch_time:.2f}s | "
              f"{sps:,.0f} muestras/s")

    total_time = time.perf_counter() - total_start
    print(f"\n  ⏱️  Tiempo total: {total_time:.2f}s")
    print(f"  📊 Promedio: {np.mean(samples_per_sec):,.0f} muestras/s")

    return {
        'losses': losses,
        'epoch_times': epoch_times,
        'samples_per_sec': samples_per_sec,
        'total_time': total_time,
        'device': device_name,
    }


# ═══════════════════════════════════════════════════════════════
# 📊 Visualización de Resultados
# ═══════════════════════════════════════════════════════════════
def create_dashboard(cpu_results, gpu_results):
    """Crea un dashboard visual comparativo CPU vs GPU."""

    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('⚡ BENCHMARK: GPU vs CPU — Predicción de Nanomateriales con IA',
                 fontsize=18, fontweight='bold', color='white', y=0.98)

    gs = gridspec.GridSpec(2, 3, hspace=0.35, wspace=0.3,
                           left=0.07, right=0.95, top=0.91, bottom=0.08)

    epochs = range(1, len(cpu_results['losses']) + 1)

    # ── Panel 1: Pérdida durante entrenamiento ──
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(epochs, cpu_results['losses'], color=CYAN, linewidth=2.5,
             label='CPU', marker='o', markersize=4, alpha=0.9)
    ax1.plot(epochs, gpu_results['losses'], color=MAGENTA, linewidth=2.5,
             label='GPU CUDA', marker='s', markersize=4, alpha=0.9)
    ax1.fill_between(epochs, cpu_results['losses'], alpha=0.1, color=CYAN)
    ax1.fill_between(epochs, gpu_results['losses'], alpha=0.1, color=MAGENTA)
    ax1.set_xlabel('Época')
    ax1.set_ylabel('Huber Loss')
    ax1.set_title('📉 Convergencia del Modelo', fontsize=12, fontweight='bold')
    ax1.legend(framealpha=0.3, edgecolor='#30363d')
    ax1.grid(True, alpha=0.3)

    # ── Panel 2: Tiempo por época ──
    ax2 = fig.add_subplot(gs[0, 1])
    x = np.arange(len(epochs))
    w = 0.35
    bars_cpu = ax2.bar(x - w/2, cpu_results['epoch_times'], w, color=CYAN,
                        alpha=0.85, label='CPU', edgecolor='#1a4a7a')
    bars_gpu = ax2.bar(x + w/2, gpu_results['epoch_times'], w, color=MAGENTA,
                        alpha=0.85, label='GPU CUDA', edgecolor='#7a1a4a')
    ax2.set_xlabel('Época')
    ax2.set_ylabel('Tiempo (segundos)')
    ax2.set_title('⏱️ Tiempo por Época', fontsize=12, fontweight='bold')
    ax2.legend(framealpha=0.3, edgecolor='#30363d')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_xticks(x[::2])
    ax2.set_xticklabels([str(i) for i in epochs][::2])

    # ── Panel 3: Throughput (muestras/segundo) ──
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(epochs, [s/1000 for s in cpu_results['samples_per_sec']],
             color=CYAN, linewidth=2.5, label='CPU', marker='D', markersize=5)
    ax3.plot(epochs, [s/1000 for s in gpu_results['samples_per_sec']],
             color=MAGENTA, linewidth=2.5, label='GPU CUDA', marker='D', markersize=5)
    ax3.fill_between(epochs, [s/1000 for s in gpu_results['samples_per_sec']],
                     alpha=0.15, color=MAGENTA)
    ax3.set_xlabel('Época')
    ax3.set_ylabel('Miles de muestras/segundo')
    ax3.set_title('🚀 Throughput de Procesamiento', fontsize=12, fontweight='bold')
    ax3.legend(framealpha=0.3, edgecolor='#30363d')
    ax3.grid(True, alpha=0.3)

    # ── Panel 4: Speedup GPU vs CPU ──
    ax4 = fig.add_subplot(gs[1, 0])
    speedups = [c/g for c, g in zip(cpu_results['epoch_times'],
                                     gpu_results['epoch_times'])]
    colors = [GREEN if s > 1 else RED for s in speedups]
    bars = ax4.bar(epochs, speedups, color=colors, alpha=0.85,
                    edgecolor=['#1a5a1a' if s > 1 else '#5a1a1a' for s in speedups])
    ax4.axhline(y=1.0, color=ORANGE, linestyle='--', linewidth=1.5, alpha=0.7,
                label='Línea base (1x)')
    ax4.set_xlabel('Época')
    ax4.set_ylabel('Speedup (×)')
    ax4.set_title('🏎️ Aceleración GPU sobre CPU', fontsize=12, fontweight='bold')
    avg_speedup = np.mean(speedups)
    ax4.text(0.95, 0.95, f'Promedio: {avg_speedup:.1f}×',
             transform=ax4.transAxes, ha='right', va='top',
             fontsize=14, fontweight='bold', color=GREEN,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#0d1117',
                       edgecolor=GREEN, alpha=0.9))
    ax4.legend(framealpha=0.3, edgecolor='#30363d')
    ax4.grid(True, alpha=0.3, axis='y')

    # ── Panel 5: Resumen comparativo (tarjeta) ──
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.axis('off')

    total_speedup = cpu_results['total_time'] / gpu_results['total_time']

    summary_text = (
        f"{'─'*40}\n"
        f"  RESUMEN DE RENDIMIENTO\n"
        f"{'─'*40}\n\n"
        f"  🖥️  CPU Total:     {cpu_results['total_time']:.1f}s\n"
        f"  🎮 GPU Total:     {gpu_results['total_time']:.1f}s\n\n"
        f"  ⚡ Speedup:       {total_speedup:.1f}×\n"
        f"  ⏳ Ahorro:        {cpu_results['total_time'] - gpu_results['total_time']:.1f}s\n\n"
        f"  📊 CPU promedio:  {np.mean(cpu_results['samples_per_sec']):,.0f} m/s\n"
        f"  📊 GPU promedio:  {np.mean(gpu_results['samples_per_sec']):,.0f} m/s\n"
        f"{'─'*40}"
    )
    ax5.text(0.5, 0.5, summary_text, transform=ax5.transAxes,
             fontsize=11, fontfamily='monospace', color='white',
             ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#161b22',
                       edgecolor=PURPLE, linewidth=2, alpha=0.95))

    # ── Panel 6: Uso de memoria GPU ──
    ax6 = fig.add_subplot(gs[1, 2])
    if torch.cuda.is_available():
        allocated = torch.cuda.max_memory_allocated() / 1e9
        reserved = torch.cuda.max_memory_reserved() / 1e9
        total_mem = torch.cuda.get_device_properties(0).total_mem / 1e9

        categories = ['Asignada', 'Reservada', 'Total GPU']
        values = [allocated, reserved, total_mem]
        bar_colors = [MAGENTA, PURPLE, '#30363d']

        bars = ax6.barh(categories, values, color=bar_colors, alpha=0.85,
                         edgecolor='#1a1a2e', height=0.5)
        for bar, val in zip(bars, values):
            ax6.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                     f'{val:.2f} GB', va='center', fontsize=11,
                     fontweight='bold', color='white')
        ax6.set_xlabel('Memoria (GB)')
        ax6.set_title('💾 Uso de Memoria GPU', fontsize=12, fontweight='bold')
        ax6.set_xlim(0, total_mem * 1.3)
        gpu_name = torch.cuda.get_device_name(0)
        ax6.text(0.5, -0.15, f'🎮 {gpu_name}', transform=ax6.transAxes,
                 ha='center', fontsize=10, color=ORANGE, style='italic')
    else:
        ax6.text(0.5, 0.5, 'GPU no disponible', transform=ax6.transAxes,
                 ha='center', va='center', fontsize=14, color=RED)

    ax6.grid(True, alpha=0.3, axis='x')

    # Guardar
    output_path = 'gpu_benchmark_results.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='#0a0a1a', edgecolor='none')
    print(f"\n📊 Dashboard guardado en: {output_path}")
    plt.show()


# ═══════════════════════════════════════════════════════════════
# 🎬 MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   🚀 GPU vs CPU Benchmark — Nanomateriales con IA          ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Información del sistema
    print(f"\n🐍 Python {sys.version.split()[0]}")
    print(f"🔥 PyTorch {torch.__version__}")

    if torch.cuda.is_available():
        gpu = torch.cuda.get_device_name(0)
        mem = torch.cuda.get_device_properties(0).total_mem / 1e9
        print(f"🎮 GPU: {gpu} ({mem:.1f} GB)")
        print(f"🔧 CUDA: {torch.version.cuda}")
    else:
        print("⚠️  GPU CUDA no detectada — solo se ejecutará en CPU")
        print("   Para habilitar GPU, instala PyTorch con soporte CUDA:")
        print("   pip install torch --index-url https://download.pytorch.org/whl/cu121")

    # Generar dataset
    X, y = generate_nanoparticle_dataset(n_samples=100_000, n_features=128)

    n_epochs = 15

    # Benchmark CPU
    print("\n" + "▓"*60)
    print(" FASE 1: Entrenamiento en CPU")
    print("▓"*60)
    cpu_results = train_benchmark('cpu', X, y, n_epochs=n_epochs, batch_size=2048)

    # Benchmark GPU
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

        print("\n" + "▓"*60)
        print(" FASE 2: Entrenamiento en GPU CUDA")
        print("▓"*60)
        gpu_results = train_benchmark('cuda', X, y, n_epochs=n_epochs, batch_size=2048)

        # Dashboard
        print("\n" + "▓"*60)
        print(" FASE 3: Generando Dashboard Comparativo")
        print("▓"*60)
        create_dashboard(cpu_results, gpu_results)

        speedup = cpu_results['total_time'] / gpu_results['total_time']
        print(f"\n{'='*60}")
        print(f"  🏆 RESULTADO: Tu GPU es {speedup:.1f}× más rápida que tu CPU")
        print(f"     para entrenar redes neuronales de nanomateriales!")
        print(f"{'='*60}\n")
    else:
        print("\n⚠️  Sin GPU disponible, no se puede hacer la comparación.")


if __name__ == '__main__':
    main()
