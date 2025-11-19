#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 6: Visualización de Reactor con Cinética de Arrhenius (ASPEN HYSYS)
=============================================================================

Visualiza los resultados del reactor con cinética de Arrhenius desde ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
from datetime import datetime
import json
import os

def main():
    """Genera visualización de reactor con cinética de Arrhenius desde ASPEN"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 6 - CINÉTICA ARRHENIUS (ASPEN)")
    print("="*60)

    # Cargar datos si existen, sino usar valores de referencia
    json_file = '/home/user/aspen_python_API/practica6/resultados_aspen.json'

    if os.path.exists(json_file):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            print("   ✓ Datos cargados desde resultados_aspen.json")
        except:
            print("   ⚠ Error cargando datos, usando valores de referencia")
            data = get_reference_data()
    else:
        print("   ⚠ Usando valores de referencia (ejecutar aspython.py primero)")
        data = get_reference_data()

    # Extraer datos
    entrada = data['entrada']
    salida = data['salida']
    reactor = data.get('reactor', {})
    cinetica = data.get('cinetica', {})

    # Parámetros de Arrhenius
    A = cinetica.get('A', 1e10)  # Factor pre-exponencial
    Ea = cinetica.get('Ea_kJ_mol', 80.0)  # Energía de activación
    R = 8.314  # J/(mol·K)

    # Crear figura
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

    fig.suptitle('Práctica 6: Reactor con Cinética de Arrhenius (ASPEN HYSYS)',
                 fontsize=16, fontweight='bold')

    # ========== Subplot 1: Diagrama del Reactor ==========
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    ax1.set_title('Diagrama de Proceso - Reactor Cinético', fontsize=13, fontweight='bold', pad=15)

    # Corriente de entrada
    entrada_box = FancyBboxPatch((0.05, 0.55), 0.20, 0.35,
                                 boxstyle="round,pad=0.02",
                                 edgecolor='blue', facecolor='lightblue',
                                 linewidth=2.5)
    ax1.add_patch(entrada_box)

    entrada_text = f"ALIMENTACIÓN\n"
    entrada_text += f"T={entrada['T_C']:.1f}°C\n"
    entrada_text += f"F={entrada['F_kgmoleh']:.1f} kgmole/h\n\n"
    entrada_text += "Composición:\n"
    for comp, frac in entrada.get('composicion', {}).items():
        entrada_text += f"{comp}: {frac:.3f}\n"

    ax1.text(0.15, 0.725, entrada_text, ha='center', va='center',
             fontsize=8.5, family='monospace')

    # Flecha entrada
    arrow_in = FancyArrowPatch((0.25, 0.725), (0.38, 0.725),
                              arrowstyle='->', mutation_scale=30,
                              color='blue', linewidth=3)
    ax1.add_patch(arrow_in)

    # Reactor
    reactor_rect = FancyBboxPatch((0.38, 0.25), 0.24, 0.70,
                                  boxstyle="round,pad=0.03",
                                  edgecolor='darkred', facecolor='lightyellow',
                                  linewidth=3.5)
    ax1.add_patch(reactor_rect)

    # Símbolo de calor (llamas)
    for i, y_flame in enumerate([0.30, 0.40, 0.50]):
        flame = mpatches.Polygon([[0.35, y_flame], [0.36, y_flame+0.06], [0.37, y_flame]],
                                 closed=True, color='orange', alpha=0.7)
        ax1.add_patch(flame)

    # Agitador
    agitator = Circle((0.50, 0.60), 0.06, edgecolor='black',
                     facecolor='lightgray', linewidth=2)
    ax1.add_patch(agitator)
    ax1.plot([0.50, 0.50], [0.66, 0.85], 'k-', linewidth=3)

    # Texto del reactor
    reactor_text = f"REACTOR PFR/CSTR\n\n"
    reactor_text += f"V = {reactor.get('volumen_m3', 2.0):.1f} m³\n"
    reactor_text += f"T = {reactor.get('T_C', 120.0):.1f}°C\n"
    reactor_text += f"k = {reactor.get('k_constante', 0.85):.3f} 1/s"

    ax1.text(0.50, 0.40, reactor_text, ha='center', va='center',
             fontsize=10, fontweight='bold', color='darkred',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Flecha de salida
    arrow_out = FancyArrowPatch((0.62, 0.725), (0.72, 0.725),
                               arrowstyle='->', mutation_scale=35,
                               color='darkgreen', linewidth=3.5)
    ax1.add_patch(arrow_out)

    # Corriente de salida
    salida_box = FancyBboxPatch((0.72, 0.55), 0.23, 0.35,
                                boxstyle="round,pad=0.02",
                                edgecolor='darkgreen', facecolor='lightgreen',
                                linewidth=2.5)
    ax1.add_patch(salida_box)

    salida_text = f"PRODUCTO\n"
    salida_text += f"T={salida['T_C']:.1f}°C\n"
    salida_text += f"F={salida['F_kgmoleh']:.1f} kgmole/h\n\n"
    salida_text += "Composición:\n"
    for comp, frac in salida.get('composicion', {}).items():
        salida_text += f"{comp}: {frac:.3f}\n"

    ax1.text(0.835, 0.725, salida_text, ha='center', va='center',
             fontsize=8.5, family='monospace', fontweight='bold')

    # Ecuación de Arrhenius
    arrhenius_text = f'k = A·exp(-Ea/RT)\nA={A:.2e} 1/s, Ea={Ea:.1f} kJ/mol'
    ax1.text(0.50, 0.12, arrhenius_text,
             ha='center', fontsize=10, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

    # ========== Subplot 2: Constante de velocidad vs Temperatura ==========
    ax2 = fig.add_subplot(gs[1, 0])

    # Rango de temperaturas
    T_range_C = np.linspace(50, 200, 100)
    T_range_K = T_range_C + 273.15

    # Calcular k(T) usando Arrhenius
    k_values = A * np.exp(-Ea * 1000 / (R * T_range_K))  # Ea en J/mol

    # Temperatura de operación
    T_op = reactor.get('T_C', 120.0)
    k_op = reactor.get('k_constante', A * np.exp(-Ea * 1000 / (R * (T_op + 273.15))))

    ax2.semilogy(T_range_C, k_values, 'b-', linewidth=2.5, label='Ley de Arrhenius')
    ax2.semilogy(T_op, k_op, 'ro', markersize=12,
                label=f'Operación (T={T_op:.1f}°C)', zorder=5)

    ax2.set_xlabel('Temperatura (°C)', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Constante de velocidad k (1/s)', fontweight='bold', fontsize=11)
    ax2.set_title('Efecto de la Temperatura en k', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, which='both')

    # Anotación
    ax2.annotate(f'k = {k_op:.3f} 1/s',
                xy=(T_op, k_op), xytext=(T_op + 20, k_op * 2),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=9, color='red', fontweight='bold')

    # ========== Subplot 3: Gráfico de Arrhenius (ln k vs 1/T) ==========
    ax3 = fig.add_subplot(gs[1, 1])

    inv_T = 1000 / T_range_K  # 1000/T para mejor escala
    ln_k = np.log(k_values)

    ax3.plot(inv_T, ln_k, 'g-', linewidth=2.5, label='ln(k) vs 1/T')
    ax3.plot(1000/(T_op + 273.15), np.log(k_op), 'ro', markersize=12,
            label='Punto de operación', zorder=5)

    ax3.set_xlabel('1000/T (K⁻¹)', fontweight='bold', fontsize=11)
    ax3.set_ylabel('ln(k)', fontweight='bold', fontsize=11)
    ax3.set_title('Gráfico de Arrhenius', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    # Pendiente = -Ea/R
    ax3.text(0.05, 0.95, f'Pendiente = -Ea/R\nEa = {Ea:.1f} kJ/mol',
            transform=ax3.transAxes, fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 4: Energía de Activación ==========
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.axis('off')
    ax4.set_title('Energía de Activación', fontsize=12, fontweight='bold', pad=10)

    # Diagrama de energía
    x_coord = np.linspace(0, 1, 100)
    E_reactivos = 0
    E_productos = -30  # Exotérmica
    E_activacion = Ea

    # Curva de energía de reacción
    y_curve = E_reactivos + E_activacion * np.exp(-10*(x_coord-0.3)**2) + \
              (E_productos - E_reactivos) * (1 / (1 + np.exp(-20*(x_coord-0.5))))

    ax4_sub = fig.add_axes([0.69, 0.38, 0.25, 0.22])
    ax4_sub.plot(x_coord, y_curve, 'b-', linewidth=3)

    # Niveles de energía
    ax4_sub.axhline(y=E_reactivos, color='blue', linestyle='--', linewidth=2, alpha=0.5)
    ax4_sub.axhline(y=E_productos, color='green', linestyle='--', linewidth=2, alpha=0.5)

    ax4_sub.text(0.1, E_reactivos + 5, 'Reactivos', fontsize=10, color='blue')
    ax4_sub.text(0.75, E_productos - 5, 'Productos', fontsize=10, color='green')

    # Flecha de Ea
    ax4_sub.annotate('', xy=(0.2, E_reactivos + E_activacion * 0.95),
                    xytext=(0.2, E_reactivos),
                    arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax4_sub.text(0.25, E_reactivos + E_activacion * 0.5, f'Ea\n{Ea:.1f} kJ/mol',
                fontsize=10, color='red', fontweight='bold')

    ax4_sub.set_xlabel('Coordenada de reacción', fontweight='bold', fontsize=10)
    ax4_sub.set_ylabel('Energía (kJ/mol)', fontweight='bold', fontsize=10)
    ax4_sub.grid(True, alpha=0.3)

    # Información adicional
    ea_info = f"""
    PARÁMETROS CINÉTICOS
    ═══════════════════════════════════

    Ley de Arrhenius:
      k = A·exp(-Ea/RT)

    Factor pre-exponencial:
      A = {A:.2e} 1/s

    Energía de activación:
      Ea = {Ea:.2f} kJ/mol

    Constante universal:
      R = {R:.3f} J/(mol·K)

    A temperatura de operación:
      T = {T_op:.2f}°C ({T_op+273.15:.2f} K)
      k = {k_op:.4f} 1/s
    """

    ax4.text(0.5, 0.35, ea_info, ha='center', va='center',
             fontsize=8, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 5: Composiciones ==========
    ax5 = fig.add_subplot(gs[2, 0])

    componentes = list(entrada.get('composicion', {}).keys())
    x_entrada = [entrada.get('composicion', {}).get(c, 0) for c in componentes]
    x_salida = [salida.get('composicion', {}).get(c, 0) for c in componentes]

    x_pos = np.arange(len(componentes))
    width = 0.35

    bars1 = ax5.bar(x_pos - width/2, x_entrada, width, label='Entrada',
                    color='#3498db', alpha=0.8, edgecolor='black')
    bars2 = ax5.bar(x_pos + width/2, x_salida, width, label='Salida',
                    color='#2ecc71', alpha=0.8, edgecolor='black')

    ax5.set_ylabel('Fracción Molar', fontweight='bold', fontsize=11)
    ax5.set_title('Composición: Entrada vs Salida', fontsize=12, fontweight='bold')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(componentes, fontsize=10)
    ax5.legend(fontsize=10)
    ax5.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=9)

    # ========== Subplot 6: Conversión vs Temperatura ==========
    ax6 = fig.add_subplot(gs[2, 1])

    # Simular conversión vs temperatura
    # Para un reactor: mayor T → mayor k → mayor conversión
    T_sim = np.linspace(50, 200, 50)
    T_sim_K = T_sim + 273.15
    k_sim = A * np.exp(-Ea * 1000 / (R * T_sim_K))

    # Conversión aproximada (asumiendo CSTR con tau fijo)
    tau = reactor.get('tau_h', 1.0) * 3600  # s
    X_sim = (k_sim * tau) / (1 + k_sim * tau)  # CSTR de 1er orden

    # Conversión real
    X_real = reactor.get('conversion', 0.80)

    ax6.plot(T_sim, X_sim * 100, 'b-', linewidth=2.5, label='Modelo cinético')
    ax6.plot(T_op, X_real * 100, 'ro', markersize=12,
            label=f'Operación (X={X_real*100:.1f}%)', zorder=5)

    ax6.set_xlabel('Temperatura (°C)', fontweight='bold', fontsize=11)
    ax6.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax6.set_title('Conversión vs Temperatura', fontsize=12, fontweight='bold')
    ax6.legend(fontsize=9)
    ax6.grid(True, alpha=0.3)

    # ========== Subplot 7: Datos del Reactor ==========
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.axis('off')
    ax7.set_title('Resumen del Reactor', fontsize=12, fontweight='bold', pad=10)

    # Calcular conversión
    reactivo = componentes[0] if len(componentes) > 0 else 'A'
    x_in = x_entrada[0] if len(x_entrada) > 0 else 0
    x_out = x_salida[0] if len(x_salida) > 0 else 0
    X_calc = (x_in - x_out) / x_in if x_in > 0 else 0

    summary_text = f"""
    RESUMEN DEL REACTOR
    ═══════════════════════════════════════════

    Tipo: {reactor.get('tipo', 'PFR/CSTR')}
    Volumen: {reactor.get('volumen_m3', 2.0):.2f} m³

    CINÉTICA DE ARRHENIUS:
      k(T) = A·exp(-Ea/RT)
      A = {A:.2e} 1/s
      Ea = {Ea:.1f} kJ/mol

    CONDICIONES DE OPERACIÓN:
      T = {T_op:.1f}°C ({T_op+273.15:.1f} K)
      P = {reactor.get('P_kPa', 101.325):.2f} kPa
      τ = {reactor.get('tau_h', 1.0):.2f} h

    RESULTADOS:
      k(T_op) = {k_op:.4f} 1/s
      Conversión = {X_calc*100:.2f}%

    BALANCE:
      F_in = {entrada['F_kgmoleh']:.2f} kgmole/h
      F_out = {salida['F_kgmoleh']:.2f} kgmole/h
      {'✓ Balance OK' if abs(entrada['F_kgmoleh']-salida['F_kgmoleh'])<0.1 else '⚠ Revisar'}

    Paquete: ASPEN HYSYS
    """

    ax7.text(0.5, 0.5, summary_text, ha='center', va='center',
             fontsize=8, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    # Nota al pie
    fig.text(0.5, 0.01,
             f'Fuente: ASPEN HYSYS | Modelo: Reactor cinético (Arrhenius) | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()

    # Guardar
    output_file = '/home/user/aspen_python_API/practica6/reactor_arrhenius_aspen.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    # Resumen en consola
    print("\n📊 RESUMEN:")
    print(f"   Energía de activación: {Ea:.2f} kJ/mol")
    print(f"   Factor pre-exponencial: {A:.2e} 1/s")
    print(f"   Temperatura operación: {T_op:.1f}°C")
    print(f"   Constante k: {k_op:.4f} 1/s")
    print(f"   Conversión: {X_calc*100:.2f}%")

    print("="*60)

def get_reference_data():
    """Datos de referencia si no existe el archivo JSON"""
    return {
        'entrada': {
            'T_C': 25.0,
            'P_kPa': 101.325,
            'F_kgmoleh': 100.0,
            'composicion': {
                'A': 0.9,
                'B': 0.1
            }
        },
        'salida': {
            'T_C': 120.0,
            'P_kPa': 101.325,
            'F_kgmoleh': 100.0,
            'composicion': {
                'A': 0.18,
                'B': 0.82
            }
        },
        'reactor': {
            'tipo': 'PFR',
            'volumen_m3': 2.0,
            'diametro_m': 0.8,
            'altura_m': 4.0,
            'T_C': 120.0,
            'P_kPa': 101.325,
            'tau_h': 1.0,
            'conversion': 0.80,
            'k_constante': 0.8547
        },
        'cinetica': {
            'A': 1e10,  # 1/s
            'Ea_kJ_mol': 80.0,
            'orden': 1,
            'reaccion': 'A → B'
        }
    }

if __name__ == '__main__':
    main()
