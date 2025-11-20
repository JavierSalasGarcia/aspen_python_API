#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 4: Operación Unitaria - Mixer (ASPEN HYSYS)
=====================================================

Este script demuestra cómo crear y configurar un mezclador (Mixer) en ASPEN HYSYS
para combinar dos corrientes de proceso.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import win32com.client as win32
import time
import json
import os

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 4: OPERACIÓN UNITARIA - MIXER")
    print("="*60)

    try:
        # PASO 1: Iniciar HYSYS
        print("\n[1/7] Iniciando ASPEN HYSYS...")
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True

        # Crear nuevo caso de simulación
        case = hysys.SimulationCases.Add()
        print("   ✓ HYSYS iniciado y caso creado")

        # PASO 2: Configurar componentes y termodinámica
        print("\n[2/7] Configurando componentes...")
        basis_manager = case.BasisManager

        # Crear ComponentList y agregar componentes
        comp_lists = basis_manager.ComponentLists
        comp_list = comp_lists.Add()
        components = comp_list.Components

        components.Add("Methanol")
        components.Add("H2O")

        # Crear FluidPackage y asignar modelo termodinámico
        fluid_pkg = basis_manager.FluidPackages.Add()

        # Probar nombres de paquetes termodinámicos
        nombres_pkg = ["NRTL", "SRK", "PR"]
        for nombre in nombres_pkg:
            try:
                fluid_pkg.PropertyPackageName = nombre
                if fluid_pkg.PropertyPackageName == nombre:
                    print(f"   ✓ Paquete termodinámico: {nombre}")
                    break
            except:
                continue

        print("   ✓ Componentes: Methanol, H2O")

        # PASO 3: Crear corrientes de entrada
        print("\n[3/7] Creando corrientes de entrada...")
        flowsheet = case.Flowsheet
        streams = flowsheet.MaterialStreams

        # Corriente 1: Metanol puro
        stream1 = streams.Add("Entrada_Metanol")
        stream1.ComponentMolarFractionValue("Methanol", 1.0)
        stream1.TemperatureValue = 25 + 273.15  # K
        stream1.PressureValue = 101.325  # kPa
        stream1.MolarFlowValue = 50.0  # kgmole/h

        print(f"\n   Corriente 1: {stream1.StreamName}")
        print(f"      100% Metanol")
        print(f"      T = {stream1.TemperatureValue - 273.15:.2f} °C")
        print(f"      F = {stream1.MolarFlowValue:.2f} kgmole/h")

        # Corriente 2: Agua pura
        stream2 = streams.Add("Entrada_Agua")
        stream2.ComponentMolarFractionValue("H2O", 1.0)
        stream2.TemperatureValue = 30 + 273.15  # K
        stream2.PressureValue = 101.325  # kPa
        stream2.MolarFlowValue = 30.0  # kgmole/h

        print(f"\n   Corriente 2: {stream2.StreamName}")
        print(f"      100% H2O")
        print(f"      T = {stream2.TemperatureValue.GetValue() - 273.15:.2f} °C")
        print(f"      F = {stream2.MolarFlowValue.GetValue():.2f} kgmole/h")

        # PASO 4: Crear corriente de salida
        print("\n[4/7] Creando corriente de salida...")
        stream_out = streams.Add("Salida_Mezcla")
        print("   ✓ Corriente de salida creada")

        # PASO 5: Crear y configurar Mixer
        print("\n[5/7] Creando operación Mixer...")
        operations = flowsheet.Operations
        mixer = operations.Add("Mixer")
        mixer.Name = "Mezclador_Principal"

        # Conectar corrientes
        mixer.Inlets.Add(stream1)
        mixer.Inlets.Add(stream2)
        mixer.Outlet = stream_out

        print("   ✓ Mixer creado y conectado")

        # Esperar cálculos
        time.sleep(2)

        # PASO 6: Extraer resultados
        print("\n[6/7] Extrayendo resultados de la mezcla...")

        results = {
            'entrada1': {
                'nombre': stream1.StreamName,
                'T_C': stream1.TemperatureValue - 273.15,
                'P_kPa': stream1.PressureValue,
                'F_kgmoleh': stream1.MolarFlowValue,
                'x_Methanol': stream1.ComponentMolarFractionValue("Methanol"),
                'x_H2O': stream1.ComponentMolarFractionValue("H2O")
            },
            'entrada2': {
                'nombre': stream2.StreamName,
                'T_C': stream2.TemperatureValue - 273.15,
                'P_kPa': stream2.PressureValue,
                'F_kgmoleh': stream2.MolarFlowValue,
                'x_Methanol': stream2.ComponentMolarFractionValue("Methanol"),
                'x_H2O': stream2.ComponentMolarFractionValue("H2O")
            },
            'salida': {
                'nombre': stream_out.StreamName,
                'T_C': stream_out.TemperatureValue - 273.15,
                'P_kPa': stream_out.PressureValue,
                'F_kgmoleh': stream_out.MolarFlowValue,
                'x_Methanol': stream_out.ComponentMolarFractionValue("Methanol"),
                'x_H2O': stream_out.ComponentMolarFractionValue("H2O"),
                'density_kgm3': stream_out.DensityValue
            }
        }

        print(f"\n   SALIDA DE LA MEZCLA:")
        print(f"      T = {results['salida']['T_C']:.2f} °C")
        print(f"      P = {results['salida']['P_kPa']:.2f} kPa")
        print(f"      F = {results['salida']['F_kgmoleh']:.2f} kgmole/h")
        print(f"      x(Methanol) = {results['salida']['x_Methanol']:.4f}")
        print(f"      x(H2O) = {results['salida']['x_H2O']:.4f}")
        print(f"      Densidad = {results['salida']['density_kgm3']:.2f} kg/m³")

        # Guardar resultados
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, 'resultados_aspen.json')
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n   ✓ Resultados guardados: resultados_aspen.json")

        # PASO 7: Cerrar HYSYS
        print("\n[7/7] Cerrando HYSYS...")
        time.sleep(3)
        hysys.Quit()
        print("   ✓ HYSYS cerrado")

        # RESUMEN
        print("\n" + "="*60)
        print("PRÁCTICA 4 COMPLETADA EXITOSAMENTE")
        print("="*60)

        print("\n💡 CONCEPTOS CLAVE:")
        print("   ✓ Operación Mixer combina múltiples corrientes")
        print("   ✓ Balance de materia: F_total = F1 + F2")
        print("   ✓ Balance de energía: T_salida depende de flujos y temperaturas")
        print("   ✓ Composición de salida: promedio ponderado por flujo")

        print("\n📊 VERIFICACIÓN:")
        F_total = results['entrada1']['F_kgmoleh'] + results['entrada2']['F_kgmoleh']
        print(f"   F1 + F2 = {results['entrada1']['F_kgmoleh']:.2f} + {results['entrada2']['F_kgmoleh']:.2f} = {F_total:.2f} kgmole/h")
        print(f"   F_salida = {results['salida']['F_kgmoleh']:.2f} kgmole/h")
        print(f"   {'✓ Balance OK' if abs(F_total - results['salida']['F_kgmoleh']) < 0.1 else '✗ Error en balance'}")

        print("\n🔄 PRÓXIMOS PASOS:")
        print("   1. Ejecuta py_alone.py para comparar")
        print("   2. Ejecuta visualiza1.py y visualiza2.py")
        print("   3. Continúa con Práctica 5: Reactor CSTR")

        print("="*60)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
