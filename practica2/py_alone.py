#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Práctica 2: Propiedades de Componentes (Python Puro)
=====================================================

Este script obtiene propiedades críticas de componentes usando librerías
Python (chemicals/thermo) sin necesidad de ASPEN HYSYS.

Autor: Salas-García, et. al
Fecha: 2025-01-15
"""

def main():
    """Función principal"""

    print("="*60)
    print("PRÁCTICA 2: PROPIEDADES DE COMPONENTES (PYTHON PURO)")
    print("="*60)

    # Verificar disponibilidad de librerías
    print("\n[1/4] Verificando librerías...")

    try:
        from chemicals import critical_point, molecular_weight, search_chemical
        print("   ✓ Librería 'chemicals' disponible")
        use_chemicals = True
    except ImportError:
        print("   ✗ Librería 'chemicals' no instalada")
        print("   Instalar con: pip install chemicals")
        use_chemicals = False

    if not use_chemicals:
        print("\n   Usando valores de referencia de la literatura...")

    # Componentes a analizar
    components = ["Methanol", "Water"]

    print(f"\n[2/4] Componentes a analizar: {', '.join(components)}")

    # Extraer propiedades
    print("\n[3/4] Extrayendo propiedades críticas...")

    results = {}

    if use_chemicals:
        for comp_name in components:
            try:
                # Buscar CAS number
                cas = search_chemical(comp_name)

                # Obtener propiedades críticas
                Tc, Pc, Vc = critical_point(cas)
                MW = molecular_weight(cas)

                results[comp_name] = {
                    'Tc': Tc,  # K
                    'Pc': Pc / 1000,  # kPa (convertir de Pa)
                    'MW': MW  # g/mol
                }

                print(f"\n   {comp_name}:")
                print(f"      Tc = {Tc:.2f} K")
                print(f"      Pc = {Pc/1000:.2f} kPa")
                print(f"      MW = {MW:.2f} g/mol")

            except Exception as e:
                print(f"   ⚠ Error obteniendo datos de {comp_name}: {e}")

    else:
        # Valores de referencia (NIST, Perry's Handbook)
        reference_data = {
            "Methanol": {
                'Tc': 512.64,  # K
                'Pc': 8084.0,  # kPa
                'MW': 32.04  # g/mol
            },
            "Water": {
                'Tc': 647.10,  # K
                'Pc': 22064.0,  # kPa
                'MW': 18.015  # g/mol
            }
        }

        for comp_name, props in reference_data.items():
            results[comp_name] = props
            print(f"\n   {comp_name}:")
            print(f"      Tc = {props['Tc']:.2f} K")
            print(f"      Pc = {props['Pc']:.2f} kPa")
            print(f"      MW = {props['MW']:.2f} g/mol")

    # Guardar resultados para visualización
    print("\n[4/4] Guardando resultados...")

    import json
    output_file = '/home/user/aspen_python_API/practica2/resultados_python.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"   ✓ Resultados guardados en: resultados_python.json")

    # RESUMEN
    print("\n" + "="*60)
    print("PRÁCTICA 2 (PYTHON PURO) COMPLETADA")
    print("="*60)

    print("\n💡 CONCEPTOS CLAVE:")
    print("   ✓ Librería 'chemicals' contiene base de datos de 20,000+ compuestos")
    print("   ✓ Propiedades críticas son esenciales para termodinámica")
    print("   ✓ Python puede acceder a datos sin necesidad de ASPEN")

    print("\n📊 COMPARACIÓN:")
    print("   ASPEN: Usa base de datos interna validada")
    print("   Python (chemicals): Usa DIPPR, NIST, literatura")
    print("   Desviación esperada: < 1% para compuestos comunes")

    print("\n🔄 PRÓXIMOS PASOS:")
    print("   1. Ejecuta aspython.py y compara resultados")
    print("   2. Ejecuta visualiza1.py y visualiza2.py")
    print("   3. Continúa con Práctica 3: Corrientes")

    print("="*60)

if __name__ == '__main__':
    main()
