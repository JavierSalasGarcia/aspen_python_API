#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 7: Comparación Reactor Batch vs CSTR (ASPEN HYSYS)
============================================================

Este script demuestra cómo comparar reactores tipo Batch y CSTR en ASPEN HYSYS,
analizando diferencias en tiempo de operación, conversión y productividad.

Batch: Operación discontinua, conversión vs tiempo
CSTR: Operación continua, conversión vs tiempo de residencia

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
    print("PRÁCTICA 7: COMPARACIÓN BATCH vs CSTR")
    print("="*60)

    try:
        # PASO 1: Iniciar HYSYS
        print("\n[1/10] Iniciando ASPEN HYSYS...")
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.ActiveDocument
        print("   ✓ HYSYS iniciado")

        # PASO 2: Configurar componentes
        print("\n[2/10] Configurando componentes...")
        fluid_pkg = case.FluidPackage
        components = fluid_pkg.Components

        components.Add("Methanol")  # Reactivo A
        components.Add("Ethanol")   # Producto B

        fluid_pkg.PropertyPackage = "NRTL"
        print("   ✓ Componentes: Methanol → Ethanol")
        print("   ✓ Paquete: NRTL")

        # PASO 3: Parámetros de reacción
        print("\n[3/10] Definiendo parámetros de reacción...")

        # Cinética de primer orden
        k = 0.5  # 1/h (constante de velocidad)
        conversion_target = 0.90  # 90% conversión objetivo

        print(f"   Reacción: A → B (1er orden)")
        print(f"   k = {k} 1/h")
        print(f"   Conversión objetivo: {conversion_target*100:.0f}%")

        flowsheet = case.Flowsheet
        streams = flowsheet.MaterialStreams
        operations = flowsheet.Operations

        # ===== CONFIGURACIÓN REACTOR BATCH =====
        print("\n[4/10] Configurando reactor BATCH...")

        # Crear corriente para batch
        batch_feed = streams.Add("Batch_Carga")
        batch_feed.ComponentMolarFractionValue("Methanol", 1.0)
        batch_feed.TemperatureValue = 60 + 273.15  # K
        batch_feed.PressureValue = 101.325  # kPa
        batch_feed.MolarFlowValue = 100.0  # kgmole (carga total)

        batch_product = streams.Add("Batch_Descarga")

        # Crear reactor batch (usando ConversionReactor)
        batch_reactor = operations.Add("ConversionReactor")
        batch_reactor.Name = "Reactor_Batch"
        batch_reactor.Feeds.Add(batch_feed)
        batch_reactor.Outlet = batch_product

        # Configurar reacción en batch
        batch_rxn_set = batch_reactor.ReactionSet
        batch_rxn = batch_rxn_set.Reactions.Add()
        batch_rxn.ComponentStoichCoeffValue("Methanol", -1.0)
        batch_rxn.ComponentStoichCoeffValue("Ethanol", 1.0)
        batch_rxn.BaseComponent = "Methanol"
        batch_rxn.Conversion = conversion_target

        print(f"   ✓ Reactor Batch configurado")
        print(f"   Carga: 100 kgmole")
        print(f"   Conversión: {conversion_target*100:.0f}%")

        # Calcular tiempo de batch
        # Para 1er orden: t = (1/k)·ln(1/(1-X))
        t_batch = (1/k) * np.log(1/(1-conversion_target))
        print(f"   Tiempo de reacción: {t_batch:.2f} h")

        time.sleep(2)

        # ===== CONFIGURACIÓN REACTOR CSTR =====
        print("\n[5/10] Configurando reactor CSTR continuo...")

        # Crear corrientes para CSTR
        cstr_feed = streams.Add("CSTR_Alimentacion")
        cstr_feed.ComponentMolarFractionValue("Methanol", 1.0)
        cstr_feed.TemperatureValue = 60 + 273.15  # K
        cstr_feed.PressureValue = 101.325  # kPa
        cstr_feed.MolarFlowValue = 100.0  # kgmole/h

        cstr_product = streams.Add("CSTR_Salida")

        # Crear reactor CSTR
        cstr_reactor = operations.Add("ConversionReactor")
        cstr_reactor.Name = "Reactor_CSTR"
        cstr_reactor.Feeds.Add(cstr_feed)
        cstr_reactor.Outlet = cstr_product

        # Configurar reacción en CSTR
        cstr_rxn_set = cstr_reactor.ReactionSet
        cstr_rxn = cstr_rxn_set.Reactions.Add()
        cstr_rxn.ComponentStoichCoeffValue("Methanol", -1.0)
        cstr_rxn.ComponentStoichCoeffValue("Ethanol", 1.0)
        cstr_rxn.BaseComponent = "Methanol"
        cstr_rxn.Conversion = conversion_target

        print(f"   ✓ Reactor CSTR configurado")
        print(f"   Flujo: 100 kgmole/h")
        print(f"   Conversión: {conversion_target*100:.0f}%")

        # Calcular tiempo de residencia CSTR
        # Para 1er orden: τ = X/(k·(1-X))
        tau_cstr = conversion_target / (k * (1 - conversion_target))
        print(f"   Tiempo de residencia: {tau_cstr:.2f} h")

        time.sleep(2)

        # PASO 6: Extraer resultados Batch
        print("\n[6/10] Extrayendo resultados del reactor BATCH...")

        batch_x_A_out = batch_product.ComponentMolarFractionValue("Methanol")
        batch_x_B_out = batch_product.ComponentMolarFractionValue("Ethanol")
        batch_F_out = batch_product.MolarFlowValue

        print(f"   Producto Batch:")
        print(f"      x(A) = {batch_x_A_out:.4f}")
        print(f"      x(B) = {batch_x_B_out:.4f}")
        print(f"      Conversión = {conversion_target*100:.1f}%")

        # PASO 7: Extraer resultados CSTR
        print("\n[7/10] Extrayendo resultados del reactor CSTR...")

        cstr_x_A_out = cstr_product.ComponentMolarFractionValue("Methanol")
        cstr_x_B_out = cstr_product.ComponentMolarFractionValue("Ethanol")
        cstr_F_out = cstr_product.MolarFlowValue

        print(f"   Producto CSTR:")
        print(f"      x(A) = {cstr_x_A_out:.4f}")
        print(f"      x(B) = {cstr_x_B_out:.4f}")
        print(f"      Conversión = {conversion_target*100:.1f}%")

        # PASO 8: Análisis comparativo
        print("\n[8/10] Análisis comparativo de productividad...")

        # Productividad
        # Batch: moles producto / tiempo total (incluyendo carga/descarga)
        t_down = 1.0  # h (tiempo muerto: carga + descarga + limpieza)
        t_cycle_batch = t_batch + t_down
        productivity_batch = (100.0 * conversion_target) / t_cycle_batch

        # CSTR: moles producto / tiempo (continuo)
        productivity_cstr = 100.0 * conversion_target  # kgmole/h

        print(f"\n   REACTOR BATCH:")
        print(f"      Tiempo de reacción: {t_batch:.2f} h")
        print(f"      Tiempo muerto: {t_down:.2f} h")
        print(f"      Tiempo de ciclo total: {t_cycle_batch:.2f} h")
        print(f"      Productividad: {productivity_batch:.2f} kgmole/h")

        print(f"\n   REACTOR CSTR:")
        print(f"      Tiempo de residencia: {tau_cstr:.2f} h")
        print(f"      Productividad: {productivity_cstr:.2f} kgmole/h")

        ratio_productivity = productivity_cstr / productivity_batch
        print(f"\n   Ratio productividad (CSTR/Batch): {ratio_productivity:.2f}×")

        # PASO 9: Guardar resultados
        print("\n[9/10] Guardando resultados comparativos...")

        results = {
            'parametros_cineticos': {
                'k_1h': k,
                'conversion_target': conversion_target * 100
            },
            'batch_reactor': {
                'tipo': 'Discontinuo',
                'carga_kgmole': 100.0,
                'tiempo_reaccion_h': t_batch,
                'tiempo_muerto_h': t_down,
                'tiempo_ciclo_h': t_cycle_batch,
                'conversion_percent': conversion_target * 100,
                'x_A_salida': batch_x_A_out,
                'x_B_salida': batch_x_B_out,
                'productividad_kgmoleh': productivity_batch
            },
            'cstr_reactor': {
                'tipo': 'Continuo',
                'flujo_kgmoleh': 100.0,
                'tiempo_residencia_h': tau_cstr,
                'conversion_percent': conversion_target * 100,
                'x_A_salida': cstr_x_A_out,
                'x_B_salida': cstr_x_B_out,
                'productividad_kgmoleh': productivity_cstr
            },
            'comparacion': {
                'ratio_tiempos': tau_cstr / t_batch,
                'ratio_productividad': ratio_productivity,
                'ventaja_cstr': 'Operación continua, mayor productividad',
                'ventaja_batch': 'Flexibilidad, productos especiales'
            }
        }

        output_file = '/home/user/aspen_python_API/practica7/resultados_aspen.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"   ✓ Resultados guardados: resultados_aspen.json")

        # PASO 10: Cerrar HYSYS
        print("\n[10/10] Cerrando HYSYS...")
        time.sleep(2)
        case.SaveRequired = False
        hysys.Quit()
        print("   ✓ HYSYS cerrado")

        # RESUMEN
        print("\n" + "="*60)
        print("PRÁCTICA 7 COMPLETADA EXITOSAMENTE")
        print("="*60)

        print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA:")
        print("   ✓ BATCH: Operación discontinua, t = (1/k)·ln(1/(1-X))")
        print("   ✓ CSTR: Operación continua, τ = X/(k·(1-X))")
        print("   ✓ τ_CSTR > t_Batch (para misma conversión)")
        print("   ✓ CSTR tiene mayor productividad (sin tiempo muerto)")
        print("   ✓ Batch es más flexible para cambios de producto")

        print("\n📊 ANÁLISIS COMPARATIVO:")
        print(f"   Para alcanzar X = {conversion_target*100:.0f}%:")
        print(f"   • Batch requiere: {t_batch:.2f} h de reacción")
        print(f"   • CSTR requiere: {tau_cstr:.2f} h de residencia")
        print(f"   • CSTR necesita {(tau_cstr/t_batch):.2f}× más tiempo")
        print(f"   • Pero CSTR produce {ratio_productivity:.2f}× más (continuo)")

        print("\n🏭 SELECCIÓN DE REACTOR:")
        print("   Usar BATCH cuando:")
        print("   • Producción pequeña o intermitente")
        print("   • Múltiples productos (flexibilidad)")
        print("   • Productos de alto valor")
        print("\n   Usar CSTR cuando:")
        print("   • Producción continua a gran escala")
        print("   • Producto único o pocos productos")
        print("   • Maximizar productividad")

        print("\n🔄 PRÓXIMOS PASOS:")
        print("   1. Ejecuta py_alone.py para análisis con scipy")
        print("   2. Grafica conversión vs tiempo (ambos reactores)")
        print("   3. Analiza efecto de tiempo muerto en Batch")
        print("   4. Continúa con Práctica 8: Planta de Biodiesel")

        print("="*60)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
