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
import sys

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
        print(f"   Tipo de error: {type(e).__name__}")
        print(f"   Detalles: {e}")

        # Diagnóstico específico según el tipo de error
        if hasattr(e, 'args') and len(e.args) > 0:
            error_code = e.args[0] if isinstance(e.args[0], int) else None

            if error_code == -2147221021:
                print("\n   ❌ ERROR IDENTIFICADO: HYSYS no está registrado en el sistema")
                print("\n   🔧 SOLUCIONES:")
                print("   1. Verifica que HYSYS esté instalado correctamente")
                print("   2. Abre HYSYS manualmente como administrador (clic derecho → Ejecutar como administrador)")
                print("   3. Verifica la compatibilidad de arquitectura:")
                arch = "64-bit" if sys.maxsize > 2**32 else "32-bit"
                print(f"      • Tu Python es: {arch}")
                print(f"      • Tu HYSYS debe ser: {arch}")
                print("   4. Ejecuta el script de diagnóstico:")
                print("      python diagnostico_hysys.py")
            elif error_code == -2147221005:
                print("\n   ❌ ERROR: Clase COM no registrada")
                print("\n   🔧 SOLUCIONES:")
                print("   1. Reinstala o repara HYSYS")
                print("   2. Verifica que tienes permisos de administrador")
            else:
                print(f"\n   Código de error COM: {error_code}")

        print("\n   📋 CAUSAS COMUNES:")
        print("   • HYSYS no está instalado")
        print("   • Incompatibilidad Python 32-bit vs HYSYS 64-bit (o viceversa)")
        print("   • HYSYS no se ha ejecutado nunca como administrador")
        print("   • No hay licencia activa de HYSYS")
        print("   • pywin32 no está instalado (pip install pywin32)")

        print("\n   💡 ALTERNATIVA: Método con HYSYS ya abierto")
        print("   Si HYSYS funciona manualmente, prueba:")
        print("   1. Abre HYSYS manualmente")
        print("   2. Ejecuta aspython_activeobject.py")

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
