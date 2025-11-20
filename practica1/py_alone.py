#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1: Información del Sistema Python (Sin ASPEN)
=======================================================

Este script demuestra cómo obtener información del sistema usando Python puro,
sin necesidad de ASPEN HYSYS. Muestra información sobre Python, sistema operativo
y librerías instaladas.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""
import os

import sys
import platform
import time

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 1: INFORMACIÓN DEL SISTEMA (PYTHON PURO)")
    print("="*60)

    # PASO 1: Información de Python
    print("\n[1/4] Información de Python...")
    print(f"   ✓ Versión de Python: {sys.version.split()[0]}")
    print(f"   ✓ Implementación: {platform.python_implementation()}")
    print(f"   ✓ Compilador: {platform.python_compiler()}")

    # PASO 2: Información del Sistema Operativo
    print("\n[2/4] Información del Sistema Operativo...")
    print(f"   ✓ Sistema: {platform.system()}")
    print(f"   ✓ Versión: {platform.version()}")
    print(f"   ✓ Arquitectura: {platform.machine()}")
    print(f"   ✓ Procesador: {platform.processor()}")

    # PASO 3: Verificar librerías necesarias
    print("\n[3/4] Verificando librerías científicas...")

    libraries = {
        'numpy': 'Cálculos numéricos',
        'matplotlib': 'Visualización de datos',
        'thermo': 'Propiedades termodinámicas',
        'chemicals': 'Base de datos química',
        'scipy': 'Cálculos científicos'
    }

    for lib, description in libraries.items():
        try:
            module = __import__(lib)
            version = getattr(module, '__version__', 'versión no disponible')
            print(f"   ✓ {lib:12s} ({version:8s}) - {description}")
        except ImportError:
            print(f"   ✗ {lib:12s} (no instalada) - {description}")

    # PASO 4: Comparación con ASPEN
    print("\n[4/4] Comparación Python vs ASPEN HYSYS...")
    print("   Python puro:")
    print("     + Multiplataforma (Windows, Linux, Mac)")
    print("     + No requiere licencia comercial")
    print("     + Velocidad en cálculos simples")
    print("     - Limitado para equipos complejos")

    print("   ASPEN HYSYS:")
    print("     + Modelos termodinámicos validados")
    print("     + Simulación de equipos complejos")
    print("     + Estándar industrial")
    print("     - Requiere Windows y licencia")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 1 (PYTHON PURO) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE:")
    print("   ✓ Python puede obtener información del sistema")
    print("   ✓ Existen librerías científicas potentes")
    print("   ✓ Cada enfoque tiene ventajas y limitaciones")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Instala las librerías faltantes")
    print("   2. Compara con aspython.py de esta práctica")
    print("   3. Ejecuta visualiza1.py y visualiza2.py")

    print("="*60)

if __name__ == '__main__':
    main()
