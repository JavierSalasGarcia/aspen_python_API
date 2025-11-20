#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico para ASPEN HYSYS
=======================================

Este script verifica la instalación y configuración de ASPEN HYSYS
para ayudar a solucionar problemas de conexión COM.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import sys
import os

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title):
    """Imprime un título de sección"""
    print(f"\n[{title}]")
    print("-"*70)

def check_python_version():
    """Verifica la versión de Python"""
    print_section("1. VERIFICACIÓN DE PYTHON")
    print(f"✓ Python {sys.version}")
    print(f"✓ Arquitectura: {sys.maxsize > 2**32 and '64-bit' or '32-bit'}")

    if sys.maxsize <= 2**32:
        print("\n⚠️  ADVERTENCIA: Estás usando Python 32-bit")
        print("   Si HYSYS es 64-bit, necesitas Python 64-bit")

def check_pywin32():
    """Verifica la instalación de pywin32"""
    print_section("2. VERIFICACIÓN DE PYWIN32")

    try:
        import win32com.client
        import pythoncom
        print("✓ win32com.client importado correctamente")
        print("✓ pythoncom importado correctamente")

        try:
            import win32api
            print(f"✓ pywin32 build: {win32api.GetFileVersionInfo(win32api.__file__, '\\\\')}")
        except:
            print("✓ pywin32 instalado (versión no disponible)")

        return True
    except ImportError as e:
        print(f"✗ ERROR: pywin32 no está instalado correctamente")
        print(f"  Detalles: {e}")
        print("\n  SOLUCIÓN:")
        print("  pip install pywin32")
        print("  python -m win32com.client.makepy")
        return False

def check_hysys_registry():
    """Verifica el registro de Windows para HYSYS"""
    print_section("3. VERIFICACIÓN DEL REGISTRO DE WINDOWS")

    try:
        import winreg

        # Posibles ubicaciones de HYSYS en el registro
        possible_keys = [
            (winreg.HKEY_CLASSES_ROOT, "HYSYS.Application"),
            (winreg.HKEY_CLASSES_ROOT, "HYSYS.Application.1"),
            (winreg.HKEY_CLASSES_ROOT, "Hysys.Application"),
            (winreg.HKEY_CLASSES_ROOT, "Hysys.SimulationCase"),
        ]

        found = False
        for hkey, subkey in possible_keys:
            try:
                key = winreg.OpenKey(hkey, subkey)
                print(f"✓ Encontrado: {subkey}")
                winreg.CloseKey(key)
                found = True
            except WindowsError:
                print(f"  No encontrado: {subkey}")

        if not found:
            print("\n✗ PROBLEMA DETECTADO: HYSYS no está registrado en el sistema")
            print("\n  POSIBLES CAUSAS:")
            print("  1. HYSYS no está instalado")
            print("  2. HYSYS necesita ser reparado/reinstalado")
            print("  3. Necesitas ejecutar HYSYS al menos una vez como administrador")
            return False

        return True

    except ImportError:
        print("✗ No se puede acceder al registro (winreg no disponible)")
        return False

