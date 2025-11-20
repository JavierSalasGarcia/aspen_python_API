#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 4: Mezclador - Balance de Materia y Energía (Python Puro)
===================================================================

Este script realiza balances de materia y energía para un mezclador
usando Python puro, sin ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import os
import numpy as np
import json

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 4: MEZCLADOR (PYTHON PURO)")
    print("="*60)

    # PASO 1: Especificaciones de entrada
    print("\n[1/4] Especificaciones de corrientes de entrada...")

    # Corriente 1: Metanol puro
    F1 = 50.0  # kgmole/h
    T1 = 25.0  # °C
    P1 = 101.325  # kPa
    x1_Methanol = 1.0
    x1_Water = 0.0

    # Corriente 2: Agua pura
    F2 = 30.0  # kgmole/h
    T2 = 30.0  # °C
    P2 = 101.325  # kPa
    x2_Methanol = 0.0
    x2_Water = 1.0

    print(f"\n   Corriente 1: Metanol puro")
    print(f"      F = {F1:.2f} kgmole/h")
    print(f"      T = {T1:.2f} °C")
    print(f"      x(Methanol) = {x1_Methanol:.2f}")

    print(f"\n   Corriente 2: Agua pura")
    print(f"      F = {F2:.2f} kgmole/h")
    print(f"      T = {T2:.2f} °C")
    print(f"      x(Water) = {x2_Water:.2f}")

    # PASO 2: Balance de materia global
    print("\n[2/4] Balance de materia...")

    F_total = F1 + F2
    print(f"\n   Balance global:")
    print(f"      F_salida = F1 + F2 = {F1:.2f} + {F2:.2f} = {F_total:.2f} kgmole/h")

    # Balance por componente
    F_Methanol = F1 * x1_Methanol + F2 * x2_Methanol
    F_Water = F1 * x1_Water + F2 * x2_Water

    x_out_Methanol = F_Methanol / F_total
    x_out_Water = F_Water / F_total

    print(f"\n   Balance por componente:")
    print(f"      Methanol: {F_Methanol:.2f} kgmole/h (x = {x_out_Methanol:.4f})")
    print(f"      Water: {F_Water:.2f} kgmole/h (x = {x_out_Water:.4f})")
    print(f"      Suma de fracciones: {x_out_Methanol + x_out_Water:.4f} ✓")

    # PASO 3: Balance de energía (simplificado)
    print("\n[3/4] Balance de energía (temperatura de mezcla)...")

    # Propiedades (valores aproximados)
    Cp_Methanol = 81.6  # J/(mol·K)
    Cp_Water = 75.3  # J/(mol·K)

    # Temperatura de mezcla (asumiendo mezcla adiabática)
    # F1*Cp1*(T_out - T1) + F2*Cp2*(T_out - T2) = 0
    # Simplificación: Cp promedio
    Cp_avg = x_out_Methanol * Cp_Methanol + x_out_Water * Cp_Water

    # Balance: suma de entalpías
    T_out = (F1 * Cp_Methanol * T1 + F2 * Cp_Water * T2) / (F1 * Cp_Methanol + F2 * Cp_Water)

    print(f"\n   Temperatura de salida (mezcla adiabática):")
    print(f"      T_salida ≈ {T_out:.2f} °C")
    print(f"      (Calculada asumiendo mezcla ideal, sin calor de mezcla)")

    # PASO 4: Estimación de densidad de la mezcla
    print("\n[4/4] Estimando densidad de la mezcla...")

    # Densidades puras a 25°C (aproximadas)
    rho_Methanol_25C = 786.5  # kg/m³
    rho_Water_25C = 997.0  # kg/m³

    # Pesos moleculares
    MW_Methanol = 32.04  # g/mol
    MW_Water = 18.015  # g/mol

    # Fracción másica
    w_Methanol = (x_out_Methanol * MW_Methanol) / (x_out_Methanol * MW_Methanol + x_out_Water * MW_Water)
    w_Water = 1 - w_Methanol

    # Densidad de mezcla (aproximación lineal en volumen)
    # 1/rho_mix = w1/rho1 + w2/rho2
    rho_mix = 1 / (w_Methanol / rho_Methanol_25C + w_Water / rho_Water_25C)

    print(f"      Fracción másica Methanol: {w_Methanol:.4f}")
    print(f"      Densidad estimada: {rho_mix:.2f} kg/m³")

    # Guardar resultados
    results = {
        'entrada1': {
            'F_kgmoleh': F1,
            'T_C': T1,
            'P_kPa': P1,
            'x_Methanol': x1_Methanol,
            'x_Water': x1_Water
        },
        'entrada2': {
            'F_kgmoleh': F2,
            'T_C': T2,
            'P_kPa': P2,
            'x_Methanol': x2_Methanol,
            'x_Water': x2_Water
        },
        'salida': {
            'F_kgmoleh': F_total,
            'T_C': T_out,
            'P_kPa': P1,  # Asumimos presión constante
            'x_Methanol': x_out_Methanol,
            'x_Water': x_out_Water,
            'density_kgm3': rho_mix
        },
        'method': 'Python puro (balances analíticos)'
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'resultados_python.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n   ✓ Resultados guardados: resultados_python.json")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 4 (PYTHON PURO) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE:")
    print("   ✓ Balance de materia: conservación de masa")
    print("   ✓ Balance de energía: conservación de energía")
    print("   ✓ Composición = promedio ponderado por flujo molar")
    print("   ✓ Python puede resolver balances sin ASPEN")

    print("\n📊 LIMITACIONES:")
    print("   • No incluye calor de mezcla (no ideal)")
    print("   • Densidad es aproximación (no rigurosa)")
    print("   • ASPEN usa modelos termodinámicos más precisos (NRTL)")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Compara con resultados de aspython.py")
    print("   2. Ejecuta visualiza1.py y visualiza2.py")
    print("   3. Observa diferencias por efectos no ideales")

    print("="*60)

if __name__ == '__main__':
    main()
