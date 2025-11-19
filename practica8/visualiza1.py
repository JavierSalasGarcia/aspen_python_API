#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 8: Visualización de Planta de Biodiesel Completa (ASPEN HYSYS)
========================================================================

Visualiza los resultados de la planta completa de producción de biodiesel
desde ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon
import numpy as np
from datetime import datetime
import json
import os

def main():
    """Genera visualización de planta de biodiesel desde ASPEN"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 8 - PLANTA BIODIESEL (ASPEN)")
    print("="*60)

    # Cargar datos si existen, sino usar valores de referencia
    json_file = '/home/user/aspen_python_API/practica8/resultados_aspen.json'

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
    corrientes = data.get('corrientes', {})
    equipos = data.get('equipos', {})
    balance = data.get('balance', {})
    economia = data.get('economia', {})

    # Crear figura
    fig = plt.figure(figsize=(18, 14))
    gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.35)

    fig.suptitle('Práctica 8: Planta Completa de Producción de Biodiesel (ASPEN HYSYS)',
                 fontsize=16, fontweight='bold')

    # ========== Subplot 1: Diagrama de Flujo de Proceso (PFD) ==========
    ax1 = fig.add_subplot(gs[0:2, :])
    ax1.axis('off')
    ax1.set_title('Diagrama de Flujo de Proceso (PFD)', fontsize=14, fontweight='bold', pad=15)

    # Escala
    x_scale = 0.95
    y_base = 0.5

    # 1. Alimentación de Aceite
    oil_box = FancyBboxPatch((0.02, y_base + 0.30), 0.10, 0.15,
                             boxstyle="round,pad=0.01",
                             edgecolor='brown', facecolor='wheat',
                             linewidth=2)
    ax1.add_patch(oil_box)
    ax1.text(0.07, y_base + 0.375, 'Aceite\nVegetal', ha='center', va='center',
             fontsize=7, fontweight='bold')

    # Flecha al mixer
    ax1.arrow(0.12, y_base + 0.375, 0.05, -0.10, head_width=0.015, head_length=0.01,
             fc='brown', ec='brown', linewidth=1.5)

    # 2. Alimentación de Metanol
    meoh_box = FancyBboxPatch((0.02, y_base - 0.05), 0.10, 0.15,
                              boxstyle="round,pad=0.01",
                              edgecolor='blue', facecolor='lightblue',
                              linewidth=2)
    ax1.add_patch(meoh_box)
    ax1.text(0.07, y_base + 0.025, 'Metanol\n+ Cat.', ha='center', va='center',
             fontsize=7, fontweight='bold')

    # Flecha al mixer
    ax1.arrow(0.12, y_base + 0.025, 0.05, 0.10, head_width=0.015, head_length=0.01,
             fc='blue', ec='blue', linewidth=1.5)

    # 3. Mixer
    mixer_circle = Circle((0.20, y_base + 0.15), 0.04,
                         edgecolor='purple', facecolor='lavender',
                         linewidth=2.5)
    ax1.add_patch(mixer_circle)
    ax1.text(0.20, y_base + 0.15, 'MIX', ha='center', va='center',
             fontsize=7, fontweight='bold')

    # Flecha al reactor
    ax1.arrow(0.24, y_base + 0.15, 0.06, 0, head_width=0.015, head_length=0.01,
             fc='purple', ec='purple', linewidth=2)

    # 4. Reactor de Transesterificación
    reactor_rect = FancyBboxPatch((0.30, y_base), 0.12, 0.30,
                                  boxstyle="round,pad=0.02",
                                  edgecolor='darkred', facecolor='lightyellow',
                                  linewidth=3)
    ax1.add_patch(reactor_rect)
    ax1.text(0.36, y_base + 0.15, 'REACTOR\nCSTR', ha='center', va='center',
             fontsize=8, fontweight='bold', color='darkred')

    # Conversión del reactor
    conversion = equipos.get('reactor', {}).get('conversion', 0.95)
    ax1.text(0.36, y_base + 0.05, f'X={conversion*100:.0f}%', ha='center',
             fontsize=7, style='italic')

    # Flecha al separador
    ax1.arrow(0.42, y_base + 0.15, 0.06, 0, head_width=0.015, head_length=0.01,
             fc='orange', ec='orange', linewidth=2)

    # 5. Separador (Decantador)
    sep_trap = Polygon([[0.48, y_base], [0.48, y_base + 0.30],
                       [0.58, y_base + 0.25], [0.58, y_base + 0.05]],
                       closed=True, edgecolor='green', facecolor='lightgreen',
                       linewidth=2.5)
    ax1.add_patch(sep_trap)
    ax1.text(0.53, y_base + 0.15, 'SEP', ha='center', va='center',
             fontsize=8, fontweight='bold', color='darkgreen')

    # Corriente superior (glicerol)
    ax1.arrow(0.53, y_base + 0.28, 0, 0.10, head_width=0.015, head_length=0.01,
             fc='brown', ec='brown', linewidth=2)
    glic_box = FancyBboxPatch((0.49, y_base + 0.40), 0.08, 0.08,
                              boxstyle="round,pad=0.01",
                              edgecolor='brown', facecolor='tan',
                              linewidth=2)
    ax1.add_patch(glic_box)
    ax1.text(0.53, y_base + 0.44, 'Glicerol\ncrudo', ha='center', va='center',
             fontsize=6, fontweight='bold')

    # Corriente inferior (biodiesel crudo)
    ax1.arrow(0.58, y_base + 0.08, 0.06, 0, head_width=0.015, head_length=0.01,
             fc='green', ec='green', linewidth=2)

    # 6. Lavado
    wash_rect = Rectangle((0.64, y_base + 0.02), 0.08, 0.12,
                          edgecolor='cyan', facecolor='lightcyan',
                          linewidth=2)
    ax1.add_patch(wash_rect)
    ax1.text(0.68, y_base + 0.08, 'Lavado', ha='center', va='center',
             fontsize=7, fontweight='bold')

    # Agua de lavado
    ax1.arrow(0.68, y_base + 0.16, 0, 0.06, head_width=0.01, head_length=0.008,
             fc='cyan', ec='cyan', linewidth=1)
    ax1.text(0.68, y_base + 0.24, 'H₂O', ha='center', fontsize=6)

    # Flecha al secado
    ax1.arrow(0.72, y_base + 0.08, 0.04, 0, head_width=0.015, head_length=0.01,
             fc='green', ec='green', linewidth=2)

    # 7. Secado
    dry_rect = Rectangle((0.76, y_base + 0.02), 0.08, 0.12,
                         edgecolor='orange', facecolor='lightyellow',
                         linewidth=2)
    ax1.add_patch(dry_rect)
    ax1.text(0.80, y_base + 0.08, 'Secado', ha='center', va='center',
             fontsize=7, fontweight='bold')

    # Flecha al producto final
    ax1.arrow(0.84, y_base + 0.08, 0.04, 0, head_width=0.015, head_length=0.01,
             fc='darkgreen', ec='darkgreen', linewidth=2.5)

    # 8. Producto Final (Biodiesel)
    biodiesel_box = FancyBboxPatch((0.88, y_base), 0.10, 0.16,
                                   boxstyle="round,pad=0.02",
                                   edgecolor='darkgreen', facecolor='lightgreen',
                                   linewidth=3)
    ax1.add_patch(biodiesel_box)
    ax1.text(0.93, y_base + 0.08, 'BIODIESEL\nB100', ha='center', va='center',
             fontsize=8, fontweight='bold', color='darkgreen')

    # Título de reacción
    ax1.text(0.50, y_base - 0.15,
             'Triglicéridos + 3 Metanol → 3 Biodiesel (FAME) + Glicerol',
             ha='center', fontsize=9, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 2: Producción por Equipo ==========
    ax2 = fig.add_subplot(gs[2, 0])

    equipos_list = ['Reactor', 'Separador', 'Lavado', 'Secado', 'Total']
    conversiones = [
        equipos.get('reactor', {}).get('conversion', 0.95) * 100,
        95.0,  # Eficiencia separación
        98.0,  # Eficiencia lavado
        99.5,  # Eficiencia secado
        equipos.get('reactor', {}).get('conversion', 0.95) * 0.95 * 0.98 * 0.995 * 100
    ]
    colors_equip = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

    bars = ax2.barh(equipos_list, conversiones, color=colors_equip, alpha=0.8,
                    edgecolor='black', linewidth=1.5)

    ax2.set_xlabel('Eficiencia / Conversión (%)', fontweight='bold', fontsize=11)
    ax2.set_title('Eficiencia por Etapa', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.set_xlim([0, 105])

    # Valores
    for bar, val in zip(bars, conversiones):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2.,
                f' {val:.1f}%', ha='left', va='center', fontsize=9, fontweight='bold')

    # ========== Subplot 3: Balance de Materia ==========
    ax3 = fig.add_subplot(gs[2, 1])

    # Entradas y salidas
    entradas = ['Aceite\nVegetal', 'Metanol', 'Catalizador', 'Agua\nLavado']
    F_entradas = [
        balance.get('aceite_kg', 1000),
        balance.get('metanol_kg', 150),
        balance.get('catalizador_kg', 10),
        balance.get('agua_lavado_kg', 500)
    ]

    salidas = ['Biodiesel', 'Glicerol', 'Agua\nResiduos']
    F_salidas = [
        balance.get('biodiesel_kg', 980),
        balance.get('glicerol_kg', 100),
        balance.get('residuos_kg', 580)
    ]

    # Graficar
    x_in = np.arange(len(entradas))
    x_out = np.arange(len(salidas))

    ax3_twin = ax3.twinx()

    bars_in = ax3.bar(x_in - 0.5, F_entradas, 0.4, label='Entradas',
                      color='#3498db', alpha=0.8, edgecolor='black')
    bars_out = ax3_twin.bar(x_out + 0.5, F_salidas, 0.4, label='Salidas',
                            color='#2ecc71', alpha=0.8, edgecolor='black')

    ax3.set_ylabel('Entradas (kg/h)', fontweight='bold', fontsize=10, color='#3498db')
    ax3_twin.set_ylabel('Salidas (kg/h)', fontweight='bold', fontsize=10, color='#2ecc71')
    ax3.set_title('Balance de Materia Global', fontsize=12, fontweight='bold')
    ax3.set_xticks(np.arange(max(len(entradas), len(salidas))))
    ax3.set_xticklabels(entradas + ['']*(max(len(entradas), len(salidas)) - len(entradas)),
                        fontsize=8)
    ax3_twin.set_xticks(np.arange(max(len(entradas), len(salidas))))
    ax3_twin.set_xticklabels(['']*(max(len(entradas), len(salidas)) - len(salidas)) + salidas,
                             fontsize=8)

    # ========== Subplot 4: Composición del Biodiesel ==========
    ax4 = fig.add_subplot(gs[2, 2])

    # Composición típica de biodiesel (FAMEs)
    componentes_bd = ['Metil\nOleato', 'Metil\nLinoleato', 'Metil\nPalmitato', 'Otros']
    comp_bd = [
        corrientes.get('biodiesel', {}).get('oleato', 0.45),
        corrientes.get('biodiesel', {}).get('linoleato', 0.25),
        corrientes.get('biodiesel', {}).get('palmitato', 0.18),
        corrientes.get('biodiesel', {}).get('otros', 0.12)
    ]
    colors_bd = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#FECA57']

    wedges, texts, autotexts = ax4.pie(comp_bd, labels=componentes_bd,
                                         autopct='%1.1f%%', startangle=90,
                                         colors=colors_bd,
                                         explode=[0.05, 0.05, 0.05, 0.05])

    ax4.set_title('Composición del Biodiesel (B100)', fontsize=12, fontweight='bold')

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)

    # ========== Subplot 5: Propiedades del Biodiesel ==========
    ax5 = fig.add_subplot(gs[3, 0])
    ax5.axis('off')
    ax5.set_title('Propiedades del Biodiesel', fontsize=12, fontweight='bold', pad=10)

    props_biodiesel = data.get('propiedades_biodiesel', {})

    props_text = f"""
    PROPIEDADES DEL BIODIESEL (B100)
    ═══════════════════════════════════════════

    FÍSICAS:
      Densidad (15°C):      {props_biodiesel.get('densidad_kg_m3', 880):.1f} kg/m³
      Viscosidad (40°C):    {props_biodiesel.get('viscosidad_cSt', 4.5):.2f} cSt
      Punto de inflamación: {props_biodiesel.get('flash_point_C', 170):.0f} °C
      Punto de nube:        {props_biodiesel.get('cloud_point_C', -3):.0f} °C

    QUÍMICAS:
      Número de cetano:     {props_biodiesel.get('cetane_number', 55):.0f}
      Índice de acidez:     {props_biodiesel.get('acid_value', 0.3):.2f} mg KOH/g
      Contenido de éster:   {props_biodiesel.get('ester_content', 98.5):.1f}%
      Glicerol libre:       {props_biodiesel.get('free_glycerol', 0.015):.3f}%

    ENERGÍA:
      Poder calorífico:     {props_biodiesel.get('heating_value_MJ_kg', 39.5):.1f} MJ/kg

    {'✓ Cumple norma ASTM D6751' if props_biodiesel.get('ester_content', 98.5) > 96.5 else '⚠ No cumple norma'}
    """

    color_props = 'lightgreen' if props_biodiesel.get('ester_content', 98.5) > 96.5 else 'lightyellow'

    ax5.text(0.5, 0.5, props_text, ha='center', va='center',
             fontsize=7.5, family='monospace',
             bbox=dict(boxstyle='round', facecolor=color_props, alpha=0.8))

    # ========== Subplot 6: Rendimientos ==========
    ax6 = fig.add_subplot(gs[3, 1])

    rendimientos = ['Conversión\nReactor', 'Rendimiento\nGlobal', 'Pureza\nBiodiesel']
    valores_rend = [
        equipos.get('reactor', {}).get('conversion', 0.95) * 100,
        balance.get('rendimiento_global', 0.88) * 100,
        props_biodiesel.get('ester_content', 98.5)
    ]
    colors_rend = ['#e74c3c', '#3498db', '#2ecc71']

    bars_rend = ax6.bar(rendimientos, valores_rend, color=colors_rend, alpha=0.8,
                        edgecolor='black', linewidth=2, width=0.6)

    ax6.set_ylabel('Porcentaje (%)', fontweight='bold', fontsize=11)
    ax6.set_title('Indicadores de Rendimiento', fontsize=12, fontweight='bold')
    ax6.grid(axis='y', alpha=0.3, linestyle='--')
    ax6.set_ylim([0, 105])

    # Valores sobre barras
    for bar, val in zip(bars_rend, valores_rend):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    # Línea de especificación
    ax6.axhline(y=96.5, color='red', linestyle='--', linewidth=2,
               alpha=0.5, label='Mín. ASTM D6751')
    ax6.legend(fontsize=9)

    # ========== Subplot 7: Análisis Económico ==========
    ax7 = fig.add_subplot(gs[3, 2])
    ax7.axis('off')
    ax7.set_title('Análisis Económico', fontsize=12, fontweight='bold', pad=10)

    economia_text = f"""
    ANÁLISIS ECONÓMICO
    ═══════════════════════════════════════════

    CAPACIDAD:
      Producción:           {economia.get('produccion_kg_h', 980):.0f} kg/h
      Operación:            {economia.get('horas_año', 8000):.0f} h/año
      Producción anual:     {economia.get('produccion_ton_año', 7840):.0f} ton/año

    COSTOS OPERATIVOS ($/kg biodiesel):
      Aceite vegetal:       ${economia.get('costo_aceite', 0.65):.2f}
      Metanol:              ${economia.get('costo_metanol', 0.08):.2f}
      Catalizador:          ${economia.get('costo_catalizador', 0.02):.2f}
      Agua y utilidades:    ${economia.get('costo_utilidades', 0.05):.2f}
      Total operativo:      ${economia.get('costo_total_kg', 0.80):.2f}/kg

    INGRESOS ($/kg):
      Biodiesel:            ${economia.get('precio_biodiesel', 1.20):.2f}
      Glicerol (subprod.):  ${economia.get('precio_glicerol', 0.40):.2f}

    MARGEN BRUTO:          ${economia.get('margen_bruto_kg', 0.40):.2f}/kg ({economia.get('margen_bruto_pct', 33.3):.1f}%)

    ROI estimado:          {economia.get('roi_años', 3.5):.1f} años
    """

    color_econ = 'lightgreen' if economia.get('margen_bruto_kg', 0.40) > 0.30 else 'lightyellow'

    ax7.text(0.5, 0.5, economia_text, ha='center', va='center',
             fontsize=7.5, family='monospace',
             bbox=dict(boxstyle='round', facecolor=color_econ, alpha=0.8))

    # Nota al pie
    fig.text(0.5, 0.01,
             f'Fuente: ASPEN HYSYS | Planta Biodiesel - Capacidad: {economia.get("produccion_ton_año", 7840):.0f} ton/año | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()

    # Guardar
    output_file = '/home/user/aspen_python_API/practica8/planta_biodiesel_aspen.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    # Resumen en consola
    print("\n📊 RESUMEN DE LA PLANTA:")
    print(f"   Capacidad:        {economia.get('produccion_kg_h', 980):.0f} kg/h")
    print(f"   Conversión:       {equipos.get('reactor', {}).get('conversion', 0.95)*100:.1f}%")
    print(f"   Rendimiento:      {balance.get('rendimiento_global', 0.88)*100:.1f}%")
    print(f"   Pureza biodiesel: {props_biodiesel.get('ester_content', 98.5):.1f}%")
    print(f"   Margen bruto:     ${economia.get('margen_bruto_kg', 0.40):.2f}/kg")

    print("="*60)

def get_reference_data():
    """Datos de referencia si no existe el archivo JSON"""
    return {
        'corrientes': {
            'aceite': {'F_kg_h': 1000, 'T_C': 60},
            'metanol': {'F_kg_h': 150, 'T_C': 25},
            'biodiesel': {
                'F_kg_h': 980,
                'oleato': 0.45,
                'linoleato': 0.25,
                'palmitato': 0.18,
                'otros': 0.12
            },
            'glicerol': {'F_kg_h': 100, 'pureza': 0.85}
        },
        'equipos': {
            'reactor': {
                'tipo': 'CSTR',
                'volumen_m3': 3.0,
                'T_C': 60,
                'conversion': 0.95
            },
            'separador': {'eficiencia': 0.95},
            'lavado': {'eficiencia': 0.98},
            'secado': {'eficiencia': 0.995}
        },
        'balance': {
            'aceite_kg': 1000,
            'metanol_kg': 150,
            'catalizador_kg': 10,
            'agua_lavado_kg': 500,
            'biodiesel_kg': 980,
            'glicerol_kg': 100,
            'residuos_kg': 580,
            'rendimiento_global': 0.88
        },
        'propiedades_biodiesel': {
            'densidad_kg_m3': 880,
            'viscosidad_cSt': 4.5,
            'flash_point_C': 170,
            'cloud_point_C': -3,
            'cetane_number': 55,
            'acid_value': 0.3,
            'ester_content': 98.5,
            'free_glycerol': 0.015,
            'heating_value_MJ_kg': 39.5
        },
        'economia': {
            'produccion_kg_h': 980,
            'horas_año': 8000,
            'produccion_ton_año': 7840,
            'costo_aceite': 0.65,
            'costo_metanol': 0.08,
            'costo_catalizador': 0.02,
            'costo_utilidades': 0.05,
            'costo_total_kg': 0.80,
            'precio_biodiesel': 1.20,
            'precio_glicerol': 0.40,
            'margen_bruto_kg': 0.40,
            'margen_bruto_pct': 33.3,
            'roi_años': 3.5
        }
    }

if __name__ == '__main__':
    main()
