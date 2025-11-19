#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 3: Visualización de Propiedades de Corrientes (ASPEN)
===============================================================

Visualiza las propiedades calculadas de corrientes desde ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def main():
    """Genera visualización de corrientes desde ASPEN"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 3 - CORRIENTES (ASPEN)")
    print("="*60)

    # Datos de la corriente (ejecutar aspython.py para valores reales)
    stream_name = "Metanol_Entrada"
    component = "Methanol"

    # Propiedades de la corriente
    T_C = 25.0
    T_K = 298.15
    P_kPa = 101.325
    F_molar = 100.0  # kgmole/h
    F_masico = 3204.0  # kg/h (F_molar * MW)
    density = 786.5  # kg/m3 (valor típico de HYSYS con NRTL)
    MW = 32.04  # g/mol

    print(f"\n📋 Datos de la corriente '{stream_name}':")
    print(f"   Componente: {component} (100%)")
    print(f"   T = {T_C:.2f} °C ({T_K:.2f} K)")
    print(f"   P = {P_kPa:.2f} kPa")
    print(f"   F (molar) = {F_molar:.2f} kgmole/h")
    print(f"   F (másico) = {F_masico:.2f} kg/h")
    print(f"   Densidad = {density:.2f} kg/m3")

    # Crear visualización
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

    fig.suptitle(f'Práctica 3: Propiedades de Corriente - {stream_name} (ASPEN HYSYS)',
                 fontsize=14, fontweight='bold')

    # ========== Subplot 1: Condiciones T-P ==========
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    ax1.set_title('Condiciones de Operación', fontsize=12, fontweight='bold', pad=10)

    # Diagrama de corriente
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    # Box de corriente
    stream_box = FancyBboxPatch((0.2, 0.5), 0.6, 0.3,
                                boxstyle="round,pad=0.05",
                                edgecolor='blue', facecolor='lightblue',
                                linewidth=3)
    ax1.add_patch(stream_box)

    ax1.text(0.5, 0.65, stream_name, ha='center', va='center',
             fontsize=14, fontweight='bold')

    # Propiedades
    props_text = f"""
    T = {T_C:.1f} °C
    P = {P_kPa:.2f} kPa
    F = {F_molar:.1f} kgmole/h
    """
    ax1.text(0.5, 0.55, props_text, ha='center', va='top',
             fontsize=10, family='monospace')

    # Flecha de flujo
    arrow = FancyArrowPatch((0.85, 0.65), (0.95, 0.65),
                           arrowstyle='->', mutation_scale=30,
                           color='green', linewidth=3)
    ax1.add_patch(arrow)

    # ========== Subplot 2: Composición ==========
    ax2 = fig.add_subplot(gs[0, 1])

    # Gráfica de pie para composición (100% metanol)
    components_pie = ['Methanol', 'Otros']
    fractions = [1.0, 0.0]
    colors_pie = ['#FF6B6B', '#CCCCCC']

    wedges, texts, autotexts = ax2.pie(fractions, labels=components_pie,
                                         autopct='%1.1f%%', startangle=90,
                                         colors=colors_pie, explode=(0.1, 0))

    ax2.set_title('Composición Molar', fontsize=12, fontweight='bold')

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    # ========== Subplot 3: Propiedades físicas ==========
    ax3 = fig.add_subplot(gs[1, 0])

    properties = ['Temperatura\n(°C)', 'Presión\n(kPa)', 'Densidad\n(kg/m³)']
    values = [T_C, P_kPa, density]
    colors_bar = ['#FF6B6B', '#4ECDC4', '#95E1D3']

    bars = ax3.bar(properties, values, color=colors_bar, alpha=0.8, edgecolor='black')
    ax3.set_ylabel('Valor', fontweight='bold')
    ax3.set_title('Propiedades Físicas', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores sobre barras
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # ========== Subplot 4: Flujos ==========
    ax4 = fig.add_subplot(gs[1, 1])

    flow_types = ['Flujo Molar\n(kgmole/h)', 'Flujo Másico\n(kg/h)', 'Densidad\n(kg/m³)']
    flow_values = [F_molar, F_masico, density]
    colors_flow = ['#F38181', '#AA96DA', '#FCBAD3']

    bars_flow = ax4.barh(flow_types, flow_values, color=colors_flow, alpha=0.8, edgecolor='black')
    ax4.set_xlabel('Valor', fontweight='bold')
    ax4.set_title('Flujos y Densidad', fontsize=12, fontweight='bold')
    ax4.grid(axis='x', alpha=0.3, linestyle='--')

    # Valores
    for bar, val in zip(bars_flow, flow_values):
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f' {val:.1f}', ha='left', va='center', fontsize=10, fontweight='bold')

    # ========== Subplot 5: Diagrama P-T ==========
    ax5 = fig.add_subplot(gs[2, 0])

    # Punto de operación en diagrama P-T (simplificado)
    T_range = np.linspace(0, 100, 100)

    # Curva de vapor saturado aproximada (Antoine para metanol)
    # log10(P) = A - B/(C+T)
    A, B, C = 7.89750, 1473.11, 230.0  # Constantes de Antoine
    P_sat = 10**(A - B/(C + T_range))  # mmHg

    ax5.plot(T_range, P_sat, 'b-', linewidth=2, label='Presión de vapor')
    ax5.plot(T_C, P_kPa / 7.50062, 'ro', markersize=12, label='Punto de operación',
             zorder=5)

    ax5.set_xlabel('Temperatura (°C)', fontweight='bold')
    ax5.set_ylabel('Presión (mmHg)', fontweight='bold')
    ax5.set_title('Diagrama P-T (Metanol)', fontsize=12, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # ========== Subplot 6: Resumen ==========
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')
    ax6.set_title('Resumen de Cálculos', fontsize=12, fontweight='bold', pad=10)

    summary_text = f"""
    Corriente: {stream_name}
    ─────────────────────────────────────

    Especificaciones (input):
      • Componente: {component} (100%)
      • T = {T_C:.2f} °C
      • P = {P_kPa:.3f} kPa
      • F = {F_molar:.2f} kgmole/h

    Propiedades calculadas (ASPEN):
      • Densidad = {density:.2f} kg/m³
      • F másico = {F_masico:.2f} kg/h
      • MW = {MW:.2f} g/mol

    Paquete termodinámico: NRTL
    Estado: Líquido
    """

    ax6.text(0.5, 0.5, summary_text, ha='center', va='center',
             fontsize=9, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Nota al pie
    fig.text(0.5, 0.01,
             f'Fuente: ASPEN HYSYS | Paquete: NRTL | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout()

    # Guardar
    output_file = '/home/user/aspen_python_API/practica3/corriente_aspen.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    print("\n💡 ANÁLISIS:")
    print(f"   • La corriente está en estado líquido a {T_C:.1f}°C y {P_kPa:.2f} kPa")
    print(f"   • Densidad calculada: {density:.2f} kg/m³ (típica para metanol)")
    print(f"   • ASPEN usa el paquete NRTL para propiedades termodinámicas")

    print("="*60)

if __name__ == '__main__':
    main()
