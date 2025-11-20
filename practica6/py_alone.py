#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 6: Cinética de Arrhenius en Reactor CSTR (Python Puro)
================================================================

Este script resuelve la ecuación de diseño de un CSTR con cinética de Arrhenius
usando scipy para análisis numérico.

Ecuación de Arrhenius: k = A·exp(-Ea/RT)
Diseño CSTR: V/F = X / (k·CA0·(1-X))  para cinética de 1er orden

Autor: Salas-García, et. al
import os
Fecha: 2025-01-15
"""

import numpy as np
import json
from scipy.optimize import fsolve

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 6: CINÉTICA DE ARRHENIUS (PYTHON + SCIPY)")
    print("="*60)

    # PASO 1: Parámetros cinéticos de Arrhenius
    print("\n[1/5] Definiendo parámetros cinéticos...")

    # Parámetros de Arrhenius
    A = 1.0e6   # Factor pre-exponencial (1/h)
    Ea = 60000  # Energía de activación (J/mol)
    R = 8.314   # Constante de gases (J/mol·K)

    print(f"   Ecuación de Arrhenius: k = A·exp(-Ea/RT)")
    print(f"      A = {A:.2e} 1/h")
    print(f"      Ea = {Ea:.0f} J/mol")
    print(f"      R = {R:.3f} J/(mol·K)")

    # PASO 2: Calcular k a diferentes temperaturas
    print("\n[2/5] Calculando constantes de velocidad vs temperatura...")

    temperatures = np.array([50, 60, 70, 80])  # °C
    k_values = {}

    print(f"\n   T (°C)    k (1/h)     Relativo a 50°C")
    print("   " + "-"*45)

    for T_celsius in temperatures:
        T_kelvin = T_celsius + 273.15
        k = A * np.exp(-Ea / (R * T_kelvin))
        k_values[float(T_celsius)] = float(k)

        if T_celsius == 50:
            k_ref = k
            ratio = 1.0
        else:
            ratio = k / k_ref

        print(f"   {T_celsius:5.0f}   {k:10.2e}   {ratio:8.2f}×")

    # PASO 3: Configuración del reactor CSTR
    print("\n[3/5] Configuración del reactor CSTR...")

    # Especificaciones
    V_reactor = 10.0  # m³
    F_feed = 100.0    # kgmole/h
    C_A0 = 1.0        # kgmole/m³ (concentración inicial asumida)
    T_operation = 60  # °C

    print(f"\n   Especificaciones del reactor:")
    print(f"      Volumen (V) = {V_reactor:.2f} m³")
    print(f"      Flujo de alimentación (F) = {F_feed:.2f} kgmole/h")
    print(f"      Concentración inicial (CA0) = {C_A0:.2f} kgmole/m³")
    print(f"      Temperatura de operación = {T_operation} °C")

    # Tiempo de residencia
    volumetric_flow = F_feed / C_A0  # m³/h
    tau = V_reactor / volumetric_flow  # h

    print(f"\n   Tiempo de residencia (τ):")
    print(f"      τ = V/Q = {V_reactor}/{volumetric_flow:.2f} = {tau:.4f} h")

    # PASO 4: Resolver ecuación de diseño CSTR
    print("\n[4/5] Resolviendo ecuación de diseño del CSTR...")

    # Para CSTR con cinética de 1er orden: r = k·CA
    # Balance: F·CA0·X = V·k·CA = V·k·CA0·(1-X)
    # Simplificando: τ·k = X/(1-X)
    # Resolviendo para X: X = (τ·k)/(1 + τ·k)

    def cstr_conversion(k_value, tau_value):
        """
        Calcula conversión en CSTR para cinética de 1er orden

        Ecuación: X = (τ·k)/(1 + τ·k)
        Derivada de: V/F = X/(k·CA0·(1-X))
        """
        Da = tau_value * k_value  # Número de Damköhler
        X = Da / (1 + Da)
        return X

    print(f"\n   Ecuación de diseño CSTR (cinética 1er orden):")
    print(f"      Balance: V/F = X/(k·CA0·(1-X))")
    print(f"      Simplificado: X = (τ·k)/(1 + τ·k)")
    print(f"      Número de Damköhler: Da = τ·k")

    # Calcular conversión a temperatura de operación
    k_op = k_values[T_operation]
    X_op = cstr_conversion(k_op, tau)
    Da_op = tau * k_op

    print(f"\n   Resultados a {T_operation}°C:")
    print(f"      k = {k_op:.2e} 1/h")
    print(f"      τ = {tau:.4f} h")
    print(f"      Da = τ·k = {Da_op:.4f}")
    print(f"      Conversión (X) = {X_op*100:.2f}%")

    # PASO 5: Análisis de sensibilidad (conversión vs temperatura)
    print("\n[5/5] Análisis de conversión vs temperatura...")

    conversions_vs_T = {}

    print(f"\n   T (°C)    k (1/h)     Da        X (%)")
    print("   " + "-"*50)

    for T_celsius in temperatures:
        k = k_values[float(T_celsius)]
        X = cstr_conversion(k, tau)
        Da = tau * k
        conversions_vs_T[float(T_celsius)] = {
            'k': float(k),
            'Da': float(Da),
            'X_percent': float(X * 100)
        }
        print(f"   {T_celsius:5.0f}   {k:10.2e}   {Da:8.4f}   {X*100:6.2f}")

    # Composición de salida a T de operación
    F_A_in = F_feed * 1.0  # 100% A en alimentación
    F_A_out = F_A_in * (1 - X_op)
    F_B_out = F_A_in * X_op
    F_total = F_A_out + F_B_out

    x_A_out = F_A_out / F_total
    x_B_out = F_B_out / F_total

    # Guardar resultados
    results = {
        'reactor_type': 'CSTR con cinética de Arrhenius (Python + scipy)',
        'parametros_cineticos': {
            'A': A,
            'Ea_J_mol': Ea,
            'R': R,
            'T_operacion_C': T_operation,
            'k_operacion': k_op,
            'volumen_reactor_m3': V_reactor
        },
        'k_vs_temperatura': {str(k): float(v) for k, v in k_values.items()},
        'alimentacion': {
            'T_C': float(T_operation),
            'P_kPa': 101.325,
            'F_kgmoleh': float(F_feed),
            'x_Methanol': 1.0,
            'x_Ethanol': 0.0
        },
        'salida': {
            'T_C': float(T_operation),
            'P_kPa': 101.325,
            'F_kgmoleh': float(F_total),
            'x_Methanol': float(x_A_out),
            'x_Ethanol': float(x_B_out),
            'conversion_percent': float(X_op * 100),
            'tau_h': float(tau),
            'Damkohler': float(Da_op)
        },
        'conversion_vs_temperatura': conversions_vs_T
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'resultados_python.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n   ✓ Resultados guardados: resultados_python.json")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 6 (PYTHON + SCIPY) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA:")
    print("   ✓ Ecuación de Arrhenius: k = A·exp(-Ea/RT)")
    print("   ✓ Número de Damköhler: Da = τ·k (tiempo reacción/residencia)")
    print("   ✓ CSTR 1er orden: X = Da/(1+Da)")
    print("   ✓ k aumenta exponencialmente con T")
    print("   ✓ ↑T → ↑k → ↑X (mayor conversión)")

    print("\n📊 INTERPRETACIÓN DEL NÚMERO DE DAMKÖHLER:")
    print(f"   Da = {Da_op:.4f}")
    if Da_op < 0.1:
        print("   → Régimen cinético (reacción lenta, conversión baja)")
    elif Da_op > 10:
        print("   → Régimen de equilibrio (reacción rápida, X → 100%)")
    else:
        print("   → Régimen intermedio (cinética controla conversión)")

    print("\n📈 EFECTO DE TEMPERATURA:")
    X_50 = conversions_vs_T[50.0]['X_percent']
    X_80 = conversions_vs_T[80.0]['X_percent']
    increment = X_80 - X_50
    print(f"   Conversión a 50°C: {X_50:.2f}%")
    print(f"   Conversión a 80°C: {X_80:.2f}%")
    print(f"   Incremento absoluto: +{increment:.2f} puntos porcentuales")
    print(f"   Incremento relativo: {(X_80/X_50 - 1)*100:.1f}%")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Compara con resultados de aspython.py")
    print("   2. Ejecuta visualiza1.py para graficar X vs T")
    print("   3. Analiza efecto de τ en conversión")
    print("   4. Continúa con Práctica 7: Batch vs Continuo")

    print("="*60)

if __name__ == '__main__':
    main()
