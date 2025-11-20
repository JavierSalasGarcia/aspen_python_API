#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 4: Visualización de Operación Mixer (ASPEN HYSYS)
===========================================================

Visualiza los resultados del mezclador desde ASPEN HYSYS, mostrando
balances de materia y energía.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from datetime import datetime
import json
import os

def main():
    """Genera visualización de mezclador desde ASPEN"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 4 - MIXER (ASPEN)")
    print("="*60)

    # Cargar datos si existen, sino usar valores de referencia
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'resultados_aspen.json')

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
    entrada1 = data['entrada1']
    entrada2 = data['entrada2']
    salida = data['salida']

    # Crear figura
    fig = plt.figure(figsize=(16, 11))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

    fig.suptitle('Práctica 4: Operación Unitaria - Mixer (ASPEN HYSYS)',
                 fontsize=16, fontweight='bold')

    # ========== Subplot 1: Diagrama de Flujo del Mixer ==========
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    ax1.set_title('Diagrama de Flujo del Proceso', fontsize=13, fontweight='bold', pad=15)

    # Corriente 1
    stream1_box = FancyBboxPatch((0.05, 0.65), 0.18, 0.25,
                                 boxstyle="round,pad=0.02",
                                 edgecolor='blue', facecolor='lightblue',
                                 linewidth=2)
    ax1.add_patch(stream1_box)

    stream1_text = f"{entrada1.get('nombre', 'Entrada 1')}\n"
    stream1_text += f"T={entrada1['T_C']:.1f}°C\n"
    stream1_text += f"F={entrada1['F_kgmoleh']:.1f} kgmole/h\n"
    stream1_text += f"x(MeOH)={entrada1['x_Methanol']:.2f}"

    ax1.text(0.14, 0.775, stream1_text, ha='center', va='center',
             fontsize=9, family='monospace')

    # Flecha 1 al mixer
    arrow1 = FancyArrowPatch((0.23, 0.775), (0.38, 0.65),
                            arrowstyle='->', mutation_scale=25,
                            color='blue', linewidth=2.5)
    ax1.add_patch(arrow1)

    # Corriente 2
    stream2_box = FancyBboxPatch((0.05, 0.25), 0.18, 0.25,
                                 boxstyle="round,pad=0.02",
                                 edgecolor='green', facecolor='lightgreen',
                                 linewidth=2)
    ax1.add_patch(stream2_box)

    stream2_text = f"{entrada2.get('nombre', 'Entrada 2')}\n"
    stream2_text += f"T={entrada2['T_C']:.1f}°C\n"
    stream2_text += f"F={entrada2['F_kgmoleh']:.1f} kgmole/h\n"
    stream2_text += f"x(H₂O)={entrada2['x_Water']:.2f}"

    ax1.text(0.14, 0.375, stream2_text, ha='center', va='center',
             fontsize=9, family='monospace')

    # Flecha 2 al mixer
    arrow2 = FancyArrowPatch((0.23, 0.375), (0.38, 0.50),
                            arrowstyle='->', mutation_scale=25,
                            color='green', linewidth=2.5)
    ax1.add_patch(arrow2)

    # Mixer
    mixer_circle = plt.Circle((0.45, 0.575), 0.12,
                              edgecolor='red', facecolor='lightyellow',
                              linewidth=3, zorder=3)
    ax1.add_patch(mixer_circle)
    ax1.text(0.45, 0.575, 'MIXER', ha='center', va='center',
             fontsize=12, fontweight='bold', color='red')

    # Flecha de salida
    arrow_out = FancyArrowPatch((0.57, 0.575), (0.72, 0.575),
                               arrowstyle='->', mutation_scale=30,
                               color='purple', linewidth=3)
    ax1.add_patch(arrow_out)

    # Corriente de salida
    stream_out_box = FancyBboxPatch((0.72, 0.425), 0.23, 0.30,
                                    boxstyle="round,pad=0.02",
                                    edgecolor='purple', facecolor='plum',
                                    linewidth=2.5)
    ax1.add_patch(stream_out_box)

    stream_out_text = f"{salida.get('nombre', 'Salida')}\n"
    stream_out_text += f"T={salida['T_C']:.2f}°C\n"
    stream_out_text += f"F={salida['F_kgmoleh']:.1f} kgmole/h\n"
    stream_out_text += f"x(MeOH)={salida['x_Methanol']:.3f}\n"
    stream_out_text += f"x(H₂O)={salida['x_Water']:.3f}\n"
    stream_out_text += f"ρ={salida['density_kgm3']:.1f} kg/m³"

    ax1.text(0.835, 0.575, stream_out_text, ha='center', va='center',
             fontsize=9, family='monospace', fontweight='bold')

    # ========== Subplot 2: Comparación de Flujos ==========
    ax2 = fig.add_subplot(gs[1, 0])

    streams = ['Entrada 1\n(Metanol)', 'Entrada 2\n(Agua)', 'Salida\n(Mezcla)']
    flows = [entrada1['F_kgmoleh'], entrada2['F_kgmoleh'], salida['F_kgmoleh']]
    colors = ['#3498db', '#2ecc71', '#9b59b6']

    bars = ax2.bar(streams, flows, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Flujo Molar (kgmole/h)', fontweight='bold', fontsize=11)
    ax2.set_title('Balance de Materia Global', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores sobre barras
    for bar, val in zip(bars, flows):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    # Verificación de balance
    F_total_in = entrada1['F_kgmoleh'] + entrada2['F_kgmoleh']
    balance_ok = abs(F_total_in - salida['F_kgmoleh']) < 0.1
    status_text = f"F₁ + F₂ = {F_total_in:.1f} kgmole/h\n"
    status_text += f"{'✓ Balance OK' if balance_ok else '✗ Error'}"

    ax2.text(0.5, 0.95, status_text, transform=ax2.transAxes,
             ha='center', va='top', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='lightgreen' if balance_ok else 'lightcoral',
                      alpha=0.7))

    # ========== Subplot 3: Temperaturas ==========
    ax3 = fig.add_subplot(gs[1, 1])

    temps = [entrada1['T_C'], entrada2['T_C'], salida['T_C']]
    colors_temp = ['#e74c3c', '#3498db', '#f39c12']

    bars_temp = ax3.bar(streams, temps, color=colors_temp, alpha=0.8,
                        edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Temperatura (°C)', fontweight='bold', fontsize=11)
    ax3.set_title('Balance de Energía (Temperaturas)', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores sobre barras
    for bar, val in zip(bars_temp, temps):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}°C', ha='center', va='bottom',
                fontsize=9, fontweight='bold')

    # ========== Subplot 4: Composiciones ==========
    ax4 = fig.add_subplot(gs[1, 2])

    components = ['Metanol', 'Agua']
    comp_salida = [salida['x_Methanol'], salida['x_Water']]
    colors_pie = ['#FF6B6B', '#4ECDC4']

    wedges, texts, autotexts = ax4.pie(comp_salida, labels=components,
                                         autopct='%1.2f%%', startangle=90,
                                         colors=colors_pie, explode=(0.05, 0.05))

    ax4.set_title('Composición de Salida', fontsize=12, fontweight='bold')

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    # ========== Subplot 5: Balance por Componente ==========
    ax5 = fig.add_subplot(gs[2, 0])

    # Flujo de metanol
    F_MeOH_in1 = entrada1['F_kgmoleh'] * entrada1['x_Methanol']
    F_MeOH_in2 = entrada2['F_kgmoleh'] * entrada2['x_Methanol']
    F_MeOH_out = salida['F_kgmoleh'] * salida['x_Methanol']

    # Flujo de agua
    F_H2O_in1 = entrada1['F_kgmoleh'] * entrada1['x_Water']
    F_H2O_in2 = entrada2['F_kgmoleh'] * entrada2['x_Water']
    F_H2O_out = salida['F_kgmoleh'] * salida['x_Water']

    x = np.arange(2)
    width = 0.25

    entrada1_flows = [F_MeOH_in1, F_H2O_in1]
    entrada2_flows = [F_MeOH_in2, F_H2O_in2]
    salida_flows = [F_MeOH_out, F_H2O_out]

    bars1 = ax5.bar(x - width, entrada1_flows, width, label='Entrada 1',
                    color='#3498db', alpha=0.8, edgecolor='black')
    bars2 = ax5.bar(x, entrada2_flows, width, label='Entrada 2',
                    color='#2ecc71', alpha=0.8, edgecolor='black')
    bars3 = ax5.bar(x + width, salida_flows, width, label='Salida',
                    color='#9b59b6', alpha=0.8, edgecolor='black')

    ax5.set_ylabel('Flujo Molar (kgmole/h)', fontweight='bold', fontsize=11)
    ax5.set_title('Balance por Componente', fontsize=12, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(components)
    ax5.legend(fontsize=9)
    ax5.grid(axis='y', alpha=0.3, linestyle='--')

    # ========== Subplot 6: Propiedades de Salida ==========
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')
    ax6.set_title('Propiedades de la Mezcla', fontsize=12, fontweight='bold', pad=10)

    props_text = f"""
    CORRIENTE DE SALIDA
    ═══════════════════════════════════════════

    Condiciones:
      • Temperatura:     {salida['T_C']:.2f} °C
      • Presión:         {salida['P_kPa']:.2f} kPa
      • Flujo molar:     {salida['F_kgmoleh']:.2f} kgmole/h

    Composición:
      • Metanol (x):     {salida['x_Methanol']:.4f}
      • Agua (x):        {salida['x_Water']:.4f}
      • Suma:            {salida['x_Methanol'] + salida['x_Water']:.4f} ✓

    Propiedades físicas:
      • Densidad:        {salida['density_kgm3']:.2f} kg/m³

    Paquete termodinámico: NRTL
    Estado: Líquido
    """

    ax6.text(0.5, 0.5, props_text, ha='center', va='center',
             fontsize=9, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 7: Resumen de Balances ==========
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.axis('off')
    ax7.set_title('Verificación de Balances', fontsize=12, fontweight='bold', pad=10)

    # Cálculos de verificación
    F_total_in = entrada1['F_kgmoleh'] + entrada2['F_kgmoleh']
    F_total_out = salida['F_kgmoleh']
    error_F = abs(F_total_in - F_total_out) / F_total_in * 100

    F_MeOH_total_in = F_MeOH_in1 + F_MeOH_in2
    error_MeOH = abs(F_MeOH_total_in - F_MeOH_out) / max(F_MeOH_total_in, 0.001) * 100

    F_H2O_total_in = F_H2O_in1 + F_H2O_in2
    error_H2O = abs(F_H2O_total_in - F_H2O_out) / max(F_H2O_total_in, 0.001) * 100

    balance_text = f"""
    VERIFICACIÓN DE BALANCES
    ═══════════════════════════════════════════

    Balance Global:
      Entrada:  {F_total_in:.2f} kgmole/h
      Salida:   {F_total_out:.2f} kgmole/h
      Error:    {error_F:.4f}% {'✓' if error_F < 0.1 else '✗'}

    Balance de Metanol:
      Entrada:  {F_MeOH_total_in:.2f} kgmole/h
      Salida:   {F_MeOH_out:.2f} kgmole/h
      Error:    {error_MeOH:.4f}% {'✓' if error_MeOH < 0.1 else '✗'}

    Balance de Agua:
      Entrada:  {F_H2O_total_in:.2f} kgmole/h
      Salida:   {F_H2O_out:.2f} kgmole/h
      Error:    {error_H2O:.4f}% {'✓' if error_H2O < 0.1 else '✗'}

    {'✓ Todos los balances cierran correctamente' if max(error_F, error_MeOH, error_H2O) < 0.1 else '⚠ Revisar balances'}
    """

    color_balance = 'lightgreen' if max(error_F, error_MeOH, error_H2O) < 0.1 else 'lightcoral'

    ax7.text(0.5, 0.5, balance_text, ha='center', va='center',
             fontsize=8.5, family='monospace',
             bbox=dict(boxstyle='round', facecolor=color_balance, alpha=0.8))

    # Nota al pie
    fig.text(0.5, 0.01,
             f'Fuente: ASPEN HYSYS | Paquete: NRTL | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()

    # Guardar
    output_file = os.path.join(script_dir, 'mixer_aspen.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    # Resumen en consola
    print("\n📊 RESUMEN:")
    print(f"   Balance global:  {error_F:.4f}% error")
    print(f"   Balance Metanol: {error_MeOH:.4f}% error")
    print(f"   Balance Agua:    {error_H2O:.4f}% error")
    print(f"   Temperatura salida: {salida['T_C']:.2f}°C")
    print(f"   Densidad mezcla: {salida['density_kgm3']:.2f} kg/m³")

    print("="*60)

def get_reference_data():
    """Datos de referencia si no existe el archivo JSON"""
    return {
        'entrada1': {
            'nombre': 'Entrada_Metanol',
            'T_C': 25.0,
            'P_kPa': 101.325,
            'F_kgmoleh': 50.0,
            'x_Methanol': 1.0,
            'x_Water': 0.0
        },
        'entrada2': {
            'nombre': 'Entrada_Agua',
            'T_C': 30.0,
            'P_kPa': 101.325,
            'F_kgmoleh': 30.0,
            'x_Methanol': 0.0,
            'x_Water': 1.0
        },
        'salida': {
            'nombre': 'Salida_Mezcla',
            'T_C': 26.87,
            'P_kPa': 101.325,
            'F_kgmoleh': 80.0,
            'x_Methanol': 0.625,
            'x_Water': 0.375,
            'density_kgm3': 852.3
        }
    }

if __name__ == '__main__':
    main()
