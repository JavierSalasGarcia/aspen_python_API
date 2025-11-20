#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1: Visualización de Información del Sistema (ASPEN)
=============================================================

Este script genera visualizaciones de la información obtenida de ASPEN HYSYS.
Para la práctica 1, muestra información básica sobre la conexión.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import os

def main():
    """Genera visualización de la práctica 1 (ASPEN)"""

    print("="*60)
    print("VISUALIZACIÓN: PRÁCTICA 1 - CONEXIÓN CON ASPEN")
    print("="*60)

    # Crear figura con información visual
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    # Título
    fig.suptitle('Práctica 1: Conexión Python ↔ ASPEN HYSYS',
                 fontsize=16, fontweight='bold', y=0.95)

    # Diagrama de flujo de conexión
    # Python box
    python_box = mpatches.FancyBboxPatch((0.1, 0.6), 0.25, 0.2,
                                         boxstyle="round,pad=0.02",
                                         edgecolor='blue', facecolor='lightblue',
                                         linewidth=2)
    ax.add_patch(python_box)
    ax.text(0.225, 0.7, 'Python Script\n(aspython.py)',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # COM API arrow
    ax.annotate('', xy=(0.45, 0.7), xytext=(0.35, 0.7),
                arrowprops=dict(arrowstyle='->', lw=2, color='green'))
    ax.text(0.4, 0.75, 'COM API', ha='center', fontsize=9, color='green')

    # HYSYS box
    hysys_box = mpatches.FancyBboxPatch((0.45, 0.6), 0.25, 0.2,
                                        boxstyle="round,pad=0.02",
                                        edgecolor='red', facecolor='lightcoral',
                                        linewidth=2)
    ax.add_patch(hysys_box)
    ax.text(0.575, 0.7, 'ASPEN HYSYS\n(Application)',
            ha='center', va='center', fontsize=11, fontweight='bold')

    # Return arrow
    ax.annotate('', xy=(0.35, 0.65), xytext=(0.45, 0.65),
                arrowprops=dict(arrowstyle='->', lw=2, color='orange'))
    ax.text(0.4, 0.62, 'Datos', ha='center', fontsize=9, color='orange')

    # Pasos realizados
    steps_text = """
    Pasos realizados en aspython.py:

    1. Importar win32com.client
    2. Dispatch('HYSYS.Application')
    3. Configurar Visible = True
    4. Obtener Version
    5. Cerrar con Quit()
    """

    ax.text(0.225, 0.35, steps_text, fontsize=10,
            verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Resultados
    results_text = """
    Información obtenida:

    ✓ Conexión exitosa
    ✓ Versión de HYSYS
    ✓ Control de visibilidad
    ✓ Cierre seguro
    """

    ax.text(0.575, 0.35, results_text, fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    # Fecha
    ax.text(0.5, 0.02, f'Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            ha='center', fontsize=8, style='italic', color='gray')

    plt.tight_layout()

    # Guardar figura (ruta relativa para funcionar en Windows y Linux)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'resultados_aspen.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfica guardada: {output_file}")

    # Mostrar
    plt.show()

    print("="*60)

if __name__ == '__main__':
    main()
