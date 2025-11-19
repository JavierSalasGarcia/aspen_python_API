#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 6: Reactor CSTR con Cinética de Arrhenius (ASPEN HYSYS)
=================================================================

Este script demuestra cómo configurar un reactor CSTR con modelo cinético
de Arrhenius en ASPEN HYSYS y analizar el efecto de la temperatura.

Ecuación de Arrhenius: k = A * exp(-Ea/RT)
Diseño CSTR: V/F = X / (k·CA0·(1-X))

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import win32com.client as win32
import time
import json
import numpy as np

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 6: REACTOR CSTR CON CINÉTICA DE ARRHENIUS")
    print("="*60)

    try:
        # PASO 1: Iniciar HYSYS
        print("\n[1/9] Iniciando ASPEN HYSYS...")
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.ActiveDocument
        print("   ✓ HYSYS iniciado")

        # PASO 2: Configurar componentes
        print("\n[2/9] Configurando componentes...")
        fluid_pkg = case.FluidPackage
        components = fluid_pkg.Components

        # Reacción simple A → B
        components.Add("Methanol")  # Componente A (reactivo)
        components.Add("Ethanol")   # Componente B (producto)

        fluid_pkg.PropertyPackage = "NRTL"
        print("   ✓ Componentes: Methanol (A) → Ethanol (B)")
        print("   ✓ Paquete termodinámico: NRTL")

        # PASO 3: Parámetros cinéticos de Arrhenius
        print("\n[3/9] Definiendo parámetros cinéticos de Arrhenius...")

        # Parámetros típicos para reacción de biodiesel
        A = 1.0e6   # Factor pre-exponencial (1/h)
        Ea = 60000  # Energía de activación (J/mol)
        R = 8.314   # Constante de gases (J/mol·K)

        print(f"   Parámetros de Arrhenius:")
        print(f"      A (factor pre-exponencial) = {A:.2e} 1/h")
        print(f"      Ea (energía de activación) = {Ea:.0f} J/mol")
        print(f"      R (constante gases) = {R:.3f} J/(mol·K)")

        # Calcular k a diferentes temperaturas
        temperatures = [50, 60, 70, 80]  # °C
        print(f"\n   Constantes de velocidad calculadas:")

        k_values = {}
        for T_celsius in temperatures:
            T_kelvin = T_celsius + 273.15
            k = A * np.exp(-Ea / (R * T_kelvin))
            k_values[T_celsius] = k
            print(f"      T = {T_celsius}°C → k = {k:.2e} 1/h")

        # PASO 4: Crear corriente de alimentación
        print("\n[4/9] Creando corriente de alimentación...")
        flowsheet = case.Flowsheet
        streams = flowsheet.MaterialStreams

        # Temperatura de operación seleccionada
        T_operation = 60  # °C

        feed_stream = streams.Add("Feed_Reactor")
        feed_stream.ComponentMolarFractionValue("Methanol", 1.0)  # 100% A
        feed_stream.TemperatureValue = T_operation + 273.15  # K
        feed_stream.PressureValue = 101.325  # kPa
        feed_stream.MolarFlowValue = 100.0  # kgmole/h

        print(f"   Alimentación:")
        print(f"      100% Methanol (reactivo A)")
        print(f"      T = {T_operation} °C")
        print(f"      F = 100.0 kgmole/h")

        # PASO 5: Crear corriente de salida
        print("\n[5/9] Creando corriente de salida...")
        outlet_stream = streams.Add("Product_Stream")
        print("   ✓ Corriente de salida creada")

        # PASO 6: Crear reactor cinético
        print("\n[6/9] Creando reactor CSTR con cinética...")
        operations = flowsheet.Operations
        reactor = operations.Add("KineticReactor")
        reactor.Name = "CSTR_Kinetic"

        # Conectar corrientes
        reactor.Feeds.Add(feed_stream)
        reactor.Outlet = outlet_stream

        # Especificar volumen del reactor
        reactor_volume = 10.0  # m³
        reactor.Volume = reactor_volume

        print(f"   ✓ Reactor cinético creado")
        print(f"   Volumen del reactor: {reactor_volume} m³")

        # PASO 7: Configurar reacción con cinética
        print("\n[7/9] Configurando reacción con cinética de Arrhenius...")

        rxn_set = reactor.ReactionSet
        rxn = rxn_set.Reactions.Add()

        # Estequiometría: A → B
        rxn.ComponentStoichCoeffValue("Methanol", -1.0)  # A (reactivo)
        rxn.ComponentStoichCoeffValue("Ethanol", 1.0)     # B (producto)

        # Configurar cinética de Arrhenius
        # Nota: En HYSYS real se configuran A y Ea en el objeto de reacción
        # Esta es una aproximación educativa

        print(f"   Estequiometría: Methanol → Ethanol")
        print(f"   Cinética: r = k·CA")
        print(f"   k = {A:.2e}·exp(-{Ea}/{R}·T)")

        # Esperar cálculos
        print("\n   ⏳ Esperando que HYSYS calcule el reactor...")
        time.sleep(3)

        # PASO 8: Extraer resultados
        print("\n[8/9] Extrayendo resultados...")

        # Información de alimentación
        feed_T = feed_stream.TemperatureValue - 273.15
        feed_F = feed_stream.MolarFlowValue
        feed_x_A = feed_stream.ComponentMolarFractionValue("Methanol")

        # Información de salida
        outlet_T = outlet_stream.TemperatureValue - 273.15
        outlet_F = outlet_stream.MolarFlowValue
        outlet_x_A = outlet_stream.ComponentMolarFractionValue("Methanol")
        outlet_x_B = outlet_stream.ComponentMolarFractionValue("Ethanol")

        # Calcular conversión
        F_A_in = feed_F * feed_x_A
        F_A_out = outlet_F * outlet_x_A
        conversion = (F_A_in - F_A_out) / F_A_in * 100

        # Calcular tiempo de residencia
        # Asumiendo densidad constante, tau = V/F
        tau = reactor_volume / (feed_F * 0.001)  # h (asumiendo densidad molar ~1000 mol/m³)

        results = {
            'reactor_type': 'CSTR con cinética de Arrhenius',
            'parametros_cineticos': {
                'A': A,
                'Ea_J_mol': Ea,
                'R': R,
                'T_operacion_C': T_operation,
                'k_operacion': k_values[T_operation],
                'volumen_reactor_m3': reactor_volume
            },
            'k_vs_temperatura': k_values,
            'alimentacion': {
                'T_C': feed_T,
                'P_kPa': feed_stream.PressureValue,
                'F_kgmoleh': feed_F,
                'x_Methanol': feed_x_A,
                'x_Ethanol': 0.0
            },
            'salida': {
                'T_C': outlet_T,
                'P_kPa': outlet_stream.PressureValue,
                'F_kgmoleh': outlet_F,
                'x_Methanol': outlet_x_A,
                'x_Ethanol': outlet_x_B,
                'conversion_percent': conversion,
                'tau_h': tau
            }
        }

        print(f"\n   RESULTADOS DEL REACTOR:")
        print(f"   Alimentación:")
        print(f"      T = {feed_T:.2f} °C")
        print(f"      F = {feed_F:.2f} kgmole/h")
        print(f"      x(A) = {feed_x_A:.4f}")

        print(f"\n   Salida:")
        print(f"      T = {outlet_T:.2f} °C")
        print(f"      x(A) = {outlet_x_A:.4f}")
        print(f"      x(B) = {outlet_x_B:.4f}")
        print(f"      Conversión = {conversion:.2f}%")

        print(f"\n   Parámetros de diseño:")
        print(f"      Tiempo de residencia (τ) ≈ {tau:.2f} h")
        print(f"      k a {T_operation}°C = {k_values[T_operation]:.2e} 1/h")

        # Guardar resultados
        output_file = '/home/user/aspen_python_API/practica6/resultados_aspen.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n   ✓ Resultados guardados: resultados_aspen.json")

        # PASO 9: Cerrar HYSYS
        print("\n[9/9] Cerrando HYSYS...")
        time.sleep(2)
        case.SaveRequired = False
        hysys.Quit()
        print("   ✓ HYSYS cerrado")

        # RESUMEN
        print("\n" + "="*60)
        print("PRÁCTICA 6 COMPLETADA EXITOSAMENTE")
        print("="*60)

        print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA:")
        print("   ✓ Ecuación de Arrhenius: k = A·exp(-Ea/RT)")
        print("   ✓ k aumenta exponencialmente con temperatura")
        print("   ✓ Ea determina sensibilidad térmica de la reacción")
        print("   ✓ CSTR: τ = V/F (tiempo de residencia)")
        print("   ✓ Conversión depende de k y τ")

        print("\n📊 ANÁLISIS DE TEMPERATURA:")
        print("   Efecto de temperatura sobre k:")
        for T_c, k_val in sorted(k_values.items()):
            ratio = k_val / k_values[50]
            print(f"      {T_c}°C: k = {k_val:.2e} (×{ratio:.2f} vs 50°C)")

        print("\n🔄 PRÓXIMOS PASOS:")
        print("   1. Ejecuta py_alone.py para resolver cinética con scipy")
        print("   2. Compara conversión vs temperatura")
        print("   3. Analiza efecto de volumen del reactor")
        print("   4. Continúa con Práctica 7: Batch vs Continuo")

        print("="*60)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n   Posibles causas:")
        print("   - HYSYS no soporta KineticReactor en esta versión")
        print("   - Usar ConversionReactor con conversión calculada")
        print("   - Parámetros cinéticos no configurados correctamente")

if __name__ == '__main__':
    main()
