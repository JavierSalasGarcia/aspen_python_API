#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 7: Visualización de Reactor Batch vs Continuo (ASPEN HYSYS)
=====================================================================

Visualiza y compara los resultados de reactores Batch vs Continuos desde ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
from datetime import datetime
import json
import os

def main():
    """Genera visualización comparativa de reactores Batch vs Continuo desde ASPEN"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 7 - BATCH vs CONTINUO (ASPEN)")
    print("="*60)

    # Cargar datos si existen, sino usar valores de referencia
    json_file = '/home/user/aspen_python_API/practica7/resultados_aspen.json'

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
    batch = data.get('batch', {})
    continuo = data.get('continuo', {})

    # Crear figura
    fig = plt.figure(figsize=(16, 13))
    gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.35)

    fig.suptitle('Práctica 7: Comparación Reactor Batch vs Reactor Continuo (ASPEN HYSYS)',
                 fontsize=16, fontweight='bold')

    # ========== Subplot 1: Diagrama Reactor Batch ==========
    ax1 = fig.add_subplot(gs[0, 0:2])
    ax1.axis('off')
    ax1.set_title('Reactor Batch (Discontinuo)', fontsize=13, fontweight='bold', pad=15)

    # Reactor batch (tanque cerrado)
    batch_rect = FancyBboxPatch((0.30, 0.20), 0.40, 0.60,
                                boxstyle="round,pad=0.03",
                                edgecolor='darkblue', facecolor='lightblue',
                                linewidth=3.5)
    ax1.add_patch(batch_rect)

    # Tapa
    lid = Rectangle((0.28, 0.75), 0.44, 0.08,
                   edgecolor='darkblue', facecolor='gray', linewidth=2)
    ax1.add_patch(lid)

    # Agitador
    agitator = Circle((0.50, 0.50), 0.08, edgecolor='black',
                     facecolor='lightgray', linewidth=2)
    ax1.add_patch(agitator)
    ax1.plot([0.50, 0.50], [0.58, 0.75], 'k-', linewidth=3)

    # Aspas
    ax1.plot([0.42, 0.58], [0.50, 0.50], 'k-', linewidth=2.5)
    ax1.plot([0.50, 0.50], [0.42, 0.58], 'k-', linewidth=2.5)

    # Nivel de líquido
    ax1.fill_between([0.32, 0.68], [0.65, 0.65], [0.22, 0.22],
                     color='cyan', alpha=0.4)

    # Información del batch
    batch_text = f"""
    REACTOR BATCH

    Volumen: {batch.get('volumen_m3', 10.0):.1f} m³
    T: {batch.get('T_C', 80.0):.1f}°C
    Tiempo: {batch.get('tiempo_h', 3.0):.1f} h

    Conversión: {batch.get('conversion', 0.85)*100:.1f}%
    """

    ax1.text(0.50, 0.45, batch_text, ha='center', va='center',
             fontsize=9, fontweight='bold', color='darkblue',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # Etiqueta de operación
    ax1.text(0.50, 0.05, 'Operación: Carga → Reacción → Descarga → Limpieza',
             ha='center', fontsize=9, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 2: Diagrama Reactor Continuo ==========
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.axis('off')
    ax2.set_title('Reactor Continuo (CSTR)', fontsize=13, fontweight='bold', pad=15)

    # Entrada
    ax2.arrow(0.1, 0.7, 0.15, 0, head_width=0.05, head_length=0.03,
             fc='blue', ec='blue', linewidth=2)
    ax2.text(0.17, 0.78, 'Entrada', fontsize=8, ha='center')

    # Reactor continuo
    cont_rect = FancyBboxPatch((0.25, 0.20), 0.50, 0.70,
                               boxstyle="round,pad=0.03",
                               edgecolor='darkgreen', facecolor='lightgreen',
                               linewidth=3)
    ax2.add_patch(cont_rect)

    # Agitador
    agitator2 = Circle((0.50, 0.55), 0.06, edgecolor='black',
                      facecolor='lightgray', linewidth=2)
    ax2.add_patch(agitator2)
    ax2.plot([0.50, 0.50], [0.61, 0.85], 'k-', linewidth=2.5)

    # Nivel de líquido
    ax2.fill_between([0.27, 0.73], [0.70, 0.70], [0.22, 0.22],
                     color='lightgreen', alpha=0.5)

    # Salida
    ax2.arrow(0.75, 0.7, 0.15, 0, head_width=0.05, head_length=0.03,
             fc='darkgreen', ec='darkgreen', linewidth=2)
    ax2.text(0.83, 0.78, 'Salida', fontsize=8, ha='center')

    # Información del continuo
    cont_text = f"""
    CSTR

    V: {continuo.get('volumen_m3', 5.0):.1f} m³
    T: {continuo.get('T_C', 80.0):.1f}°C
    τ: {continuo.get('tau_h', 1.5):.1f} h

    X: {continuo.get('conversion', 0.75)*100:.1f}%
    """

    ax2.text(0.50, 0.45, cont_text, ha='center', va='center',
             fontsize=8, fontweight='bold', color='darkgreen',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # Etiqueta
    ax2.text(0.50, 0.05, 'Estado estacionario',
             ha='center', fontsize=8, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 3: Conversión vs Tiempo (Batch) ==========
    ax3 = fig.add_subplot(gs[1, 0])

    # Perfil de conversión en batch (asumiendo 1er orden)
    t_batch = np.linspace(0, batch.get('tiempo_h', 3.0), 100)
    k = 0.8  # constante ejemplo
    X_batch = 1 - np.exp(-k * t_batch)

    ax3.plot(t_batch, X_batch * 100, 'b-', linewidth=2.5, label='Batch')
    ax3.plot(batch.get('tiempo_h', 3.0), batch.get('conversion', 0.85) * 100,
            'ro', markersize=12, label='Punto final', zorder=5)

    ax3.set_xlabel('Tiempo (h)', fontweight='bold', fontsize=11)
    ax3.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax3.set_title('Perfil de Conversión - Batch', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)

    # Regiones
    ax3.axhspan(0, 50, alpha=0.1, color='red', label='Baja')
    ax3.axhspan(50, 80, alpha=0.1, color='yellow')
    ax3.axhspan(80, 100, alpha=0.1, color='green')

    # ========== Subplot 4: Comparación de Conversiones ==========
    ax4 = fig.add_subplot(gs[1, 1])

    reactors = ['Batch\n(t={:.1f}h)'.format(batch.get('tiempo_h', 3.0)),
                'Continuo\n(τ={:.1f}h)'.format(continuo.get('tau_h', 1.5))]
    conversions = [batch.get('conversion', 0.85) * 100,
                  continuo.get('conversion', 0.75) * 100]
    colors = ['#3498db', '#2ecc71']

    bars = ax4.bar(reactors, conversions, color=colors, alpha=0.8,
                   edgecolor='black', linewidth=2, width=0.6)

    ax4.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax4.set_title('Comparación: Conversión Final', fontsize=12, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    ax4.set_ylim([0, 100])

    # Valores sobre barras
    for bar, val in zip(bars, conversions):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom',
                fontsize=12, fontweight='bold')

    # ========== Subplot 5: Productividad ==========
    ax5 = fig.add_subplot(gs[1, 2])

    # Productividad = (F * X) / V
    # Batch: necesita considerar tiempo muerto
    t_total_batch = batch.get('tiempo_h', 3.0) + batch.get('tiempo_muerto_h', 1.0)
    F_batch_equiv = batch.get('volumen_m3', 10.0) / t_total_batch  # kgmole/h equivalente
    Prod_batch = F_batch_equiv * batch.get('conversion', 0.85) / batch.get('volumen_m3', 10.0)

    # Continuo
    F_cont = continuo.get('F_kgmoleh', 100.0)
    Prod_cont = F_cont * continuo.get('conversion', 0.75) / continuo.get('volumen_m3', 5.0)

    productivities = [Prod_batch, Prod_cont]
    colors_prod = ['#e74c3c', '#9b59b6']

    bars_prod = ax5.bar(reactors, productivities, color=colors_prod, alpha=0.8,
                        edgecolor='black', linewidth=2, width=0.6)

    ax5.set_ylabel('Productividad\n(kgmole/(h·m³))', fontweight='bold', fontsize=10)
    ax5.set_title('Productividad Volumétrica', fontsize=12, fontweight='bold')
    ax5.grid(axis='y', alpha=0.3, linestyle='--')

    # Valores
    for bar, val in zip(bars_prod, productivities):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom',
                fontsize=11, fontweight='bold')

    # ========== Subplot 6: Conversión vs Volumen ==========
    ax6 = fig.add_subplot(gs[2, 0])

    # Para misma conversión, comparar volumen necesario
    X_target = 0.75
    tau_range = np.linspace(0.1, 5, 100)

    # CSTR: X = k·τ / (1 + k·τ)
    X_cstr = (k * tau_range) / (1 + k * tau_range)

    # Batch: X = 1 - exp(-k·t)
    X_batch_curve = 1 - np.exp(-k * tau_range)

    ax6.plot(tau_range, X_batch_curve * 100, 'b-', linewidth=2.5, label='Batch')
    ax6.plot(tau_range, X_cstr * 100, 'g--', linewidth=2.5, label='CSTR')
    ax6.axhline(y=X_target * 100, color='red', linestyle=':', linewidth=2,
               label=f'Objetivo ({X_target*100:.0f}%)')

    ax6.set_xlabel('Tiempo / Tiempo de residencia (h)', fontweight='bold', fontsize=11)
    ax6.set_ylabel('Conversión (%)', fontweight='bold', fontsize=11)
    ax6.set_title('Conversión vs Tiempo de Reacción', fontsize=12, fontweight='bold')
    ax6.legend(fontsize=10)
    ax6.grid(True, alpha=0.3)

    # ========== Subplot 7: Tabla Comparativa ==========
    ax7 = fig.add_subplot(gs[2, 1:])
    ax7.axis('off')
    ax7.set_title('Tabla Comparativa Detallada', fontsize=13, fontweight='bold', pad=10)

    table_text = f"""
    PARÁMETRO                    BATCH           CONTINUO         VENTAJA
    ═══════════════════════════════════════════════════════════════════════

    CONFIGURACIÓN:
    Volumen reactor (m³)         {batch.get('volumen_m3', 10.0):6.1f}          {continuo.get('volumen_m3', 5.0):6.1f}          {'Continuo' if continuo.get('volumen_m3', 5.0) < batch.get('volumen_m3', 10.0) else 'Batch'}
    Temperatura (°C)             {batch.get('T_C', 80.0):6.1f}          {continuo.get('T_C', 80.0):6.1f}          Igual

    TIEMPO:
    Tiempo reacción (h)          {batch.get('tiempo_h', 3.0):6.2f}          {continuo.get('tau_h', 1.5):6.2f} (τ)       {'Continuo' if continuo.get('tau_h', 1.5) < batch.get('tiempo_h', 3.0) else 'Batch'}
    Tiempo muerto (h)            {batch.get('tiempo_muerto_h', 1.0):6.2f}          0.00            Continuo
    Tiempo total ciclo (h)       {batch.get('tiempo_h', 3.0) + batch.get('tiempo_muerto_h', 1.0):6.2f}          -               -

    RENDIMIENTO:
    Conversión (%)               {batch.get('conversion', 0.85)*100:6.2f}          {continuo.get('conversion', 0.75)*100:6.2f}          {'Batch' if batch.get('conversion', 0.85) > continuo.get('conversion', 0.75) else 'Continuo'}
    Productividad (kgmole/h·m³)  {Prod_batch:6.2f}          {Prod_cont:6.2f}          {'Continuo' if Prod_cont > Prod_batch else 'Batch'}

    FLEXIBILIDAD:
    Cambio de producto           Alta            Baja            Batch
    Control de calidad           Lote por lote   Continuo        Batch
    Startup/Shutdown             Frecuente       Raro            Continuo

    ECONÓMICO:
    Inversión inicial            Baja            Alta            Batch
    Costo operativo unitario     Alto            Bajo            Continuo
    Escala de producción         Pequeña/Media   Grande          Continuo
    """

    ax7.text(0.5, 0.5, table_text, ha='center', va='center',
             fontsize=7, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6))

    # ========== Subplot 8: Ventajas Batch ==========
    ax8 = fig.add_subplot(gs[3, 0])
    ax8.axis('off')
    ax8.set_title('Ventajas: Reactor Batch', fontsize=12, fontweight='bold', pad=10)

    batch_adv = """
    REACTOR BATCH
    ═══════════════════════════════════

    VENTAJAS:
    ✓ Flexibilidad para cambiar producto
    ✓ Menor inversión inicial
    ✓ Fácil control de calidad (lote)
    ✓ Mejor para producciones pequeñas
    ✓ Ideal para productos de alto valor
    ✓ Permite ajustes entre lotes
    ✓ Menor riesgo en desarrollo

    IDEAL PARA:
    • Farmacéuticos
    • Especialidades químicas
    • Pequeñas producciones
    • Productos múltiples
    • Desarrollo de procesos

    CONVERSIÓN TÍPICA: Alta
    (Mayor tiempo de reacción)
    """

    ax8.text(0.5, 0.5, batch_adv, ha='center', va='center',
             fontsize=8, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # ========== Subplot 9: Ventajas Continuo ==========
    ax9 = fig.add_subplot(gs[3, 1])
    ax9.axis('off')
    ax9.set_title('Ventajas: Reactor Continuo', fontsize=12, fontweight='bold', pad=10)

    cont_adv = """
    REACTOR CONTINUO (CSTR)
    ═══════════════════════════════════

    VENTAJAS:
    ✓ Mayor productividad
    ✓ Menor costo operativo/unidad
    ✓ Estado estacionario
    ✓ Sin tiempo muerto
    ✓ Mejor para grandes volúmenes
    ✓ Control automatizado
    ✓ Calidad consistente

    IDEAL PARA:
    • Commodities químicos
    • Grandes producciones
    • Productos únicos
    • Operación 24/7
    • Economías de escala

    PRODUCTIVIDAD: Mayor
    (Sin tiempos muertos)
    """

    ax9.text(0.5, 0.5, cont_adv, ha='center', va='center',
             fontsize=8, family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    # ========== Subplot 10: Conclusiones ==========
    ax10 = fig.add_subplot(gs[3, 2])
    ax10.axis('off')
    ax10.set_title('Conclusiones', fontsize=12, fontweight='bold', pad=10)

    conclusions = f"""
    CONCLUSIONES
    ═══════════════════════════════════

    1. CONVERSIÓN:
       Batch:     {batch.get('conversion', 0.85)*100:.1f}%
       Continuo:  {continuo.get('conversion', 0.75)*100:.1f}%
       {'✓ Batch mayor' if batch.get('conversion', 0.85) > continuo.get('conversion', 0.75) else '✓ Continuo mayor'}

    2. PRODUCTIVIDAD:
       Batch:     {Prod_batch:.2f}
       Continuo:  {Prod_cont:.2f}
       {'✓ Continuo mayor' if Prod_cont > Prod_batch else '✓ Batch mayor'}

    3. SELECCIÓN:
       Batch si:
         • Prod. pequeña/media
         • Alta flexibilidad
         • Productos múltiples

       Continuo si:
         • Prod. grande
         • Un producto
         • Bajo costo unitario

    4. HÍBRIDO:
       • Semi-batch
       • Fed-batch
       • Combina ventajas
    """

    ax10.text(0.5, 0.5, conclusions, ha='center', va='center',
              fontsize=7.5, family='monospace',
              bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    # Nota al pie
    fig.text(0.5, 0.01,
             f'Fuente: ASPEN HYSYS | Análisis: Batch vs Continuo | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()

    # Guardar
    output_file = '/home/user/aspen_python_API/practica7/batch_vs_continuo_aspen.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    # Resumen en consola
    print("\n📊 RESUMEN:")
    print(f"   BATCH:")
    print(f"     Conversión:     {batch.get('conversion', 0.85)*100:.1f}%")
    print(f"     Tiempo:         {batch.get('tiempo_h', 3.0):.1f} h")
    print(f"     Productividad:  {Prod_batch:.2f} kgmole/(h·m³)")
    print(f"\n   CONTINUO:")
    print(f"     Conversión:     {continuo.get('conversion', 0.75)*100:.1f}%")
    print(f"     Tiempo resid.:  {continuo.get('tau_h', 1.5):.1f} h")
    print(f"     Productividad:  {Prod_cont:.2f} kgmole/(h·m³)")

    print("="*60)

def get_reference_data():
    """Datos de referencia si no existe el archivo JSON"""
    return {
        'batch': {
            'tipo': 'Batch',
            'volumen_m3': 10.0,
            'T_C': 80.0,
            'P_kPa': 101.325,
            'tiempo_h': 3.0,
            'tiempo_muerto_h': 1.0,  # Carga, descarga, limpieza
            'conversion': 0.85,
            'composicion_inicial': {'A': 0.9, 'B': 0.1},
            'composicion_final': {'A': 0.135, 'B': 0.865}
        },
        'continuo': {
            'tipo': 'CSTR',
            'volumen_m3': 5.0,
            'T_C': 80.0,
            'P_kPa': 101.325,
            'tau_h': 1.5,
            'F_kgmoleh': 100.0,
            'conversion': 0.75,
            'composicion_entrada': {'A': 0.9, 'B': 0.1},
            'composicion_salida': {'A': 0.225, 'B': 0.775}
        },
        'cinetica': {
            'k': 0.8,  # 1/h
            'orden': 1,
            'reaccion': 'A → B'
        }
    }

if __name__ == '__main__':
    main()
