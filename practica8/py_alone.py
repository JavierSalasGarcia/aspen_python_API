#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 8: Planta Completa de Biodiesel - Simulación Simplificada (Python Puro)
==================================================================================

Este script simula una planta completa de biodiesel usando balances de materia
secuenciales en Python puro, sin ASPEN HYSYS.

Etapas:
1. Mezclador
2. Reactor (conversión fija)
3. Separador primario
4. Lavado
5. Secado

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import numpy as np
import json

def main():
    """Función principal"""

    print("="*70)
    print("PRÁCTICA 8: PLANTA DE BIODIESEL (PYTHON PURO)")
    print("="*70)

    # PASO 1: Especificaciones del proceso
    print("\n[1/7] Definiendo especificaciones del proceso...")

    # Parámetros de diseño
    conversion_reactor = 0.90  # 90%
    efficiency_separation = 0.98  # 98%
    efficiency_washing = 0.95  # 95%
    efficiency_drying = 0.99  # 99%

    print(f"   Parámetros de diseño:")
    print(f"      Conversión en reactor: {conversion_reactor*100:.0f}%")
    print(f"      Eficiencia de separación: {efficiency_separation*100:.0f}%")
    print(f"      Eficiencia de lavado: {efficiency_washing*100:.0f}%")
    print(f"      Eficiencia de secado: {efficiency_drying*100:.0f}%")

    # PASO 2: Alimentaciones
    print("\n[2/7] Configurando alimentaciones...")

    # Corrientes de entrada
    F_oil = 100.0  # kgmole/h (triglicérido/aceite)
    F_methanol = 120.0  # kgmole/h (20% exceso)
    F_wash_water = 20.0  # kgmole/h

    stoich_ratio = 1.0  # Relación estequiométrica 1:1 (simplificada)
    excess_methanol = (F_methanol / F_oil) / stoich_ratio - 1

    print(f"\n   Alimentaciones:")
    print(f"      Aceite vegetal (triglicérido): {F_oil:.2f} kgmole/h")
    print(f"      Metanol: {F_methanol:.2f} kgmole/h")
    print(f"      Exceso de metanol: {excess_methanol*100:.1f}%")
    print(f"      Agua de lavado: {F_wash_water:.2f} kgmole/h")

    # PASO 3: Mezclador
    print("\n[3/7] Etapa 1: Mezclador de reactivos...")

    # Balance de materia del mezclador
    F_mixer_out = F_oil + F_methanol
    x_oil_mixer = F_oil / F_mixer_out
    x_methanol_mixer = F_methanol / F_mixer_out

    print(f"\n   Salida del mezclador:")
    print(f"      Flujo total: {F_mixer_out:.2f} kgmole/h")
    print(f"      x(Aceite): {x_oil_mixer:.4f}")
    print(f"      x(Metanol): {x_methanol_mixer:.4f}")

    # PASO 4: Reactor de transesterificación
    print("\n[4/7] Etapa 2: Reactor de transesterificación...")

    # Estequiometría simplificada: Oil + MeOH → Biodiesel + Glycerol
    # Coeficientes estequiométricos: -1, -1, +1, +1

    # Reactivo limitante (aceite, ya que metanol está en exceso)
    xi = conversion_reactor * F_oil  # Extent de reacción

    # Flujos de salida del reactor
    F_oil_reactor = F_oil - xi
    F_methanol_reactor = F_methanol - xi
    F_biodiesel_reactor = xi
    F_glycerol_reactor = xi

    F_reactor_out = F_oil_reactor + F_methanol_reactor + F_biodiesel_reactor + F_glycerol_reactor

    # Composiciones
    x_oil_reactor = F_oil_reactor / F_reactor_out
    x_methanol_reactor = F_methanol_reactor / F_reactor_out
    x_biodiesel_reactor = F_biodiesel_reactor / F_reactor_out
    x_glycerol_reactor = F_glycerol_reactor / F_reactor_out

    print(f"\n   Reacción: Aceite + Metanol → Biodiesel + Glicerol")
    print(f"   Conversión: {conversion_reactor*100:.0f}%")
    print(f"   Extent de reacción: {xi:.2f} kgmole/h")

    print(f"\n   Salida del reactor:")
    print(f"      Flujo total: {F_reactor_out:.2f} kgmole/h")
    print(f"      Aceite sin reaccionar: {F_oil_reactor:.2f} kgmole/h")
    print(f"      Metanol sin reaccionar: {F_methanol_reactor:.2f} kgmole/h")
    print(f"      Biodiesel producido: {F_biodiesel_reactor:.2f} kgmole/h")
    print(f"      Glicerol producido: {F_glycerol_reactor:.2f} kgmole/h")

    # PASO 5: Separador primario (Biodiesel/Glicerol)
    print("\n[5/7] Etapa 3: Separador Biodiesel/Glicerol...")

    # Asumimos separación por densidad
    # Fase liviana (biodiesel): Biodiesel + Metanol + algo de Aceite
    # Fase pesada (glicerol): Glicerol + algo de Biodiesel

    # Eficiencia de separación
    split_biodiesel_to_light = efficiency_separation  # 98% del biodiesel va a fase liviana
    split_glycerol_to_heavy = efficiency_separation   # 98% del glicerol va a fase pesada
    split_methanol_to_light = 0.90  # 90% del metanol va a fase liviana
    split_oil_to_light = 0.95  # 95% del aceite va a fase liviana

    # Fase liviana (biodiesel crudo)
    F_biodiesel_to_light = F_biodiesel_reactor * split_biodiesel_to_light
    F_glycerol_to_light = F_glycerol_reactor * (1 - split_glycerol_to_heavy)
    F_methanol_to_light = F_methanol_reactor * split_methanol_to_light
    F_oil_to_light = F_oil_reactor * split_oil_to_light

    F_light = F_biodiesel_to_light + F_glycerol_to_light + F_methanol_to_light + F_oil_to_light

    # Fase pesada (glicerol crudo)
    F_biodiesel_to_heavy = F_biodiesel_reactor * (1 - split_biodiesel_to_light)
    F_glycerol_to_heavy = F_glycerol_reactor * split_glycerol_to_heavy
    F_methanol_to_heavy = F_methanol_reactor * (1 - split_methanol_to_light)
    F_oil_to_heavy = F_oil_reactor * (1 - split_oil_to_light)

    F_heavy = F_biodiesel_to_heavy + F_glycerol_to_heavy + F_methanol_to_heavy + F_oil_to_heavy

    print(f"\n   Separación por densidad:")
    print(f"      Fase liviana (biodiesel crudo): {F_light:.2f} kgmole/h")
    print(f"         • Biodiesel: {F_biodiesel_to_light:.2f} kgmole/h")
    print(f"         • Metanol: {F_methanol_to_light:.2f} kgmole/h")
    print(f"      Fase pesada (glicerol crudo): {F_heavy:.2f} kgmole/h")
    print(f"         • Glicerol: {F_glycerol_to_heavy:.2f} kgmole/h")

    # PASO 6: Lavado
    print("\n[6/7] Etapa 4-5: Lavado y separación de agua...")

    # Mezclado con agua de lavado
    F_wash_mix = F_light + F_wash_water

    # Separación después de lavado
    # El agua remueve impurezas (metanol, glicerol residual)
    removal_methanol = efficiency_washing  # 95% del metanol se remueve
    removal_glycerol = efficiency_washing  # 95% del glicerol se remueve

    # Biodiesel lavado
    F_biodiesel_washed = F_biodiesel_to_light
    F_methanol_washed = F_methanol_to_light * (1 - removal_methanol)
    F_glycerol_washed = F_glycerol_to_light * (1 - removal_glycerol)
    F_oil_washed = F_oil_to_light
    F_water_washed = F_wash_water * 0.02  # 2% de agua queda

    F_washed = F_biodiesel_washed + F_methanol_washed + F_glycerol_washed + F_oil_washed + F_water_washed

    # Agua residual
    F_methanol_removed = F_methanol_to_light * removal_methanol
    F_glycerol_removed = F_glycerol_to_light * removal_glycerol
    F_wastewater = F_wash_water * 0.98 + F_methanol_removed + F_glycerol_removed

    print(f"\n   Después del lavado:")
    print(f"      Biodiesel lavado: {F_washed:.2f} kgmole/h")
    print(f"      Agua residual: {F_wastewater:.2f} kgmole/h")
    print(f"      Metanol removido: {F_methanol_removed:.2f} kgmole/h")
    print(f"      Glicerol removido: {F_glycerol_removed:.2f} kgmole/h")

    # PASO 7: Secado
    print("\n[7/7] Etapa 6: Secado (remoción de humedad)...")

    # Secado remueve agua residual
    F_water_removed = F_water_washed * efficiency_drying

    # Biodiesel final
    F_biodiesel_final = F_biodiesel_washed
    F_methanol_final = F_methanol_washed
    F_glycerol_final = F_glycerol_washed
    F_oil_final = F_oil_washed
    F_water_final = F_water_washed * (1 - efficiency_drying)

    F_final = F_biodiesel_final + F_methanol_final + F_glycerol_final + F_oil_final + F_water_final

    # Composiciones finales
    x_biodiesel_final = F_biodiesel_final / F_final
    x_methanol_final = F_methanol_final / F_final
    x_glycerol_final = F_glycerol_final / F_final
    x_oil_final = F_oil_final / F_final
    x_water_final = F_water_final / F_final

    # Pureza (biodiesel sobre total)
    purity = x_biodiesel_final * 100

    print(f"\n   BIODIESEL FINAL:")
    print(f"      Flujo total: {F_final:.2f} kgmole/h")
    print(f"      Composición:")
    print(f"         • Biodiesel: {x_biodiesel_final*100:.2f}% ({F_biodiesel_final:.2f} kgmole/h)")
    print(f"         • Metanol: {x_methanol_final*100:.4f}%")
    print(f"         • Glicerol: {x_glycerol_final*100:.4f}%")
    print(f"         • Aceite: {x_oil_final*100:.4f}%")
    print(f"         • Agua: {x_water_final*100:.4f}%")
    print(f"\n      PUREZA TOTAL: {purity:.2f}%")

    # Análisis de rendimiento global
    print("\n" + "-"*70)
    print("ANÁLISIS DE RENDIMIENTO GLOBAL")
    print("-"*70)

    # Rendimiento global
    yield_global = (F_biodiesel_final / F_oil) * 100

    # Pérdidas en cada etapa
    loss_reactor = (1 - conversion_reactor) * 100
    loss_separation = F_biodiesel_to_heavy / F_biodiesel_reactor * 100
    loss_washing = 0  # No se pierde biodiesel en lavado
    loss_drying = 0   # No se pierde biodiesel en secado

    # Consumos específicos
    specific_methanol = F_methanol / F_biodiesel_final
    specific_water = F_wash_water / F_biodiesel_final

    print(f"\n   Rendimiento global: {yield_global:.2f}%")
    print(f"   Pureza del producto: {purity:.2f}%")
    print(f"\n   Pérdidas por etapa:")
    print(f"      Reactor (conversión): {loss_reactor:.2f}%")
    print(f"      Separación: {loss_separation:.2f}%")
    print(f"      Lavado: {loss_washing:.2f}%")
    print(f"      Secado: {loss_drying:.2f}%")
    print(f"\n   Consumos específicos:")
    print(f"      Metanol: {specific_methanol:.2f} mol/mol biodiesel")
    print(f"      Agua de lavado: {specific_water:.2f} mol/mol biodiesel")

    # Cumplimiento de norma ASTM D6751
    astm_compliant = (purity >= 96.5 and x_water_final*100 <= 0.05 and x_glycerol_final*100 <= 0.02)

    print(f"\n   Cumplimiento ASTM D6751:")
    print(f"      Pureza ≥ 96.5%: {'✓' if purity >= 96.5 else '✗'} ({purity:.2f}%)")
    print(f"      Agua ≤ 0.05%: {'✓' if x_water_final*100 <= 0.05 else '✗'} ({x_water_final*100:.4f}%)")
    print(f"      Glicerol ≤ 0.02%: {'✓' if x_glycerol_final*100 <= 0.02 else '✗'} ({x_glycerol_final*100:.4f}%)")
    print(f"      RESULTADO: {'✓ CUMPLE' if astm_compliant else '✗ NO CUMPLE'}")

    # Guardar resultados
    results = {
        'proceso': 'Planta completa de biodiesel (Python simplificado)',
        'configuracion': {
            'conversion_reactor': conversion_reactor * 100,
            'eficiencia_separacion': efficiency_separation * 100,
            'eficiencia_lavado': efficiency_washing * 100,
            'eficiencia_secado': efficiency_drying * 100
        },
        'alimentaciones': {
            'aceite_vegetal_kgmoleh': F_oil,
            'metanol_kgmoleh': F_methanol,
            'exceso_metanol_percent': excess_methanol * 100,
            'agua_lavado_kgmoleh': F_wash_water
        },
        'productos': {
            'biodiesel_final': {
                'flujo_total_kgmoleh': F_final,
                'flujo_biodiesel_kgmoleh': F_biodiesel_final,
                'pureza_percent': purity,
                'x_biodiesel': x_biodiesel_final,
                'x_metanol': x_methanol_final,
                'x_glycerol': x_glycerol_final,
                'x_aceite': x_oil_final,
                'x_agua': x_water_final
            },
            'glicerol_crudo': {
                'flujo_kgmoleh': F_heavy,
                'flujo_glicerol_kgmoleh': F_glycerol_to_heavy
            },
            'agua_residual': {
                'flujo_kgmoleh': F_wastewater
            }
        },
        'indicadores_desempeno': {
            'rendimiento_global_percent': yield_global,
            'pureza_percent': purity,
            'consumo_especifico_metanol': specific_methanol,
            'consumo_especifico_agua': specific_water,
            'cumple_ASTM_D6751': astm_compliant
        },
        'perdidas_por_etapa': {
            'reactor_percent': loss_reactor,
            'separacion_percent': loss_separation,
            'lavado_percent': loss_washing,
            'secado_percent': loss_drying
        },
        'balance_materia': {
            'entrada_total_kgmoleh': F_oil + F_methanol + F_wash_water,
            'biodiesel_final_kgmoleh': F_biodiesel_final,
            'glicerol_kgmoleh': F_glycerol_to_heavy,
            'agua_residual_kgmoleh': F_wastewater
        }
    }

    output_file = '/home/user/aspen_python_API/practica8/resultados_python.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n   ✓ Resultados guardados: resultados_python.json")

    # RESUMEN
    print("\n" + "="*70)
    print("PRÁCTICA 8 (PYTHON PURO) COMPLETADA")
    print("="*70)

    print("\n💡 CONCEPTOS CLAVE DE INGENIERÍA:")
    print("   ✓ Simulación secuencial de operaciones unitarias")
    print("   ✓ Balance de materia en cada etapa")
    print("   ✓ Eficiencias de separación y purificación")
    print("   ✓ Rendimiento global = Π(rendimientos parciales)")
    print("   ✓ Cumplimiento de especificaciones (ASTM)")

    print("\n📊 RESUMEN DEL PROCESO:")
    print(f"   Entrada: {F_oil:.0f} kgmole/h de aceite vegetal")
    print(f"   Salida: {F_biodiesel_final:.2f} kgmole/h de biodiesel")
    print(f"   Rendimiento: {yield_global:.1f}%")
    print(f"   Pureza: {purity:.1f}% {'✓' if astm_compliant else '✗'}")

    print("\n🔬 COMPARACIÓN CON ASPEN:")
    print("   Python (simplificado):")
    print("   + Rápido y transparente")
    print("   + Comprensión de fundamentos")
    print("   - Propiedades simplificadas")
    print("   - No incluye termodinámica rigurosa")
    print("\n   ASPEN HYSYS:")
    print("   + Modelos termodinámicos precisos")
    print("   + Propiedades reales")
    print("   + Validado industrialmente")
    print("   - Requiere licencia y entrenamiento")

    print("\n⚙️ MEJORAS POTENCIALES:")
    print("   • Implementar reciclo de metanol no reaccionado")
    print("   • Optimizar exceso de metanol (minimizar costo)")
    print("   • Análisis económico (CAPEX + OPEX)")
    print("   • Control de calidad en línea")
    print("   • Valorización de glicerol (mercado)")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Compara con resultados de aspython.py")
    print("   2. Ejecuta visualiza1.py y visualiza2.py")
    print("   3. Diseña sistema de reciclo completo")
    print("   4. Realiza análisis de sensibilidad")
    print("   5. Evalúa viabilidad económica del proceso")

    print("\n🎓 APLICACIONES INDUSTRIALES:")
    print("   Este tipo de simulación se usa para:")
    print("   • Diseño preliminar de plantas")
    print("   • Optimización de procesos existentes")
    print("   • Entrenamiento de operadores")
    print("   • Evaluación de cambios de proceso")
    print("   • Estudios de factibilidad técnico-económica")

    print("="*70)

if __name__ == '__main__':
    main()
