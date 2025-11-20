#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1 (Alternativa): Conexión con HYSYS ya abierto
========================================================

Este script es una ALTERNATIVA para cuando no puedes abrir HYSYS desde Python.
En lugar de crear una nueva instancia, se conecta a HYSYS si ya está abierto.

INSTRUCCIONES:
1. Abre ASPEN HYSYS manualmente ANTES de ejecutar este script
2. Ejecuta este script
3. El script se conectará a la instancia ya abierta

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import win32com.client as win32
import time

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 1: CONEXIÓN CON HYSYS YA ABIERTO")
    print("="*60)

    # PASO 0: Verificar que HYSYS esté abierto
    print("\n[0/4] Verificando que HYSYS esté abierto...")
    print("   ⚠️  IMPORTANTE: Asegúrate de que HYSYS esté abierto")

    input("   Presiona ENTER cuando HYSYS esté abierto...")

    # PASO 1: Conectar con HYSYS existente
    print("\n[1/4] Conectando con HYSYS existente...")

    try:
        # Conectar a instancia existente de HYSYS
        hysys = win32.GetActiveObject('HYSYS.Application')
        print("   ✓ Conectado a HYSYS existente")

    except Exception as e:
        print(f"   ✗ ERROR: No se pudo conectar con HYSYS")
        print(f"   Detalles: {e}")
        print("\n   Posibles causas:")
        print("   - HYSYS no está abierto (ábrelo manualmente primero)")
        print("   - pywin32 no está instalado (pip install pywin32)")
        print("\n   💡 PRUEBA TAMBIÉN:")
        print("   - Intenta con diferentes ProgIDs:")
        print("     • 'HYSYS.Application'")
        print("     • 'Hysys.Application'")
        print("     • 'HYSYS.Application.1'")

        # Intentar con ProgID alternativo
        print("\n   Intentando con ProgID alternativo...")
        try:
            hysys = win32.GetActiveObject('Hysys.Application')
            print("   ✓ ¡Éxito con ProgID alternativo!")
        except:
            print("   ✗ Tampoco funcionó con ProgID alternativo")
            return

    # PASO 2: Obtener información de HYSYS
    print("\n[2/4] Obteniendo información del sistema...")

    try:
        version = hysys.Version
        print(f"   ✓ HYSYS Versión: {version}")

    except Exception as e:
        print(f"   ⚠ No se pudo obtener versión: {e}")

    # PASO 3: Verificar si hay simulaciones abiertas
    print("\n[3/4] Verificando simulaciones abiertas...")

    try:
        sim_count = hysys.SimulationCases.Count
        print(f"   ✓ Simulaciones abiertas: {sim_count}")

        if sim_count > 0:
            print("\n   Detalles de simulaciones:")
            for i in range(sim_count):
                sim = hysys.SimulationCases.Item(i)
                try:
                    print(f"   • Simulación {i+1}: {sim.Title}")
                except:
                    print(f"   • Simulación {i+1}: (sin título)")

    except Exception as e:
        print(f"   ⚠ No se pudo obtener información de simulaciones: {e}")

    # PASO 4: Información final
    print("\n[4/4] Información importante...")
    print("   ℹ️  Este script NO cerrará HYSYS")
    print("   ℹ️  Cierra HYSYS manualmente cuando termines")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 1 (ALTERNATIVA) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE APRENDIDOS:")
    print("   ✓ GetActiveObject() → Conectar a instancia existente")
    print("   ✓ Diferencia con Dispatch() → No crea nueva instancia")
    print("   ✓ hysys.SimulationCases → Acceder a casos abiertos")

    print("\n🔄 VENTAJAS DE ESTE MÉTODO:")
    print("   ✓ Funciona incluso si Dispatch() falla")
    print("   ✓ Útil para debugging y desarrollo")
    print("   ✓ Permite trabajar con simulaciones ya abiertas")

    print("\n⚠️  DESVENTAJAS:")
    print("   • Requiere abrir HYSYS manualmente primero")
    print("   • No es automático para scripts de producción")

    print("\n🎯 OBJETIVO FINAL:")
    print("   Idealmente, deberías poder usar Dispatch() en aspython.py")
    print("   Este método es solo una ALTERNATIVA temporal")

    print("\n" + "="*60)

if __name__ == '__main__':
    main()
