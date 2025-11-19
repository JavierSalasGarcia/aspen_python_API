#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 7: Comparación Batch vs CSTR - Análisis Analítico (Python Puro)
==========================================================================

Este script compara reactores Batch y CSTR usando ecuaciones analíticas y
scipy para integración numérica.

Batch: Integración de dX/dt = k·CA0·(1-X)
CSTR: Solución algebraica X = (τ·k)/(1 + τ·k)

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import numpy as np
import json
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 7: BATCH vs CSTR (PYTHON + SCIPY)")
    print("="*60)

    # PASO 1: Parámetros de reacción
    print("\n[1/6] Definiendo parámetros de reacción...")

    k = 0.5  # 1/h (constante de velocidad de 1er orden)
    CA0 = 1.0  # kgmole/m³ (concentración inicial)
    conversion_target = 0.90  # 90%

    print(f"   Reacción: A → B (cinética de 1er orden)")
    print(f"   r = k·CA = k·CA0·(1-X)")
    print(f"   k = {k} 1/h")
    print(f"   CA0 = {CA0} kgmole/m³")
    print(f"   Conversión objetivo: {conversion_target*100:.0f}%")

    # PASO 2: Resolver reactor BATCH
    print("\n[2/6] Resolviendo reactor BATCH...")

    def batch_ode(X, t, k_value):
        """
        Ecuación diferencial para reactor batch

        dX/dt = k·CA0·(1-X) / CA0 = k·(1-X)

        Parámetros:
            X: conversión
            t: tiempo (h)
            k_value: constante de velocidad (1/h)
        """
        dXdt = k_value * (1 - X)
        return dXdt

    # Solución analítica para batch
    # Integrando: ∫dX/(1-X) = ∫k·dt
    # -ln(1-X) = k·t
    # X = 1 - exp(-k·t)
    # Para tiempo necesario: t = -ln(1-X)/k

    t_batch_analytical = -np.log(1 - conversion_target) / k

    print(f"\n   Solución analítica:")
    print(f"      Ecuación: X = 1 - exp(-k·t)")
    print(f"      Para X = {conversion_target*100:.0f}%:")
    print(f"      t = -ln(1-{conversion_target})/k = {t_batch_analytical:.2f} h")

    # Solución numérica (integración con scipy)
    t_span = np.linspace(0, 10, 100)  # h
    X_batch_numeric = odeint(batch_ode, 0.0, t_span, args=(k,))

    # Encontrar tiempo para alcanzar conversión objetivo
    idx_target = np.argmin(np.abs(X_batch_numeric.flatten() - conversion_target))
    t_batch_numeric = t_span[idx_target]

    print(f"\n   Solución numérica (scipy.odeint):")
    print(f"      t ≈ {t_batch_numeric:.2f} h")
    print(f"      Diferencia: {abs(t_batch_analytical - t_batch_numeric):.4f} h")

    # Perfil completo de conversión vs tiempo
    print(f"\n   Perfil de conversión vs tiempo:")
    print(f"   {'t (h)':>8}  {'X':>8}  {'Velocidad (dX/dt)':>20}")
    print("   " + "-"*45)

    batch_profile = []
    for t_val in [0.5, 1.0, 2.0, 4.0, 6.0]:
        X_val = 1 - np.exp(-k * t_val)
        dXdt_val = k * (1 - X_val)
        batch_profile.append({'t': t_val, 'X': X_val, 'dXdt': dXdt_val})
        print(f"   {t_val:8.2f}  {X_val:8.4f}  {dXdt_val:20.4f}")

    # PASO 3: Resolver reactor CSTR
    print("\n[3/6] Resolviendo reactor CSTR...")

    def cstr_conversion(tau_value, k_value):
        """
        Conversión en CSTR para cinética de 1er orden

        Balance de materia: V·r = F·(CAin - CAout)
        Para 1er orden: τ·k·CA = CA0·X
        CA = CA0·(1-X)
        τ·k·CA0·(1-X) = CA0·X
        X = (τ·k)/(1 + τ·k)

        Parámetros:
            tau_value: tiempo de residencia (h)
            k_value: constante de velocidad (1/h)
        """
        Da = tau_value * k_value  # Número de Damköhler
        X = Da / (1 + Da)
        return X

    # Tiempo de residencia necesario para conversión objetivo
    # De X = (τ·k)/(1 + τ·k), despejando τ:
    # τ = X/(k·(1-X))
    tau_cstr = conversion_target / (k * (1 - conversion_target))

    print(f"\n   Ecuación algebraica:")
    print(f"      Balance: X = (τ·k)/(1 + τ·k)")
    print(f"      Despejando: τ = X/(k·(1-X))")
    print(f"      Para X = {conversion_target*100:.0f}%:")
    print(f"      τ = {tau_cstr:.2f} h")

    # Número de Damköhler
    Da = tau_cstr * k
    print(f"\n   Número de Damköhler:")
    print(f"      Da = τ·k = {tau_cstr:.2f} × {k} = {Da:.2f}")

    # Perfil de conversión vs tiempo de residencia
    print(f"\n   Perfil de conversión vs tiempo de residencia:")
    print(f"   {'τ (h)':>8}  {'X':>8}  {'Da':>8}")
    print("   " + "-"*30)

    cstr_profile = []
    for tau_val in [0.5, 1.0, 2.0, 4.0, 10.0]:
        X_val = cstr_conversion(tau_val, k)
        Da_val = tau_val * k
        cstr_profile.append({'tau': tau_val, 'X': X_val, 'Da': Da_val})
        print(f"   {tau_val:8.2f}  {X_val:8.4f}  {Da_val:8.2f}")

    # PASO 4: Comparación de tiempos
    print("\n[4/6] Comparación de tiempos de operación...")

    print(f"\n   Para alcanzar X = {conversion_target*100:.0f}%:")
    print(f"      Reactor Batch:    t = {t_batch_analytical:.2f} h")
    print(f"      Reactor CSTR:     τ = {tau_cstr:.2f} h")
    print(f"      Ratio (τ/t):      {tau_cstr/t_batch_analytical:.2f}×")

    print(f"\n   CSTR requiere {(tau_cstr/t_batch_analytical - 1)*100:.1f}% más tiempo")
    print(f"   (para la misma conversión)")

    # PASO 5: Análisis de productividad
    print("\n[5/6] Análisis de productividad...")

    # Parámetros de producción
    V_batch = 10.0  # m³ (volumen del batch)
    t_downtime = 1.0  # h (carga + descarga + limpieza)

    # Productividad Batch
    moles_per_batch = V_batch * CA0 * conversion_target  # kgmole
    t_cycle_batch = t_batch_analytical + t_downtime  # h
    productivity_batch = moles_per_batch / t_cycle_batch  # kgmole/h

    # Productividad CSTR (continuo)
    Q_cstr = V_batch / tau_cstr  # m³/h (flujo volumétrico)
    F_cstr = Q_cstr * CA0  # kgmole/h (flujo molar)
    productivity_cstr = F_cstr * conversion_target  # kgmole/h

    print(f"\n   REACTOR BATCH:")
    print(f"      Volumen: {V_batch} m³")
    print(f"      Tiempo de reacción: {t_batch_analytical:.2f} h")
    print(f"      Tiempo muerto: {t_downtime:.2f} h")
    print(f"      Tiempo de ciclo: {t_cycle_batch:.2f} h")
    print(f"      Producción por batch: {moles_per_batch:.2f} kgmole")
    print(f"      Productividad: {productivity_batch:.2f} kgmole/h")

    print(f"\n   REACTOR CSTR:")
    print(f"      Volumen: {V_batch} m³ (mismo que batch)")
    print(f"      Tiempo de residencia: {tau_cstr:.2f} h")
    print(f"      Flujo de alimentación: {F_cstr:.2f} kgmole/h")
    print(f"      Productividad: {productivity_cstr:.2f} kgmole/h")

    ratio_productivity = productivity_cstr / productivity_batch
    print(f"\n   Ratio de productividad (CSTR/Batch): {ratio_productivity:.2f}×")
    print(f"   CSTR produce {(ratio_productivity - 1)*100:.1f}% más")

    # PASO 6: Guardar resultados
    print("\n[6/6] Guardando resultados...")

    results = {
        'parametros_cineticos': {
            'k_1h': k,
            'CA0_kgmolem3': CA0,
            'conversion_target': conversion_target * 100
        },
        'batch_reactor': {
            'tipo': 'Discontinuo',
            'ecuacion': 'dX/dt = k·(1-X)',
            'solucion': 'X = 1 - exp(-k·t)',
            'tiempo_reaccion_h': t_batch_analytical,
            'tiempo_muerto_h': t_downtime,
            'tiempo_ciclo_h': t_cycle_batch,
            'volumen_m3': V_batch,
            'produccion_por_batch_kgmole': moles_per_batch,
            'productividad_kgmoleh': productivity_batch,
            'perfil_tiempo': batch_profile[:5]
        },
        'cstr_reactor': {
            'tipo': 'Continuo',
            'ecuacion': 'X = (τ·k)/(1 + τ·k)',
            'tiempo_residencia_h': tau_cstr,
            'Damkohler': Da,
            'volumen_m3': V_batch,
            'flujo_alimentacion_kgmoleh': F_cstr,
            'productividad_kgmoleh': productivity_cstr,
            'perfil_tau': cstr_profile[:5]
        },
        'comparacion': {
            'ratio_tiempo': tau_cstr / t_batch_analytical,
            'ratio_productividad': ratio_productivity,
            'ventaja_tiempo_batch': f'Batch es {(1 - t_batch_analytical/tau_cstr)*100:.1f}% más rápido',
            'ventaja_productividad_cstr': f'CSTR produce {(ratio_productivity - 1)*100:.1f}% más',
            'conclusion': 'CSTR es superior para producción continua a pesar de mayor τ'
        }
    }

    output_file = '/home/user/aspen_python_API/practica7/resultados_python.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"   ✓ Resultados guardados: resultados_python.json")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 7 (PYTHON + SCIPY) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA:")
    print("   ✓ Batch: dX/dt = k·(1-X) → X = 1 - exp(-k·t)")
    print("   ✓ CSTR: X = (τ·k)/(1 + τ·k) = Da/(1+Da)")
    print("   ✓ τ_CSTR > t_Batch para misma X (más volumen)")
    print("   ✓ CSTR tiene mayor productividad (sin downtime)")
    print("   ✓ Número de Damköhler cuantifica rendimiento")

    print("\n📊 COMPARACIÓN CUANTITATIVA:")
    print(f"   Tiempo de reacción:")
    print(f"      Batch: {t_batch_analytical:.2f} h")
    print(f"      CSTR:  {tau_cstr:.2f} h (+{(tau_cstr/t_batch_analytical - 1)*100:.1f}%)")
    print(f"\n   Productividad:")
    print(f"      Batch: {productivity_batch:.2f} kgmole/h")
    print(f"      CSTR:  {productivity_cstr:.2f} kgmole/h (+{(ratio_productivity - 1)*100:.1f}%)")

    print("\n⚖️ CRITERIOS DE SELECCIÓN:")
    print("   Elegir BATCH si:")
    print("   • Producción < 10 ton/año")
    print("   • Múltiples productos (flexibilidad)")
    print("   • Productos de alto valor añadido")
    print("   • Tiempo muerto < 20% del ciclo")
    print("\n   Elegir CSTR si:")
    print("   • Producción > 100 ton/año")
    print("   • Producto único o pocos cambios")
    print("   • Economías de escala importantes")
    print("   • Operación 24/7 requerida")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Compara con resultados de aspython.py")
    print("   2. Ejecuta visualiza1.py para graficar perfiles")
    print("   3. Analiza efecto del tiempo muerto en Batch")
    print("   4. Continúa con Práctica 8: Planta completa de Biodiesel")

    print("="*60)

if __name__ == '__main__':
    main()