def try_hysys_connection():
    """Intenta conectar con HYSYS usando diferentes métodos"""
    print_section("4. INTENTOS DE CONEXIÓN CON HYSYS")

    try:
        import win32com.client
        import pythoncom
    except ImportError:
        print("✗ No se puede continuar: pywin32 no disponible")
        return False

    # Método 1: Dispatch estándar
    print("\nMétodo 1: win32.Dispatch('HYSYS.Application')")
    try:
        hysys = win32com.client.Dispatch('HYSYS.Application')
        print("✓ ÉXITO: Conexión establecida con HYSYS")
        try:
            version = hysys.Version
            print(f"✓ Versión de HYSYS: {version}")
        except:
            pass
        try:
            hysys.Quit()
        except:
            pass
        return True
    except Exception as e:
        print(f"✗ FALLÓ: {e}")
        print(f"  Código de error: {e.args[0] if e.args else 'desconocido'}")

    # Método 2: Dispatch con ProgID alternativo
    print("\nMétodo 2: win32.Dispatch('Hysys.Application')")
    try:
        hysys = win32com.client.Dispatch('Hysys.Application')
        print("✓ ÉXITO: Conexión establecida con HYSYS (ProgID alternativo)")
        try:
            hysys.Quit()
        except:
            pass
        return True
    except Exception as e:
        print(f"✗ FALLÓ: {e}")

    # Método 3: DispatchEx
    print("\nMétodo 3: win32.DispatchEx('HYSYS.Application')")
    try:
        hysys = win32com.client.DispatchEx('HYSYS.Application')
        print("✓ ÉXITO: Conexión establecida con HYSYS (DispatchEx)")
        try:
            hysys.Quit()
        except:
            pass
        return True
    except Exception as e:
        print(f"✗ FALLÓ: {e}")

    # Método 4: GetActiveObject (si HYSYS ya está ejecutándose)
    print("\nMétodo 4: GetActiveObject('HYSYS.Application')")
    print("  (Este método solo funciona si HYSYS ya está abierto)")
    try:
        hysys = win32com.client.GetActiveObject('HYSYS.Application')
        print("✓ ÉXITO: Conectado a instancia existente de HYSYS")
        return True
    except Exception as e:
        print(f"✗ FALLÓ: {e}")
        print("  (Esto es normal si HYSYS no está ejecutándose)")

    return False

def print_solutions():
    """Imprime soluciones comunes"""
    print_section("SOLUCIONES RECOMENDADAS")

    print("\n📋 PASOS PARA SOLUCIONAR EL PROBLEMA:")
    print("\n1. VERIFICAR INSTALACIÓN DE HYSYS")
    print("   • Asegúrate de que HYSYS está instalado correctamente")
    print("   • Verifica que tienes una licencia activa")
    print("   • Intenta abrir HYSYS manualmente")

    print("\n2. VERIFICAR COMPATIBILIDAD DE ARQUITECTURA")
    print("   • Si HYSYS es 64-bit, Python debe ser 64-bit")
    print("   • Si HYSYS es 32-bit, Python debe ser 32-bit")
    print("   • NO PUEDEN SER DIFERENTES")

    print("\n3. REPARAR REGISTRO DE HYSYS")
    print("   • Ejecuta HYSYS como administrador al menos una vez")
    print("   • Considera reparar la instalación de HYSYS")

    print("\n4. REINSTALAR PYWIN32")
    print("   • pip uninstall pywin32")
    print("   • pip install pywin32")
    print("   • python -m win32com.client.makepy")

    print("\n5. MÉTODO ALTERNATIVO: HYSYS YA ABIERTO")
    print("   • Abre HYSYS manualmente")
    print("   • Luego ejecuta el script modificado que usa GetActiveObject()")

def main():
    """Función principal de diagnóstico"""
    print_header("DIAGNÓSTICO DE ASPEN HYSYS - SOLUCIÓN DE PROBLEMAS")

    print("\nEste script verificará:")
    print("  • Versión de Python y arquitectura")
    print("  • Instalación de pywin32")
    print("  • Registro de HYSYS en Windows")
    print("  • Diferentes métodos de conexión COM")

    input("\nPresiona ENTER para comenzar el diagnóstico...")

    # Ejecutar verificaciones
    check_python_version()

    pywin32_ok = check_pywin32()
    if not pywin32_ok:
        print_solutions()
        return

    hysys_registered = check_hysys_registry()
    hysys_connected = try_hysys_connection()

    # Resultado final
    print_section("RESUMEN DEL DIAGNÓSTICO")

    if hysys_connected:
        print("\n✓✓✓ ¡EXCELENTE! HYSYS está funcionando correctamente")
        print("    Puedes ejecutar aspython.py sin problemas")
    elif not hysys_registered:
        print("\n✗✗✗ PROBLEMA: HYSYS no está registrado correctamente")
        print("    Necesitas revisar la instalación de HYSYS")
    else:
        print("\n⚠️⚠️⚠️ PROBLEMA: HYSYS está instalado pero no se puede conectar")
        print("    Revisa la compatibilidad de arquitectura (32/64-bit)")

    print_solutions()

    print("\n" + "="*70)
    print("DIAGNÓSTICO COMPLETADO")
    print("="*70)

if __name__ == '__main__':
    main()
