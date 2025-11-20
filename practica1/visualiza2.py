#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1: Visualización de Información del Sistema (Python Puro)
===================================================================

Este script genera visualizaciones de la información obtenida usando Python puro,
sin ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import platform
from datetime import datetime
import os

def main():
    """Genera visualización de la práctica 1 (Python puro)"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 1 - PYTHON PURO")
    print("="*60)

    # Crear figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    fig.suptitle('Práctica 1: Información del Sistema (Python Puro)',
                 fontsize=16, fontweight='bold')

    # ========== Subplot 1: Información de Python ==========
    ax1.axis('off')
    ax1.set_title('Entorno Python', fontsize=12, fontweight='bold', pad=20)

    # Verificar librerías
    libraries = ['numpy', 'matplotlib', 'thermo', 'chemicals', 'scipy']
    installed = []
    not_installed = []

    for lib in libraries:
        try:
            __import__(lib)
            installed.append(lib)
        except ImportError:
            not_installed.append(lib)

    # Python info box
    python_info = f"""
    Versión: {sys.version.split()[0]}
    Implementación: {platform.python_implementation()}
    Sistema: {platform.system()}
    Arquitectura: {platform.machine()}

    Librerías instaladas: {len(installed)}/{len(libraries)}
    """

    ax1.text(0.5, 0.7, python_info, fontsize=10, ha='center', va='top',
             family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    # Librerías
    libs_text = "Librerías disponibles:\n" + "\n".join([f"✓ {lib}" for lib in installed])
    if not_installed:
        libs_text += "\n\nFaltantes:\n" + "\n".join([f"✗ {lib}" for lib in not_installed])

    ax1.text(0.5, 0.35, libs_text, fontsize=9, ha='center', va='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ========== Subplot 2: Comparación ==========
    ax2.axis('off')
    ax2.set_title('Python vs ASPEN', fontsize=12, fontweight='bold', pad=20)

    # Tabla comparativa
    comparison_data = [
        ['Aspecto', 'Python Puro', 'ASPEN HYSYS'],
        ['Licencia', 'Libre', 'Comercial'],
        ['Plataforma', 'Multiplataforma', 'Solo Windows'],
        ['Termodinámica', 'Básica', 'Avanzada'],
        ['Equipos', 'Limitado', 'Completo'],
        ['Velocidad', 'Alta', 'Media'],
        ['Uso recomendado', 'Cálculos simples', 'Simulación rigurosa']
    ]

    # Crear tabla
    table = ax2.table(cellText=comparison_data, cellLoc='left',
                      loc='center', bbox=[0.05, 0.1, 0.9, 0.8])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Colorear encabezado
    for i in range(3):
        cell = table[(0, i)]
        cell.set_facecolor('lightgray')
        cell.set_text_props(weight='bold')

    # Colorear columnas
    for i in range(1, len(comparison_data)):
        table[(i, 1)].set_facecolor('lightblue')
        table[(i, 2)].set_facecolor('lightcoral')

    # Conclusión
    conclusion = """
    Conclusión: Python puro es excelente para cálculos rápidos
    y análisis de datos, mientras que ASPEN HYSYS es necesario
    para simulaciones rigurosas de procesos industriales.
    La combinación de ambos (aspython.py) aprovecha lo mejor
    de cada herramienta.
    """

    fig.text(0.5, 0.02, conclusion, ha='center', fontsize=9, style='italic',
             wrap=True, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

    plt.tight_layout()

    # Guardar figura
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'resultados_python.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    print("="*60)

if __name__ == '__main__':
    main()
