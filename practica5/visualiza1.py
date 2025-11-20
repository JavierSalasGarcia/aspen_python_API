#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 5: Visualización de Reactor CSTR (ASPEN HYSYS)
========================================================

Visualiza los resultados del reactor CSTR con conversión fija desde ASPEN HYSYS.

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
    """Genera visualización de reactor CSTR desde ASPEN"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 5 - REACTOR CSTR (ASPEN)")
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
    entrada = data['entrada']
    salida = data['salida']
    reactor = data.get('reactor', {})
    conversion = reactor.get('conversion', 0.75)

    # Crear figura
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

    fig.suptitle('Práctica 5: Reactor CSTR con Conversión Fija (ASPEN HYSYS)',
                 fontsize=16, fontweight='bold')

    # ========== Subplot 1: Diagrama del Reactor CSTR ==========
    ax1 = fig.add_subplot(gs[0, :])
    ax1.axis('off')
    ax1.set_title('Diagrama de Proceso - Reactor CSTR', fontsize=13, fontweight='bold', pad=15)

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

    # Flecha entrada al reactor
    arrow_in = FancyArrowPatch((0.25, 0.725), (0.38, 0.725),
                              arrowstyle='->', mutation_scale=30,
                              color='blue', linewidth=3)
    ax1.add_patch(arrow_in)

    # Reactor CSTR (cilindro con agitador)
    # Cilindro
    reactor_rect = FancyBboxPatch((0.38, 0.25), 0.24, 0.70,
                                  boxstyle="round,pad=0.03",
                                  edgecolor='darkred', facecolor='lightyellow',
                                  linewidth=3.5)
    ax1.add_patch(reactor_rect)

    # Agitador
    agitator = Circle((0.50, 0.60), 0.06, edgecolor='black',
                     facecolor='lightgray', linewidth=2)
    ax1.add_patch(agitator)
    ax1.plot([0.50, 0.50], [0.66, 0.85], 'k-', linewidth=3)
    ax1.plot([0.50], [0.87], 'ko', markersize=8)

    # Aspas del agitador
    ax1.plot([0.44, 0.56], [0.60, 0.60], 'k-', linewidth=2.5)
    ax1.plot([0.50, 0.50], [0.54, 0.66], 'k-', linewidth=2.5)

    # Texto del reactor
    reactor_text = f"REACTOR CSTR\n\n"
    reactor_text += f"V = {reactor.get('volumen_m3', 5.0):.1f} m³\n"
    reactor_text += f"T = {reactor.get('T_C', 80.0):.1f}°C\n"
    reactor_text += f"X = {conversion*100:.1f}%"

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

    # Reacción química
    reaction_text = reactor.get('reaccion', 'A → B')
    ax1.text(0.50, 0.15, f'Reacción: {reaction_text}',
             ha='center', fontsize=11, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

    # ========== Subplot 2: Composiciones Entrada vs Salida ==========
    ax2 = fig.add_subplot(gs[1, 0])

    # Obtener componentes
    componentes = list(entrada.get('composicion', {'A': 0.8, 'B': 0.2}).keys())
    x_entrada = [entrada.get('composicion', {}).get(c, 0) for c in componentes]
    x_salida = [salida.get('composicion', {}).get(c, 0) for c in componentes]

    x_pos = np.arange(len(componentes))
    width = 0.35

    bars1 = ax2.bar(x_pos - width/2, x_entrada, width, label='Entrada',
                    color='#3498db', alpha=0.8, edgecolor='black')
    bars2 = ax2.bar(x_pos + width/2, x_salida, width, label='Salida',
                    color='#2ecc71', alpha=0.8, edgecolor='black')

    ax2.set_ylabel('Fracción Molar', fontweight='bold', fontsize=11)
    ax2.set_title('Composición: Entrada vs Salida', fontsize=12, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(componentes, fontsize=11)
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores sobre barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=9)

    # ========== Subplot 3: Conversión del Reactivo ==========
    ax3 = fig.add_subplot(gs[1, 1])

    # Gauge de conversión
    theta = np.linspace(0, np.pi, 100)
    r = 1
    x_arc = r * np.cos(theta)
    y_arc = r * np.sin(theta)

    ax3.plot(x_arc, y_arc, 'k-', linewidth=3)
    ax3.fill_between(x_arc, 0, y_arc, alpha=0.1, color='gray')

    # Nivel de conversión
    conversion_angle = np.pi * (1 - conversion)
    ax3.plot([0, r*np.cos(conversion_angle)], [0, r*np.sin(conversion_angle)],
             'r-', linewidth=4, label=f'X = {conversion*100:.1f}%')

    # Zonas de color
    theta_low = np.linspace(0, np.pi*0.5, 50)
    theta_med = np.linspace(np.pi*0.5, np.pi*0.8, 50)
    theta_high = np.linspace(np.pi*0.8, np.pi, 50)

    ax3.fill_between(r*np.cos(theta_low), 0, r*np.sin(theta_low),
                     alpha=0.3, color='red', label='Baja (<50%)')
    ax3.fill_between(r*np.cos(theta_med), 0, r*np.sin(theta_med),
                     alpha=0.3, color='yellow', label='Media (50-80%)')
    ax3.fill_between(r*np.cos(theta_high), 0, r*np.sin(theta_high),
                     alpha=0.3, color='green', label='Alta (>80%)')

    ax3.text(0, -0.3, f'{conversion*100:.1f}%', ha='center', va='top',
             fontsize=24, fontweight='bold', color='red')

    ax3.set_xlim([-1.2, 1.2])
    ax3.set_ylim([-0.5, 1.2])
    ax3.axis('off')
    ax3.set_title('Conversión del Reactivo Limitante', fontsize=12, fontweight='bold')
    ax3.legend(loc='upper right', fontsize=8)

    # ========== Subplot 4: Flujos Molares por Componente ==========
    ax4 = fig.add_subplot(gs[1, 2])

    F_entrada_comp = [entrada['F_kgmoleh'] * x for x in x_entrada]
    F_salida_comp = [salida['F_kgmoleh'] * x for x in x_salida]

    bars1 = ax4.bar(x_pos - width/2, F_entrada_comp, width, label='Entrada',
                    color='#e74c3c', alpha=0.8, edgecolor='black')
    bars2 = ax4.bar(x_pos + width/2, F_salida_comp, width, label='Salida',
                    color='#9b59b6', alpha=0.8, edgecolor='black')

    ax4.set_ylabel('Flujo Molar (kgmole/h)', fontweight='bold', fontsize=11)
    ax4.set_title('Flujos Molares por Componente', fontsize=12, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(componentes, fontsize=11)
    ax4.legend(fontsize=10)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores sobre barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0.1:
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}', ha='center', va='bottom', fontsize=8)

    # ========== Subplot 5: Velocidad de Reacción ==========
    ax5 = fig.add_subplot(gs[2, 0])

    # Simulación de velocidad de reacción vs conversión
    X_range = np.linspace(0, 0.99, 100)
    # Para CSTR: r = k·C_A = k·C_A0·(1-X)
    # Asumiendo reacción de primer orden
    r_rel = (1 - X_range)  # Velocidad relativa

    ax5.plot(X_range * 100, r_rel, 'b-', linewidth=2.5)
    ax5.plot(conversion * 100, (1 - conversion), 'ro', markersize=12,
             label=f'Punto de operación (X={conversion*100:.1f}%)', zorder=5)

    ax5.set_xlabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax5.set_ylabel('Velocidad Relativa (r/r₀)', fontweight='bold', fontsize=11)
    ax5.set_title('Velocidad de Reacción vs Conversión', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)

    # ========== Subplot 6: Datos del Reactor ==========
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')
    ax6.set_title('Especificaciones del Reactor', fontsize=12, fontweight='bold', pad=10)

    specs_text = f"""
    REACTOR CSTR
    ═══════════════════════════════════════════

    Tipo: Tanque Agitado Continuo (CSTR)

    Dimensiones:
      • Volumen:         {reactor.get('volumen_m3', 5.0):.2f} m³
      • Diámetro:        {reactor.get('diametro_m', 1.5):.2f} m
      • Altura:          {reactor.get('altura_m', 2.0):.2f} m

    Condiciones de operación:
      • Temperatura:     {reactor.get('T_C', 80.0):.1f} °C
      • Presión:         {reactor.get('P_kPa', 101.325):.2f} kPa
      • Tiempo resid.:   {reactor.get('tau_h', 1.5):.2f} h

    Performance:
      • Conversión:      {conversion*100:.2f}%
      • Selectividad:    {reactor.get('selectividad', 0.95)*100:.1f}%

    Reacción:
      {reactor.get('reaccion', 'A → B')}
      Orden: {reactor.get('orden_reaccion', 1)}
    """

    ax6.text(0.5, 0.5, specs_text, ha='center', va='center',
             fontsize=8.5, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 7: Balance de Materia ==========
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.axis('off')
    ax7.set_title('Balance de Materia', fontsize=12, fontweight='bold', pad=10)

    # Verificar balance
    F_in = entrada['F_kgmoleh']
    F_out = salida['F_kgmoleh']

    # Componente reactivo (asumimos el primero)
    reactivo = componentes[0] if len(componentes) > 0 else 'A'
    F_reactivo_in = F_entrada_comp[0] if len(F_entrada_comp) > 0 else 0
    F_reactivo_out = F_salida_comp[0] if len(F_salida_comp) > 0 else 0
    F_reactivo_reaccionado = F_reactivo_in - F_reactivo_out

    # Conversión calculada
    X_calc = F_reactivo_reaccionado / F_reactivo_in if F_reactivo_in > 0 else 0

    balance_text = f"""
    BALANCE DE MATERIA
    ═══════════════════════════════════════════

    Balance global:
      F_entrada:       {F_in:.2f} kgmole/h
      F_salida:        {F_out:.2f} kgmole/h
      Diferencia:      {abs(F_in - F_out):.4f} kgmole/h

    Balance de {reactivo} (reactivo):
      Entrada:         {F_reactivo_in:.2f} kgmole/h
      Salida:          {F_reactivo_out:.2f} kgmole/h
      Reaccionado:     {F_reactivo_reaccionado:.2f} kgmole/h

    Conversión:
      Especificada:    {conversion*100:.2f}%
      Calculada:       {X_calc*100:.2f}%
      Error:           {abs(conversion - X_calc)*100:.3f}%

    {'✓ Balance verificado correctamente' if abs(conversion - X_calc) < 0.01 else '⚠ Revisar balance'}
    """

    color_balance = 'lightgreen' if abs(conversion - X_calc) < 0.01 else 'lightyellow'

    ax7.text(0.5, 0.5, balance_text, ha='center', va='center',
             fontsize=8.5, family='monospace',
             bbox=dict(boxstyle='round', facecolor=color_balance, alpha=0.8))

    # Nota al pie
    fig.text(0.5, 0.01,
             f'Fuente: ASPEN HYSYS | Modelo: Conversion Reactor | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()

    # Guardar
    output_file = os.path.join(script_dir, 'reactor_cstr_aspen.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    # Resumen en consola
    print("\n📊 RESUMEN:")
    print(f"   Conversión: {conversion*100:.2f}%")
    print(f"   Flujo entrada: {F_in:.2f} kgmole/h")
    print(f"   Flujo salida: {F_out:.2f} kgmole/h")
    print(f"   {reactivo} reaccionado: {F_reactivo_reaccionado:.2f} kgmole/h")

    print("="*60)

def get_reference_data():
    """Datos de referencia si no existe el archivo JSON"""
    return {
        'entrada': {
            'T_C': 25.0,
            'P_kPa': 101.325,
            'F_kgmoleh': 100.0,
            'composicion': {
                'A': 0.8,
                'B': 0.2
            }
        },
        'salida': {
            'T_C': 80.0,
            'P_kPa': 101.325,
            'F_kgmoleh': 100.0,
            'composicion': {
                'A': 0.2,
                'B': 0.8
            }
        },
        'reactor': {
            'tipo': 'CSTR',
            'volumen_m3': 5.0,
            'diametro_m': 1.5,
            'altura_m': 2.0,
            'T_C': 80.0,
            'P_kPa': 101.325,
            'tau_h': 1.5,
            'conversion': 0.75,
            'selectividad': 0.95,
            'reaccion': 'A → B',
            'orden_reaccion': 1
        }
    }

if __name__ == '__main__':
    main()
