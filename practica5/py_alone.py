#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 5: Reactor CSTR con Conversión Fija (Python Puro)
===========================================================

Este script calcula el comportamiento de un reactor CSTR con conversión fija
usando balance de materia estequiométrico en Python puro.

Reacción: Methanol + Triglicérido → Biodiesel + Glicerol

Autor: Salas-García, et. al
Fecha: 2025-01-15
import os
"""

import numpy as np
import json

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 5: REACTOR CSTR - CONVERSIÓN FIJA (PYTHON)")
    print("="*60)

    # PASO 1: Especificaciones de entrada
    print("\n[1/4] Especificaciones de alimentación...")

    # Condiciones de entrada
    F_feed = 100.0  # kgmole/h (flujo total)
    T_feed = 60.0   # °C
    P_feed = 101.325  # kPa

    # Composición de alimentación
    x_Methanol_in = 0.60  # Exceso
    x_Ethanol_in = 0.40   # Triglicérido (reactivo limitante)
    x_Biodiesel_in = 0.0
    x_Glycerol_in = 0.0

    print(f"\n   Alimentación:")
    print(f"      F_total = {F_feed:.2f} kgmole/h")
    print(f"      T = {T_feed:.2f} °C")
    print(f"      x(Methanol) = {x_Methanol_in:.4f}")
    print(f"      x(Ethanol/Triglicérido) = {x_Ethanol_in:.4f}")

    # Flujos molares de entrada
    F_Methanol_in = F_feed * x_Methanol_in
    F_Ethanol_in = F_feed * x_Ethanol_in

    print(f"\n   Flujos molares de entrada:")
    print(f"      F(Methanol) = {F_Methanol_in:.2f} kgmole/h")
    print(f"      F(Ethanol) = {F_Ethanol_in:.2f} kgmole/h")

    # PASO 2: Configuración de reacción y conversión
    print("\n[2/4] Configuración de reacción química...")

    # Estequiometría: Methanol + Ethanol → Biodiesel + Glycerol
    # Coeficientes estequiométricos (negativos reactivos, positivos productos)
    nu_Methanol = -1.0
    nu_Ethanol = -1.0
    nu_Biodiesel = 1.0
    nu_Glycerol = 1.0

    print(f"\n   Estequiometría:")
    print(f"      Methanol + Ethanol → Biodiesel + Glycerol")
    print(f"      Coeficientes: {nu_Methanol}, {nu_Ethanol}, {nu_Biodiesel}, {nu_Glycerol}")

    # Conversión especificada (basada en Ethanol/Triglicérido)
    conversion = 0.85  # 85%

    print(f"\n   Conversión especificada: {conversion*100:.1f}%")
    print(f"   (basada en Ethanol/Triglicérido)")

    # PASO 3: Balance de materia con reacción
    print("\n[3/4] Calculando balance de materia...")

    # Cálculo de extent de reacción (ξ)
    # Para componente i: F_i_out = F_i_in + nu_i * ξ
    # Conversión X = ξ / F_limitante_in
    # Por lo tanto: ξ = X * F_limitante_in

    xi = conversion * F_Ethanol_in  # kgmole/h (extent de reacción)

    print(f"\n   Extent de reacción (ξ): {xi:.2f} kgmole/h")

    # Cálculo de flujos de salida
    F_Methanol_out = F_Methanol_in + nu_Methanol * xi
    F_Ethanol_out = F_Ethanol_in + nu_Ethanol * xi
    F_Biodiesel_out = 0.0 + nu_Biodiesel * xi
    F_Glycerol_out = 0.0 + nu_Glycerol * xi

    # Flujo total de salida
    F_total_out = F_Methanol_out + F_Ethanol_out + F_Biodiesel_out + F_Glycerol_out

    print(f"\n   Flujos de salida:")
    print(f"      F(Methanol) = {F_Methanol_out:.2f} kgmole/h")
    print(f"      F(Ethanol) = {F_Ethanol_out:.2f} kgmole/h")
    print(f"      F(Biodiesel) = {F_Biodiesel_out:.2f} kgmole/h")
    print(f"      F(Glycerol) = {F_Glycerol_out:.2f} kgmole/h")
    print(f"      F_total = {F_total_out:.2f} kgmole/h")

    # Composiciones de salida
    x_Methanol_out = F_Methanol_out / F_total_out
    x_Ethanol_out = F_Ethanol_out / F_total_out
    x_Biodiesel_out = F_Biodiesel_out / F_total_out
    x_Glycerol_out = F_Glycerol_out / F_total_out

    print(f"\n   Composiciones de salida:")
    print(f"      x(Methanol) = {x_Methanol_out:.4f}")
    print(f"      x(Ethanol) = {x_Ethanol_out:.4f}")
    print(f"      x(Biodiesel) = {x_Biodiesel_out:.4f}")
    print(f"      x(Glycerol) = {x_Glycerol_out:.4f}")
    print(f"      Σx = {x_Methanol_out + x_Ethanol_out + x_Biodiesel_out + x_Glycerol_out:.4f} ✓")

    # PASO 4: Análisis de rendimiento
    print("\n[4/4] Análisis de rendimiento del reactor...")

    # Verificación de conversión
    conversion_check = (F_Ethanol_in - F_Ethanol_out) / F_Ethanol_in
    print(f"\n   Verificación de conversión:")
    print(f"      Conversión calculada: {conversion_check*100:.2f}%")
    print(f"      Conversión especificada: {conversion*100:.2f}%")

    # Rendimiento de productos
    yield_biodiesel = F_Biodiesel_out / F_Ethanol_in * 100  # % basado en Ethanol
    print(f"\n   Rendimiento:")
    print(f"      Biodiesel producido: {F_Biodiesel_out:.2f} kgmole/h")
    print(f"      Rendimiento: {yield_biodiesel:.2f}%")

    # Selectividad (en reacción única = 100%)
    selectivity = 100.0
    print(f"      Selectividad: {selectivity:.1f}% (reacción única)")

    # Guardar resultados
    results = {
        'reactor_type': 'CSTR con conversión fija (Python)',
        'conversion_specified': conversion * 100,
        'alimentacion': {
            'T_C': T_feed,
            'P_kPa': P_feed,
            'F_kgmoleh': F_feed,
            'x_Methanol': x_Methanol_in,
            'x_Ethanol': x_Ethanol_in,
            'x_Biodiesel': x_Biodiesel_in,
            'x_Glycerol': x_Glycerol_in
        },
        'salida': {
            'T_C': T_feed,  # Asumimos isotérmico
            'P_kPa': P_feed,  # Asumimos isobárico
            'F_kgmoleh': F_total_out,
            'x_Methanol': x_Methanol_out,
            'x_Ethanol': x_Ethanol_out,
            'x_Biodiesel': x_Biodiesel_out,
            'x_Glycerol': x_Glycerol_out
        },
        'analisis': {
            'extent_reaccion': xi,
            'conversion_alcanzada': conversion_check * 100,
            'rendimiento_biodiesel': yield_biodiesel,
            'selectividad': selectivity
        }
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'resultados_python.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n   ✓ Resultados guardados: resultados_python.json")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 5 (PYTHON PURO) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA:")
    print("   ✓ Balance de materia: F_i_out = F_i_in + ν_i·ξ")
    print("   ✓ Extent de reacción: ξ = X · F_limitante")
    print("   ✓ Conversión: X = (F_in - F_out) / F_in")
    print("   ✓ Rendimiento: moles producto / moles reactivo teórico")
    print("   ✓ Selectividad: producto deseado / total productos")

    print("\n📊 VENTAJAS DE CONVERSIÓN FIJA:")
    print("   + Simple para diseño preliminar")
    print("   + No requiere parámetros cinéticos")
    print("   + Útil para análisis de factibilidad")
    print("   - No predice tamaño del reactor")
    print("   - No considera efectos de temperatura")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Compara con resultados de aspython.py")
    print("   2. Ejecuta visualiza1.py y visualiza2.py")
    print("   3. Experimenta con diferentes conversiones")
    print("   4. Continúa con Práctica 6: Cinética de Arrhenius")

    print("="*60)

if __name__ == '__main__':
    main()
