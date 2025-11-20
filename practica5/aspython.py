#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 5: Reactor CSTR con Conversión Fija (ASPEN HYSYS)
===========================================================

Este script demuestra cómo crear y configurar un reactor CSTR (Continuous Stirred
Tank Reactor) en ASPEN HYSYS con conversión fija.

Reacción simulada: Transesterificación (simplificada)
Metanol + Triglicérido → Biodiesel + Glicerol

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import win32com.client as win32
import time
import json

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 5: REACTOR CSTR CON CONVERSIÓN FIJA")
    print("="*60)

    try:
        # PASO 1: Iniciar HYSYS
        print("\n[1/8] Iniciando ASPEN HYSYS...")
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True

        # Crear nuevo caso de simulación
        case = hysys.SimulationCases.Add()
        print("   ✓ HYSYS iniciado y caso creado")

        # PASO 2: Configurar componentes
        print("\n[2/8] Configurando componentes para biodiesel...")
        fluid_pkg = case.FluidPackage
        components = fluid_pkg.Components

        # Componentes para reacción de transesterificación
        components.Add("Methanol")      # Reactivo
        components.Add("Ethanol")       # Sustituto de triglicérido
        components.Add("Ethyl acetate") # Sustituto de biodiesel
        components.Add("Water")         # Sustituto de glicerol

        fluid_pkg.PropertyPackage = "NRTL"
        print("   ✓ Componentes: Methanol, Ethanol, Ethyl acetate, Water")
        print("   ✓ Paquete termodinámico: NRTL")
        print("   ℹ Nota: Se usan sustitutos por disponibilidad en HYSYS")

        # PASO 3: Crear corriente de alimentación
        print("\n[3/8] Creando corriente de alimentación al reactor...")
        flowsheet = case.Flowsheet
        streams = flowsheet.MaterialStreams

        # Corriente de alimentación: Mezcla de reactivos
        feed_stream = streams.Add("Alimentacion_Reactor")
        feed_stream.ComponentMolarFractionValue("Methanol", 0.60)
        feed_stream.ComponentMolarFractionValue("Ethanol", 0.40)
        feed_stream.TemperatureValue = 60 + 273.15  # K (60°C, temperatura típica)
        feed_stream.PressureValue = 101.325  # kPa
        feed_stream.MolarFlowValue = 100.0  # kgmole/h

        print(f"   Alimentación al reactor:")
        print(f"      x(Methanol) = 0.60 (exceso)")
        print(f"      x(Ethanol) = 0.40 (triglicérido)")
        print(f"      T = 60 °C")
        print(f"      F = 100.0 kgmole/h")

        # PASO 4: Crear corriente de salida
        print("\n[4/8] Creando corriente de salida...")
        outlet_stream = streams.Add("Salida_Reactor")
        print("   ✓ Corriente de salida creada")

        # PASO 5: Crear reactor de conversión
        print("\n[5/8] Creando reactor CSTR con conversión fija...")
        operations = flowsheet.Operations
        reactor = operations.Add("ConversionReactor")
        reactor.Name = "CSTR_Biodiesel"

        # Conectar corrientes
        reactor.Feeds.Add(feed_stream)
        reactor.Outlet = outlet_stream

        print("   ✓ Reactor CSTR creado")
        print("   ✓ Corrientes conectadas")

        # PASO 6: Configurar reacción química
        print("\n[6/8] Configurando reacción de transesterificación...")

        # Agregar reacción al reactor
        rxn_set = reactor.ReactionSet
        rxn = rxn_set.Reactions.Add()

        # Definir estequiometría (simplificada)
        # Methanol + Ethanol → Ethyl acetate + Water
        rxn.ComponentStoichCoeffValue("Methanol", -1.0)   # Reactivo
        rxn.ComponentStoichCoeffValue("Ethanol", -1.0)    # Reactivo
        rxn.ComponentStoichCoeffValue("Ethyl acetate", 1.0) # Producto (biodiesel)
        rxn.ComponentStoichCoeffValue("Water", 1.0)       # Producto (glicerol)

        # Configurar base de conversión
        rxn.BaseComponent = "Ethanol"  # Conversión basada en triglicérido

        # Establecer conversión fija (85%)
        conversion_percent = 85.0
        rxn.Conversion = conversion_percent / 100.0

        print(f"   Estequiometría:")
        print(f"      Methanol + Ethanol → Ethyl acetate + Water")
        print(f"   Conversión fija: {conversion_percent}%")
        print(f"   Base de conversión: Ethanol (triglicérido)")

        # Esperar cálculos
        print("\n   ⏳ Esperando que HYSYS calcule el reactor...")
        time.sleep(3)

        # PASO 7: Extraer resultados
        print("\n[7/8] Extrayendo resultados del reactor...")

        # Información de alimentación
        feed_T = feed_stream.TemperatureValue - 273.15
        feed_F = feed_stream.MolarFlowValue
        feed_x_methanol = feed_stream.ComponentMolarFractionValue("Methanol")
        feed_x_ethanol = feed_stream.ComponentMolarFractionValue("Ethanol")

        # Información de salida
        outlet_T = outlet_stream.TemperatureValue - 273.15
        outlet_F = outlet_stream.MolarFlowValue
        outlet_x_methanol = outlet_stream.ComponentMolarFractionValue("Methanol")
        outlet_x_ethanol = outlet_stream.ComponentMolarFractionValue("Ethanol")
        outlet_x_biodiesel = outlet_stream.ComponentMolarFractionValue("Ethyl acetate")
        outlet_x_glycerol = outlet_stream.ComponentMolarFractionValue("Water")

        results = {
            'reactor_type': 'CSTR con conversión fija',
            'conversion_specified': conversion_percent,
            'alimentacion': {
                'T_C': feed_T,
                'P_kPa': feed_stream.PressureValue,
                'F_kgmoleh': feed_F,
                'x_Methanol': feed_x_methanol,
                'x_Ethanol': feed_x_ethanol,
                'x_Biodiesel': 0.0,
                'x_Glycerol': 0.0
            },
            'salida': {
                'T_C': outlet_T,
                'P_kPa': outlet_stream.PressureValue,
                'F_kgmoleh': outlet_F,
                'x_Methanol': outlet_x_methanol,
                'x_Ethanol': outlet_x_ethanol,
                'x_Biodiesel': outlet_x_biodiesel,
                'x_Glycerol': outlet_x_glycerol
            }
        }

        print(f"\n   RESULTADOS DEL REACTOR:")
        print(f"   Alimentación:")
        print(f"      T = {feed_T:.2f} °C")
        print(f"      F = {feed_F:.2f} kgmole/h")
        print(f"      x(Methanol) = {feed_x_methanol:.4f}")
        print(f"      x(Ethanol) = {feed_x_ethanol:.4f}")

        print(f"\n   Salida:")
        print(f"      T = {outlet_T:.2f} °C")
        print(f"      F = {outlet_F:.2f} kgmole/h")
        print(f"      x(Methanol) = {outlet_x_methanol:.4f}")
        print(f"      x(Ethanol) = {outlet_x_ethanol:.4f}")
        print(f"      x(Biodiesel) = {outlet_x_biodiesel:.4f}")
        print(f"      x(Glycerol) = {outlet_x_glycerol:.4f}")

        # Guardar resultados
        output_file = '/home/user/aspen_python_API/practica5/resultados_aspen.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n   ✓ Resultados guardados: resultados_aspen.json")

        # PASO 8: Cerrar HYSYS
        print("\n[8/8] Cerrando HYSYS...")
        time.sleep(2)
        case.SaveRequired = False
        hysys.Quit()
        print("   ✓ HYSYS cerrado")

        # RESUMEN
        print("\n" + "="*60)
        print("PRÁCTICA 5 COMPLETADA EXITOSAMENTE")
        print("="*60)

        print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA:")
        print("   ✓ CSTR (Continuous Stirred Tank Reactor)")
        print("   ✓ Conversión = moles reaccionados / moles alimentados")
        print("   ✓ Conversión fija: útil para diseño preliminar")
        print("   ✓ Exceso de Methanol (60%) mejora conversión")
        print("   ✓ Balance de materia con reacción química")

        print("\n📊 ANÁLISIS DE CONVERSIÓN:")
        F_ethanol_in = feed_F * feed_x_ethanol
        F_ethanol_out = outlet_F * outlet_x_ethanol
        conversion_real = (F_ethanol_in - F_ethanol_out) / F_ethanol_in * 100
        print(f"   Etanol alimentado: {F_ethanol_in:.2f} kgmole/h")
        print(f"   Etanol sin reaccionar: {F_ethanol_out:.2f} kgmole/h")
        print(f"   Conversión alcanzada: {conversion_real:.2f}%")

        print("\n🔄 PRÓXIMOS PASOS:")
        print("   1. Ejecuta py_alone.py para comparar cálculos Python")
        print("   2. Experimenta con diferentes conversiones (60%, 90%)")
        print("   3. Analiza efecto de exceso de Methanol")
        print("   4. Continúa con Práctica 6: Cinética de Arrhenius")

        print("="*60)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n   Posibles causas:")
        print("   - HYSYS no está instalado o sin licencia")
        print("   - Componentes no disponibles en base de datos")
        print("   - Error en configuración de reacción")

if __name__ == '__main__':
    main()
