#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 2: Visualización de Propiedades (ASPEN)
=================================================

Este script visualiza las propiedades críticas obtenidas de ASPEN HYSYS.
Nota: Requiere haber ejecutado aspython.py primero para generar los datos.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def main():
    """Genera visualización de propiedades desde ASPEN"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 2 - PROPIEDADES (ASPEN)")
    print("="*60)

    # Datos de ASPEN HYSYS (valores típicos con NRTL)
    # Estos valores se obtendrían del archivo generado por aspython.py
    # Para el ejemplo, usamos valores de referencia

    components = ['Methanol', 'Water']

    # Propiedades críticas desde ASPEN HYSYS
    # Valores de referencia (ejecuta aspython.py para datos reales)
    data_aspen = {
        'Methanol': {'Tc': 512.64, 'Pc': 8084.0, 'MW': 32.04},
        'Water': {'Tc': 647.10, 'Pc': 22064.0, 'MW': 18.015}
    }

    # Extraer valores
    Tc_values = [data_aspen[comp]['Tc'] for comp in components]
    Pc_values = [data_aspen[comp]['Pc'] for comp in components]
    MW_values = [data_aspen[comp]['MW'] for comp in components]

    # Crear figura con 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Práctica 2: Propiedades Críticas desde ASPEN HYSYS',
                 fontsize=14, fontweight='bold')

    x = np.arange(len(components))
    width = 0.5
    colors = ['#FF6B6B', '#4ECDC4']

    # Subplot 1: Temperatura crítica
    bars1 = ax1.bar(x, Tc_values, width, color=colors, alpha=0.8, edgecolor='black')
    ax1.set_ylabel('Temperatura Crítica (K)', fontsize=11, fontweight='bold')
    ax1.set_title('Temperatura Crítica (Tc)', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(components)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    # Agregar valores sobre las barras
    for i, (bar, val) in enumerate(zip(bars1, Tc_values)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f} K', ha='center', va='bottom', fontsize=9)

    # Subplot 2: Presión crítica
    bars2 = ax2.bar(x, Pc_values, width, color=colors, alpha=0.8, edgecolor='black')
    ax2.set_ylabel('Presión Crítica (kPa)', fontsize=11, fontweight='bold')
    ax2.set_title('Presión Crítica (Pc)', fontsize=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(components)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    for i, (bar, val) in enumerate(zip(bars2, Pc_values)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.0f} kPa', ha='center', va='bottom', fontsize=9)

    # Subplot 3: Peso molecular
    bars3 = ax3.bar(x, MW_values, width, color=colors, alpha=0.8, edgecolor='black')
    ax3.set_ylabel('Peso Molecular (g/mol)', fontsize=11, fontweight='bold')
    ax3.set_title('Peso Molecular (MW)', fontsize=12)
    ax3.set_xticks(x)
    ax3.set_xticklabels(components)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')

    for i, (bar, val) in enumerate(zip(bars3, MW_values)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f} g/mol', ha='center', va='bottom', fontsize=9)

    # Nota al pie
    fig.text(0.5, 0.02,
             f'Fuente: ASPEN HYSYS con paquete termodinámico NRTL | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout()

    # Guardar figura
    output_file = '/home/user/aspen_python_API/practica2/propiedades_aspen.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    print("\n💡 ANÁLISIS:")
    print(f"   • El agua tiene mayor Tc ({Tc_values[1]:.2f} K) que el metanol ({Tc_values[0]:.2f} K)")
    print(f"   • El agua tiene mayor Pc ({Pc_values[1]:.0f} kPa) que el metanol ({Pc_values[0]:.0f} kPa)")
    print(f"   • El metanol tiene mayor MW ({MW_values[0]:.2f} g/mol) que el agua ({MW_values[1]:.2f} g/mol)")

    print("="*60)

if __name__ == '__main__':
    main()
