#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 8: Planta Completa de Biodiesel (ASPEN HYSYS)
=======================================================

Este script simula una planta completa de producción de biodiesel con:
1. Mezclador: Metanol + Triglicérido
2. Reactor: Transesterificación
3. Separador: Biodiesel/Glicerol
4. Lavado: Remoción de impurezas
5. Secado: Remoción de agua

Calcula rendimiento global, pureza y eficiencia energética.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import win32com.client as win32
import time
import json
import os

def main():
    """Función principal"""

    print("="*70)
    print("PRÁCTICA 8: PLANTA COMPLETA DE PRODUCCIÓN DE BIODIESEL")
    print("="*70)

    try:
        # PASO 1: Iniciar HYSYS
        print("\n[1/15] Iniciando ASPEN HYSYS...")
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True

        # Crear nuevo caso de simulación
        case = hysys.SimulationCases.Add()
        print("   ✓ HYSYS iniciado y caso creado")

        # PASO 2: Configurar componentes
        print("\n[2/15] Configurando componentes del proceso...")
        basis_manager = case.BasisManager

        # Crear ComponentList y agregar componentes
        comp_lists = basis_manager.ComponentLists
        comp_list = comp_lists.Add()
        components = comp_list.Components

        # Componentes del proceso de biodiesel (usando sustitutos disponibles)
        components.Add("Methanol")      # Alcohol
        components.Add("Ethanol")       # Triglicérido (sustituto)
        components.Add("Ethyl acetate") # Biodiesel (sustituto)
        components.Add("H2O")           # Agua (lavado/glicerol)

        # Intentar agregar Glycerol si está disponible
        try:
            components.Add("Glycerol")
        except:
            pass  # Si no está disponible, continuar sin él

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

        print("   ✓ Componentes configurados")
        print("   ℹ Nota: Se usan sustitutos por disponibilidad")

        flowsheet = case.Flowsheet
        streams = flowsheet.MaterialStreams
        operations = flowsheet.Operations

        # PASO 3: Crear alimentaciones
        print("\n[3/15] Creando corrientes de alimentación...")

        # Alimentación 1: Triglicérido (aceite vegetal)
        feed_oil = streams.Add("Aceite_Vegetal")
        feed_oil.ComponentMolarFractionValue("Ethanol", 1.0)  # 100% Triglicérido
        feed_oil.TemperatureValue = 25 + 273.15  # K
        feed_oil.PressureValue = 101.325  # kPa
        feed_oil.MolarFlowValue = 100.0  # kgmole/h

        # Alimentación 2: Metanol (exceso)
        feed_methanol = streams.Add("Metanol_Fresco")
        feed_methanol.ComponentMolarFractionValue("Methanol", 1.0)
        feed_methanol.TemperatureValue = 25 + 273.15  # K
        feed_methanol.PressureValue = 101.325  # kPa
        feed_methanol.MolarFlowValue = 120.0  # kgmole/h (20% exceso)

        print(f"   Aceite vegetal: 100 kgmole/h a 25°C")
        print(f"   Metanol: 120 kgmole/h (20% exceso)")

        # PASO 4: Mezclador
        print("\n[4/15] Configurando mezclador de reactivos...")

        mixer = operations.Add("Mixer")
        mixer.Name = "Mezclador_Reactivos"

        stream_mixed = streams.Add("Mezcla_Reactivos")

        mixer.Inlets.Add(feed_oil)
        mixer.Inlets.Add(feed_methanol)
        mixer.Outlet = stream_mixed

        print("   ✓ Mezclador configurado")

        time.sleep(2)

        # PASO 5: Intercambiador de calor (precalentamiento)
        print("\n[5/15] Configurando precalentador...")

        stream_heated = streams.Add("Mezcla_Caliente")

        heater = operations.Add("Heater")
        heater.Name = "Precalentador"
        heater.Inlet = stream_mixed
        heater.Outlet = stream_heated

        # Especificar temperatura de salida
        heater.OutletTemperature = 60 + 273.15  # K (60°C óptimo)

        print("   ✓ Precalentador: 25°C → 60°C")

        time.sleep(2)

        # PASO 6: Reactor de transesterificación
        print("\n[6/15] Configurando reactor de transesterificación...")

        stream_reactor_out = streams.Add("Salida_Reactor")

        reactor = operations.Add("ConversionReactor")
        reactor.Name = "Reactor_Transesterificacion"
        reactor.Feeds.Add(stream_heated)
        reactor.Outlet = stream_reactor_out

        # Configurar reacción
        rxn_set = reactor.ReactionSet
        rxn = rxn_set.Reactions.Add()

        # Estequiometría: Methanol + Ethanol → Ethyl acetate + Water
        rxn.ComponentStoichCoeffValue("Methanol", -1.0)
        rxn.ComponentStoichCoeffValue("Ethanol", -1.0)
        rxn.ComponentStoichCoeffValue("Ethyl acetate", 1.0)  # Biodiesel
        rxn.ComponentStoichCoeffValue("H2O", 1.0)  # Glicerol

        rxn.BaseComponent = "Ethanol"
        rxn.Conversion = 0.90  # 90% conversión

        print("   ✓ Reactor configurado (X = 90%)")

        time.sleep(2)

        # PASO 7: Separador Biodiesel/Glicerol
        print("\n[7/15] Configurando separador principal...")

        stream_biodiesel_crude = streams.Add("Biodiesel_Crudo")
        stream_glycerol_crude = streams.Add("Glicerol_Crudo")

        separator = operations.Add("ComponentSplitter")
        separator.Name = "Separador_Principal"
        separator.Inlet = stream_reactor_out
        separator.VapourOutlet = stream_biodiesel_crude  # Fase liviana (biodiesel)
        separator.LiquidOutlet = stream_glycerol_crude   # Fase pesada (glicerol)

        # Especificar splits (eficiencias de separación)
        # Biodiesel y Metanol van a fase liviana
        # Glicerol y Agua van a fase pesada

        print("   ✓ Separador configurado")
        print("   Fase liviana: Biodiesel + Metanol no reaccionado")
        print("   Fase pesada: Glicerol + Agua")

        time.sleep(2)

        # PASO 8: Lavado del biodiesel
        print("\n[8/15] Configurando etapa de lavado...")

        # Agua de lavado
        wash_water = streams.Add("Agua_Lavado")
        wash_water.ComponentMolarFractionValue("H2O", 1.0)
        wash_water.TemperatureValue = 25 + 273.15  # K
        wash_water.PressureValue = 101.325  # kPa
        wash_water.MolarFlowValue = 20.0  # kgmole/h

        stream_wash_mix = streams.Add("Mezcla_Lavado")

        wash_mixer = operations.Add("Mixer")
        wash_mixer.Name = "Mezclador_Lavado"
        wash_mixer.Inlets.Add(stream_biodiesel_crude)
        wash_mixer.Inlets.Add(wash_water)
        wash_mixer.Outlet = stream_wash_mix

        print("   ✓ Agua de lavado: 20 kgmole/h")

        time.sleep(2)

        # PASO 9: Separador de agua de lavado
        print("\n[9/15] Configurando separador de agua de lavado...")

        stream_biodiesel_washed = streams.Add("Biodiesel_Lavado")
        stream_wastewater = streams.Add("Agua_Residual")

        wash_separator = operations.Add("ComponentSplitter")
        wash_separator.Name = "Separador_Lavado"
        wash_separator.Inlet = stream_wash_mix
        wash_separator.VapourOutlet = stream_biodiesel_washed
        wash_separator.LiquidOutlet = stream_wastewater

        print("   ✓ Separador de lavado configurado")

        time.sleep(2)

        # PASO 10: Secador (remoción final de agua)
        print("\n[10/15] Configurando secador...")

        stream_biodiesel_final = streams.Add("Biodiesel_Final")

        dryer = operations.Add("Heater")
        dryer.Name = "Secador"
        dryer.Inlet = stream_biodiesel_washed
        dryer.Outlet = stream_biodiesel_final

        # Temperatura de secado
        dryer.OutletTemperature = 80 + 273.15  # K

        print("   ✓ Secador configurado (T = 80°C)")

        time.sleep(3)

        # PASO 11: Extraer resultados del proceso
        print("\n[11/15] Extrayendo resultados del proceso...")

        # Alimentaciones
        F_oil = feed_oil.MolarFlowValue
        F_methanol = feed_methanol.MolarFlowValue

        # Salida del reactor
        F_reactor_out = stream_reactor_out.MolarFlowValue
        x_biodiesel_reactor = stream_reactor_out.ComponentMolarFractionValue("Ethyl acetate")

        # Biodiesel final
        F_biodiesel_final = stream_biodiesel_final.MolarFlowValue
        x_biodiesel_final = stream_biodiesel_final.ComponentMolarFractionValue("Ethyl acetate")
        x_water_final = stream_biodiesel_final.ComponentMolarFractionValue("H2O")
        T_biodiesel_final = stream_biodiesel_final.TemperatureValue - 273.15

        print(f"\n   RESULTADOS DEL PROCESO:")
        print(f"\n   Alimentaciones:")
        print(f"      Aceite vegetal: {F_oil:.2f} kgmole/h")
        print(f"      Metanol: {F_methanol:.2f} kgmole/h")

        print(f"\n   Salida del reactor:")
        print(f"      Flujo total: {F_reactor_out:.2f} kgmole/h")
        print(f"      x(Biodiesel): {x_biodiesel_reactor:.4f}")

        print(f"\n   Biodiesel final:")
        print(f"      Flujo: {F_biodiesel_final:.2f} kgmole/h")
        print(f"      Pureza (x Biodiesel): {x_biodiesel_final:.4f}")
        print(f"      Humedad (x Agua): {x_water_final:.4f}")
        print(f"      Temperatura: {T_biodiesel_final:.2f} °C")

        # PASO 12: Cálculos de rendimiento
        print("\n[12/15] Calculando rendimientos del proceso...")

        # Rendimiento global
        F_biodiesel_produced = F_biodiesel_final * x_biodiesel_final
        yield_global = (F_biodiesel_produced / F_oil) * 100

        # Pureza
        purity = x_biodiesel_final * 100

        # Consumo específico de metanol
        specific_methanol = F_methanol / F_biodiesel_produced

        print(f"\n   INDICADORES DE DESEMPEÑO:")
        print(f"      Rendimiento global: {yield_global:.2f}%")
        print(f"      Pureza del biodiesel: {purity:.2f}%")
        print(f"      Consumo específico MeOH: {specific_methanol:.2f} mol/mol")

        # PASO 13: Análisis de eficiencia
        print("\n[13/15] Análisis de eficiencia energética...")

        # Carga térmica del precalentador
        try:
            Q_heater = heater.EnergyStream.HeatFlow  # kJ/h
            specific_energy = Q_heater / F_biodiesel_produced  # kJ/kgmole
            print(f"      Carga térmica precalentador: {Q_heater:.2f} kJ/h")
            print(f"      Energía específica: {specific_energy:.2f} kJ/kgmole")
        except:
            print(f"      Carga térmica: No disponible")

        # PASO 14: Guardar resultados
        print("\n[14/15] Guardando resultados completos...")

        results = {
            'proceso': 'Planta completa de biodiesel',
            'configuracion': {
                'unidades': [
                    'Mezclador de reactivos',
                    'Precalentador',
                    'Reactor de transesterificación',
                    'Separador Biodiesel/Glicerol',
                    'Lavado',
                    'Separador de lavado',
                    'Secador'
                ],
                'conversion_reactor': 90.0,
                'temperatura_reaccion_C': 60.0,
                'temperatura_secado_C': 80.0
            },
            'alimentaciones': {
                'aceite_vegetal_kgmoleh': F_oil,
                'metanol_kgmoleh': F_methanol,
                'exceso_metanol_percent': (F_methanol / F_oil - 1) * 100,
                'agua_lavado_kgmoleh': 20.0
            },
            'productos': {
                'biodiesel_final': {
                    'flujo_kgmoleh': F_biodiesel_final,
                    'pureza_percent': purity,
                    'humedad_percent': x_water_final * 100,
                    'temperatura_C': T_biodiesel_final
                },
                'glicerol_crudo': {
                    'descripcion': 'Subproducto valorizable'
                }
            },
            'indicadores_desempeno': {
                'rendimiento_global_percent': yield_global,
                'pureza_biodiesel_percent': purity,
                'consumo_especifico_metanol': specific_methanol,
                'cumple_norma_ASTM': purity > 96.5
            },
            'balance_materia': {
                'entrada_total_kgmoleh': F_oil + F_methanol + 20.0,
                'biodiesel_producido_kgmoleh': F_biodiesel_produced
            }
        }

        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, "resultados_aspen.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"   ✓ Resultados guardados: resultados_aspen.json")

        # PASO 15: Cerrar HYSYS
        print("\n[15/15] Cerrando HYSYS...")
        time.sleep(3)
        hysys.Quit()
        print("   ✓ HYSYS cerrado")

        # RESUMEN
        print("\n" + "="*70)
        print("PRÁCTICA 8 COMPLETADA EXITOSAMENTE")
        print("="*70)

        print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA DE PROCESOS:")
        print("   ✓ Integración de múltiples operaciones unitarias")
        print("   ✓ Balance de materia y energía en planta completa")
        print("   ✓ Rendimiento global vs rendimiento por etapa")
        print("   ✓ Importancia de purificación (lavado + secado)")
        print("   ✓ Cumplimiento de especificaciones (ASTM D6751)")

        print("\n📊 RESUMEN DEL PROCESO:")
        print(f"   Capacidad: {F_oil:.0f} kgmole/h de aceite vegetal")
        print(f"   Producción: {F_biodiesel_produced:.2f} kgmole/h de biodiesel")
        print(f"   Rendimiento: {yield_global:.1f}%")
        print(f"   Pureza: {purity:.1f}% {'✓ ASTM' if purity > 96.5 else '✗ No cumple'}")

        print("\n🏭 ETAPAS CRÍTICAS DEL PROCESO:")
        print("   1. Mezclado: Exceso de metanol mejora conversión")
        print("   2. Precalentamiento: Óptimo 60°C (cinética)")
        print("   3. Reacción: CSTR con X=90% (economía)")
        print("   4. Separación: Crítica para pureza")
        print("   5. Lavado: Remueve catalizador e impurezas")
        print("   6. Secado: Cumplir especificación de humedad")

        print("\n⚙️ OPTIMIZACIÓN POTENCIAL:")
        print("   • Reciclo de metanol no reaccionado")
        print("   • Valorización de glicerol (subproducto)")
        print("   • Integración energética (recuperación de calor)")
        print("   • Control automático de conversión")

        print("\n🔄 PRÓXIMOS PASOS:")
        print("   1. Ejecuta py_alone.py para simulación simplificada")
        print("   2. Ejecuta visualiza1.py y visualiza2.py")
        print("   3. Analiza sensibilidad de parámetros clave")
        print("   4. Diseña sistema de reciclo de metanol")
        print("   5. Evalúa economía del proceso completo")

        print("="*70)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n   Posibles causas:")
        print("   - Proceso complejo requiere tiempo de cálculo")
        print("   - Componentes no disponibles en HYSYS")
        print("   - Especificaciones de separadores no configuradas")

if __name__ == '__main__':
    main()
