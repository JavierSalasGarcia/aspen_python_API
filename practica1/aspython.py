#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 1: Conexión Básica con ASPEN HYSYS
============================================

Este script demuestra cómo:
1. Conectar con ASPEN HYSYS desde Python
2. Obtener información del sistema
3. Cerrar HYSYS de forma segura

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import win32com.client as win32
import time

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 1: CONEXIÓN BÁSICA CON ASPEN HYSYS")
    print("="*60)

    # PASO 1: Iniciar ASPEN HYSYS
    print("\n[1/4] Iniciando ASPEN HYSYS...")

    try:
        # Crear objeto COM de HYSYS
        hysys = win32.Dispatch('HYSYS.Application')

        # Hacer HYSYS visible (cambiar a False para invisible)
        hysys.Visible = True

        print("   ✓ HYSYS iniciado correctamente")

    except Exception as e:
        print(f"   ✗ ERROR: No se pudo iniciar HYSYS")
        print(f"   Detalles: {e}")
        print("\n   Posibles causas:")
        print("   - HYSYS no está instalado")
        print("   - No hay licencia activa")
        print("   - pywin32 no está instalado (pip install pywin32)")
        return

    # PASO 2: Obtener información de HYSYS
    print("\n[2/4] Obteniendo información del sistema...")

    try:
        version = hysys.Version
        print(f"   ✓ HYSYS Versión: {version}")

    except Exception as e:
        print(f"   ⚠ No se pudo obtener versión: {e}")

    # PASO 3: Esperar para observar
    print("\n[3/4] HYSYS está abierto. Observa la ventana...")
    print("   ⏳ Esperando 3 segundos...")
    time.sleep(3)

    # PASO 4: Cerrar HYSYS
    print("\n[4/4] Cerrando ASPEN HYSYS...")

    try:
        hysys.Quit()
        print("   ✓ HYSYS cerrado correctamente")

    except Exception as e:
        print(f"   ⚠ Advertencia al cerrar: {e}")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 1 COMPLETADA EXITOSAMENTE")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE APRENDIDOS:")
    print("   ✓ win32com.client.Dispatch() → Crear conexión COM")
    print("   ✓ hysys.Visible = True/False → Controlar visibilidad")
    print("   ✓ hysys.Version → Obtener información del sistema")
    print("   ✓ hysys.Quit() → Cerrar HYSYS de forma segura")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Modifica Visible a False y ejecuta de nuevo")
    print("   2. Experimenta con try-except eliminando bloques")
    print("   3. Continúa con Práctica 2: Componentes")

    print("="*60)

if __name__ == '__main__':
    main()
