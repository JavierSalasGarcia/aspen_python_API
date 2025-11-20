#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 3: Cálculo de Propiedades de Corrientes (Python Puro)
===============================================================

Este script calcula propiedades de corrientes (densidad, entalpía, etc.)
usando librerías Python (thermo/CoolProp) sin ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

import os
def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 3: CORRIENTES (PYTHON PURO)")
    print("="*60)

    # Verificar librerías
    print("\n[1/5] Verificando librerías...")

    use_thermo = False
    use_coolprop = False

    try:
        from thermo.chemical import Chemical
        from thermo import ChemicalConstantsPackage, PRMIX, CEOSLiquid, CEOSGas, FlashPureVLS
        print("   ✓ Librería 'thermo' disponible")
        use_thermo = True
    except ImportError:
        print("   ✗ 'thermo' no instalada (pip install thermo)")

    try:
        from CoolProp.CoolProp import PropsSI
        print("   ✓ Librería 'CoolProp' disponible")
        use_coolprop = True
    except ImportError:
        print("   ✗ 'CoolProp' no instalada (pip install CoolProp)")

    if not use_thermo and not use_coolprop:
        print("\n   ⚠ Usando cálculos aproximados...")

    # Datos de la corriente
    print("\n[2/5] Especificaciones de la corriente:")
    print("   Componente: Methanol (100%)")
    print("   Temperatura: 25.0 °C (298.15 K)")
    print("   Presión: 101.325 kPa")
    print("   Flujo molar: 100.0 kgmole/h")

    T = 298.15  # K
    P = 101325  # Pa (101.325 kPa)
    component = "Methanol"

    # Calcular densidad
    print("\n[3/5] Calculando propiedades...")

    density = None

    if use_coolprop:
        try:
            from CoolProp.CoolProp import PropsSI
            # CoolProp usa nombres específicos
            density = PropsSI('D', 'T', T, 'P', P, 'Methanol')  # kg/m3
            print(f"   ✓ Densidad (CoolProp): {density:.2f} kg/m3")
        except Exception as e:
            print(f"   ⚠ Error con CoolProp: {e}")

    if use_thermo and density is None:
        try:
            chem = Chemical(component, T=T, P=P)
            density = chem.rho  # kg/m3
            print(f"   ✓ Densidad (thermo): {density:.2f} kg/m3")

            # Otras propiedades disponibles
            print(f"   ✓ Viscosidad: {chem.mu:.6f} Pa·s")
            print(f"   ✓ Cp (líquido): {chem.Cpl:.2f} J/(mol·K)")

        except Exception as e:
            print(f"   ⚠ Error con thermo: {e}")

    if density is None:
        # Valor de referencia para metanol líquido a 25°C
        density = 786.5  # kg/m3 (literatura)
        print(f"   ✓ Densidad (referencia): {density:.2f} kg/m3")

    # Calcular flujo másico
    print("\n[4/5] Cálculos adicionales...")

    MW = 32.04  # g/mol (metanol)
    F_molar = 100.0  # kgmole/h
    F_masico = F_molar * MW  # kg/h

    print(f"   Peso molecular: {MW:.2f} g/mol")
    print(f"   Flujo molar: {F_molar:.2f} kgmole/h")
    print(f"   Flujo másico: {F_masico:.2f} kg/h")

    # Volumen
    if density:
        V_flow = F_masico / density  # m3/h
        print(f"   Flujo volumétrico: {V_flow:.2f} m3/h")

    # Guardar resultados
    print("\n[5/5] Guardando resultados...")

    import json
    results = {
        'component': component,
        'T_C': T - 273.15,
        'T_K': T,
        'P_kPa': P / 1000,
        'F_molar_kgmoleh': F_molar,
        'F_masico_kgh': F_masico,
        'density_kgm3': density,
        'V_flow_m3h': V_flow if density else None,
        'MW_gmol': MW,
        'method': 'CoolProp' if use_coolprop else ('thermo' if use_thermo else 'referencia')
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'resultados_python.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"   ✓ Resultados guardados: resultados_python.json")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 3 (PYTHON PURO) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE:")
    print("   ✓ thermo y CoolProp calculan propiedades termodinámicas")
    print("   ✓ Requieren T, P y componente como entrada")
    print("   ✓ Proveen densidad, viscosidad, Cp, etc.")

    print("\n📊 COMPARACIÓN CON ASPEN:")
    print("   Python (thermo/CoolProp):")
    print("     + Cálculos rápidos para componentes puros")
    print("     + Bases de datos extensas")
    print("     - Modelos termodinámicos limitados para mezclas")

    print("   ASPEN HYSYS:")
    print("     + Múltiples paquetes termodinámicos (NRTL, UNIFAC, etc.)")
    print("     + Manejo completo de mezclas multi-componente")
    print("     + Cálculos flash rigurosos")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Compara con resultados de aspython.py")
    print("   2. Ejecuta visualiza1.py y visualiza2.py")
    print("   3. Continúa con Práctica 4: Mixer")

    print("="*60)

if __name__ == '__main__':
    main()
