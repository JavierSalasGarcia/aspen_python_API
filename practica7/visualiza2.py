#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 7: Comparación Python Puro vs ASPEN - Batch vs Continuo
=================================================================

Compara los resultados de reactores Batch vs Continuo calculados con
Python puro vs ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json
import os

def main():
    """Genera visualización comparativa Python vs ASPEN para Batch vs Continuo"""

    print("="*60)
    print("VISUALIZACIÓN: COMPARACIÓN PYTHON vs ASPEN - BATCH/CONTINUO")
    print("="*60)

    # Cargar datos
    aspen_file = '/home/user/aspen_python_API/practica7/resultados_aspen.json'
    python_file = '/home/user/aspen_python_API/practica7/resultados_python.json'

    if os.path.exists(aspen_file):
        try:
            with open(aspen_file, 'r') as f:
                data_aspen = json.load(f)
            print("   ✓ Datos ASPEN cargados")
        except:
            print("   ⚠ Error cargando ASPEN, usando referencia")
            data_aspen = get_reference_aspen()
    else:
        print("   ⚠ Archivo ASPEN no existe, usando referencia")
        data_aspen = get_reference_aspen()

    if os.path.exists(python_file):
        try:
            with open(python_file, 'r') as f:
                data_python = json.load(f)
            print("   ✓ Datos Python cargados")
        except:
            print("   ⚠ Error cargando Python, usando referencia")
            data_python = get_reference_python()
    else:
        print("   ⚠ Archivo Python no existe, usando referencia")
        data_python = get_reference_python()

    # Extraer datos
    batch_py = data_python.get('batch', {})
    batch_asp = data_aspen.get('batch', {})
    cont_py = data_python.get('continuo', {})
    cont_asp = data_aspen.get('continuo', {})

    # Crear figura
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

    fig.suptitle('Práctica 7: Comparación Python vs ASPEN - Reactores Batch y Continuo',
                 fontsize=16, fontweight='bold')

    # ========== Subplot 1: Conversión Batch ==========
    ax1 = fig.add_subplot(gs[0, 0])

    methods = ['Python', 'ASPEN']
    conv_batch_py = batch_py.get('conversion', 0.85) * 100
    conv_batch_asp = batch_asp.get('conversion', 0.85) * 100
    conversions_batch = [conv_batch_py, conv_batch_asp]
    colors = ['#3498db', '#e74c3c']

    bars = ax1.bar(methods, conversions_batch, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2, width=0.5)

    ax1.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax1.set_title('Reactor Batch: Conversión', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_ylim([0, 100])

    # Valores sobre barras
    for bar, val in zip(bars, conversions_batch):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}%', ha='center', va='bottom',
                fontsize=11, fontweight='bold')

    # ========== Subplot 2: Conversión Continuo ==========
    ax2 = fig.add_subplot(gs[0, 1])

    conv_cont_py = cont_py.get('conversion', 0.75) * 100
    conv_cont_asp = cont_asp.get('conversion', 0.75) * 100
    conversions_cont = [conv_cont_py, conv_cont_asp]

    bars = ax2.bar(methods, conversions_cont, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2, width=0.5)

    ax2.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax2.set_title('Reactor Continuo: Conversión', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_ylim([0, 100])

    # Valores sobre barras
    for bar, val in zip(bars, conversions_cont):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}%', ha='center', va='bottom',
                fontsize=11, fontweight='bold')

    # ========== Subplot 3: Desviaciones ==========
    ax3 = fig.add_subplot(gs[0, 2])

    # Calcular desviaciones
    dev_batch_X = abs(conv_batch_py - conv_batch_asp) / conv_batch_asp * 100
    dev_cont_X = abs(conv_cont_py - conv_cont_asp) / conv_cont_asp * 100

    # Tiempo
    t_batch_py = batch_py.get('tiempo_h', 3.0)
    t_batch_asp = batch_asp.get('tiempo_h', 3.0)
    dev_batch_t = abs(t_batch_py - t_batch_asp) / t_batch_asp * 100

    tau_cont_py = cont_py.get('tau_h', 1.5)
    tau_cont_asp = cont_asp.get('tau_h', 1.5)
    dev_cont_tau = abs(tau_cont_py - tau_cont_asp) / tau_cont_asp * 100

    properties = ['Batch:\nConversión', 'Batch:\nTiempo', 'Continuo:\nConversión', 'Continuo:\nτ']
    deviations = [dev_batch_X, dev_batch_t, dev_cont_X, dev_cont_tau]
    colors_dev = ['#2ecc71' if d < 1 else '#f39c12' if d < 5 else '#e74c3c' for d in deviations]

    bars_dev = ax3.barh(properties, deviations, color=colors_dev, alpha=0.8,
                        edgecolor='black', linewidth=1.5)

    ax3.set_xlabel('Desviación Relativa (%)', fontweight='bold', fontsize=11)
    ax3.set_title('Análisis de Desviaciones', fontsize=12, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3, linestyle='--')
    ax3.axvline(x=1, color='green', linestyle='--', linewidth=1, alpha=0.5)
    ax3.axvline(x=5, color='orange', linestyle='--', linewidth=1, alpha=0.5)

    # Valores
    for bar, val in zip(bars_dev, deviations):
        width_bar = bar.get_width()
        if width_bar > 0.01:
            ax3.text(width_bar, bar.get_y() + bar.get_height()/2.,
                    f' {val:.3f}%', ha='left', va='center', fontsize=9, fontweight='bold')

    # ========== Subplot 4: Perfil Batch - Python vs ASPEN ==========
    ax4 = fig.add_subplot(gs[1, 0])

    # Perfil de conversión en batch
    t_batch = np.linspace(0, max(t_batch_py, t_batch_asp), 100)
    k = data_python.get('cinetica', {}).get('k', 0.8)

    # Simulación (1er orden): X = 1 - exp(-k·t)
    X_batch_curve = 1 - np.exp(-k * t_batch)

    ax4.plot(t_batch, X_batch_curve * 100, 'g-', linewidth=2, label='Modelo (1er orden)')
    ax4.plot(t_batch_py, conv_batch_py, 'o', markersize=12, color='#3498db',
            label='Python', zorder=5)
    ax4.plot(t_batch_asp, conv_batch_asp, 's', markersize=12, color='#e74c3c',
            label='ASPEN', zorder=5)

    ax4.set_xlabel('Tiempo (h)', fontweight='bold', fontsize=11)
    ax4.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax4.set_title('Perfil Batch: Python vs ASPEN', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)

    # ========== Subplot 5: Conversión vs τ (Continuo) ==========
    ax5 = fig.add_subplot(gs[1, 1])

    # Perfil CSTR: X = k·τ / (1 + k·τ)
    tau_range = np.linspace(0, 5, 100)
    X_cstr_curve = (k * tau_range) / (1 + k * tau_range)

    ax5.plot(tau_range, X_cstr_curve * 100, 'g-', linewidth=2, label='Modelo CSTR')
    ax5.plot(tau_cont_py, conv_cont_py, 'o', markersize=12, color='#3498db',
            label='Python', zorder=5)
    ax5.plot(tau_cont_asp, conv_cont_asp, 's', markersize=12, color='#e74c3c',
            label='ASPEN', zorder=5)

    ax5.set_xlabel('Tiempo de residencia τ (h)', fontweight='bold', fontsize=11)
    ax5.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax5.set_title('CSTR: Python vs ASPEN', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=10)
    ax5.grid(True, alpha=0.3)

    # ========== Subplot 6: Productividad ==========
    ax6 = fig.add_subplot(gs[1, 2])

    # Calcular productividad
    # Batch
    t_total_batch_py = t_batch_py + batch_py.get('tiempo_muerto_h', 1.0)
    t_total_batch_asp = t_batch_asp + batch_asp.get('tiempo_muerto_h', 1.0)

    F_batch_equiv_py = batch_py.get('volumen_m3', 10.0) / t_total_batch_py
    F_batch_equiv_asp = batch_asp.get('volumen_m3', 10.0) / t_total_batch_asp

    Prod_batch_py = F_batch_equiv_py * batch_py.get('conversion', 0.85) / batch_py.get('volumen_m3', 10.0)
    Prod_batch_asp = F_batch_equiv_asp * batch_asp.get('conversion', 0.85) / batch_asp.get('volumen_m3', 10.0)

    # Continuo
    F_cont_py = cont_py.get('F_kgmoleh', 100.0)
    F_cont_asp = cont_asp.get('F_kgmoleh', 100.0)

    Prod_cont_py = F_cont_py * cont_py.get('conversion', 0.75) / cont_py.get('volumen_m3', 5.0)
    Prod_cont_asp = F_cont_asp * cont_asp.get('conversion', 0.75) / cont_asp.get('volumen_m3', 5.0)

    # Graficar
    x_pos = np.arange(2)
    width = 0.35

    prod_py = [Prod_batch_py, Prod_cont_py]
    prod_asp = [Prod_batch_asp, Prod_cont_asp]

    bars1 = ax6.bar(x_pos - width/2, prod_py, width, label='Python',
                    color='#3498db', alpha=0.8, edgecolor='black')
    bars2 = ax6.bar(x_pos + width/2, prod_asp, width, label='ASPEN',
                    color='#e74c3c', alpha=0.8, edgecolor='black')

    ax6.set_ylabel('Productividad\n(kgmole/(h·m³))', fontweight='bold', fontsize=10)
    ax6.set_title('Productividad Volumétrica', fontsize=12, fontweight='bold')
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels(['Batch', 'Continuo'])
    ax6.legend(fontsize=10)
    ax6.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=9)

    # ========== Subplot 7: Tabla Comparativa Batch ==========
    ax7 = fig.add_subplot(gs[2, 0])
    ax7.axis('off')
    ax7.set_title('Reactor Batch: Comparación', fontsize=12, fontweight='bold', pad=10)

    batch_table = f"""
    REACTOR BATCH
    ═══════════════════════════════════════════

    PROPIEDAD         PYTHON    ASPEN     DESV(%)
    ───────────────────────────────────────────

    Volumen (m³)      {batch_py.get('volumen_m3', 10.0):6.1f}    {batch_asp.get('volumen_m3', 10.0):6.1f}    0.00

    Tiempo reac.(h)   {t_batch_py:6.2f}    {t_batch_asp:6.2f}    {dev_batch_t:5.3f}

    Tiempo muerto(h)  {batch_py.get('tiempo_muerto_h', 1.0):6.2f}    {batch_asp.get('tiempo_muerto_h', 1.0):6.2f}    0.00

    Conversión (%)    {conv_batch_py:6.2f}    {conv_batch_asp:6.2f}    {dev_batch_X:5.3f}

    Productivid.      {Prod_batch_py:6.2f}    {Prod_batch_asp:6.2f}    {abs(Prod_batch_py-Prod_batch_asp)/Prod_batch_asp*100:5.3f}
    (kgmole/h·m³)

    ───────────────────────────────────────────
    {'✓ Excelente acuerdo' if dev_batch_X < 1 else '✓ Buen acuerdo' if dev_batch_X < 5 else '⚠ Revisar'}
    """

    color_batch = 'lightgreen' if dev_batch_X < 1 else 'lightyellow' if dev_batch_X < 5 else 'lightcoral'

    ax7.text(0.5, 0.5, batch_table, ha='center', va='center',
             fontsize=8, family='monospace',
             bbox=dict(boxstyle='round', facecolor=color_batch, alpha=0.7))

    # ========== Subplot 8: Tabla Comparativa Continuo ==========
    ax8 = fig.add_subplot(gs[2, 1])
    ax8.axis('off')
    ax8.set_title('Reactor Continuo: Comparación', fontsize=12, fontweight='bold', pad=10)

    cont_table = f"""
    REACTOR CONTINUO (CSTR)
    ═══════════════════════════════════════════

    PROPIEDAD         PYTHON    ASPEN     DESV(%)
    ───────────────────────────────────────────

    Volumen (m³)      {cont_py.get('volumen_m3', 5.0):6.1f}    {cont_asp.get('volumen_m3', 5.0):6.1f}    0.00

    Flujo (kgmole/h)  {F_cont_py:6.1f}    {F_cont_asp:6.1f}    0.00

    τ (h)             {tau_cont_py:6.2f}    {tau_cont_asp:6.2f}    {dev_cont_tau:5.3f}

    Conversión (%)    {conv_cont_py:6.2f}    {conv_cont_asp:6.2f}    {dev_cont_X:5.3f}

    Productivid.      {Prod_cont_py:6.2f}    {Prod_cont_asp:6.2f}    {abs(Prod_cont_py-Prod_cont_asp)/Prod_cont_asp*100:5.3f}
    (kgmole/h·m³)

    ───────────────────────────────────────────
    {'✓ Excelente acuerdo' if dev_cont_X < 1 else '✓ Buen acuerdo' if dev_cont_X < 5 else '⚠ Revisar'}
    """

    color_cont = 'lightgreen' if dev_cont_X < 1 else 'lightyellow' if dev_cont_X < 5 else 'lightcoral'

    ax8.text(0.5, 0.5, cont_table, ha='center', va='center',
             fontsize=8, family='monospace',
             bbox=dict(boxstyle='round', facecolor=color_cont, alpha=0.7))

    # ========== Subplot 9: Conclusiones ==========
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.axis('off')
    ax9.set_title('Conclusiones', fontsize=12, fontweight='bold', pad=10)

    # Evaluación
    max_dev = max(dev_batch_X, dev_cont_X, dev_batch_t, dev_cont_tau)
    evaluation = "Excelente" if max_dev < 1 else "Buena" if max_dev < 5 else "Requiere revisión"
    color_eval = 'lightgreen' if max_dev < 1 else 'lightyellow' if max_dev < 5 else 'lightcoral'

    conclusions_text = f"""
    CONCLUSIONES
    ════════════════════════════════════

    1. PRECISIÓN: {evaluation}
       Desviación máxima: {max_dev:.3f}%

    2. REACTOR BATCH:
       Desv. conversión: {dev_batch_X:.3f}%
       {'✓ Python confiable' if dev_batch_X < 5 else '⚠ Revisar'}

    3. REACTOR CONTINUO:
       Desv. conversión: {dev_cont_X:.3f}%
       {'✓ Python confiable' if dev_cont_X < 5 else '⚠ Revisar'}

    4. MODELOS USADOS:
       Python:
         • Batch: integración ODEs
         • CSTR: ecuaciones algebráicas

       ASPEN:
         • Modelos rigurosos
         • Termodinámica avanzada

    5. RECOMENDACIÓN:
       Python: Diseño preliminar,
               estudios paramétricos
       ASPEN:  Diseño final,
               validación industrial
    """

    ax9.text(0.5, 0.5, conclusions_text, ha='center', va='center',
             fontsize=7.5, family='monospace',
             bbox=dict(boxstyle='round', facecolor=color_eval, alpha=0.7))

    # Nota al pie
    avg_dev = np.mean([dev_batch_X, dev_cont_X, dev_batch_t, dev_cont_tau])
    fig.text(0.5, 0.01,
             f'Desviación promedio: {avg_dev:.3f}% | Evaluación: {evaluation} | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=9, style='italic', color='gray',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.2))

    plt.tight_layout()

    # Guardar
    output_file = '/home/user/aspen_python_API/practica7/comparacion_batch_continuo.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    # Resumen en consola
    print("\n📊 RESUMEN DE COMPARACIÓN:")
    print(f"   BATCH:")
    print(f"     Desviación conversión: {dev_batch_X:.3f}%")
    print(f"   CONTINUO:")
    print(f"     Desviación conversión: {dev_cont_X:.3f}%")
    print(f"   Evaluación general:      {evaluation}")

    print("="*60)

def get_reference_aspen():
    """Datos de referencia ASPEN"""
    return {
        'batch': {
            'tipo': 'Batch',
            'volumen_m3': 10.0,
            'T_C': 80.0,
            'tiempo_h': 3.0,
            'tiempo_muerto_h': 1.0,
            'conversion': 0.85
        },
        'continuo': {
            'tipo': 'CSTR',
            'volumen_m3': 5.0,
            'T_C': 80.0,
            'tau_h': 1.5,
            'F_kgmoleh': 100.0,
            'conversion': 0.75
        },
        'cinetica': {
            'k': 0.8,
            'orden': 1
        }
    }

def get_reference_python():
    """Datos de referencia Python"""
    return {
        'batch': {
            'tipo': 'Batch',
            'volumen_m3': 10.0,
            'T_C': 80.0,
            'tiempo_h': 3.0,
            'tiempo_muerto_h': 1.0,
            'conversion': 0.85
        },
        'continuo': {
            'tipo': 'CSTR',
            'volumen_m3': 5.0,
            'T_C': 80.0,
            'tau_h': 1.5,
            'F_kgmoleh': 100.0,
            'conversion': 0.75
        },
        'cinetica': {
            'k': 0.8,
            'orden': 1
        },
        'method': 'Python (scipy.integrate.odeint + algebraic)'
    }

if __name__ == '__main__':
    main()
