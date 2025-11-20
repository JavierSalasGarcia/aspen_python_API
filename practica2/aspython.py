# Practica 2: Componentes y Paquetes

import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: COMPONENTES Y PAQUETES")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True

        # Crear nuevo caso de simulación
        case = hysys.SimulationCases.Add()
        print("\n[1/4] HYSYS iniciado y caso creado")

        # Acceder al BasisManager (donde viven los componentes y paquetes)
        print("   → Accediendo al Basis Manager...")
        basis_manager = case.BasisManager

        print("\n[2/4] Creando Fluid Package...")
        # Primero crear el FluidPackage
        fluid_packages = basis_manager.FluidPackages

        if fluid_packages.Count == 0:
            print("   → Creando nuevo FluidPackage...")
            fluid_pkg = fluid_packages.Add()
        else:
            print("   → Usando FluidPackage existente...")
            fluid_pkg = fluid_packages.Item(0)

        print("\n[3/4] Agregando componentes al FluidPackage...")
        # Ahora agregar componentes al FluidPackage
        components = fluid_pkg.Components

        print("   → Agregando Methanol...")
        try:
            components.Add("Methanol")
            print("   ✓ Methanol agregado")
        except Exception as e:
            print(f"   ✗ Error al agregar Methanol: {e}")

        print("   → Agregando Water...")
        try:
            components.Add("Water")
            print("   ✓ Water agregado")
        except Exception as e:
            print(f"   ✗ Error al agregar Water: {e}")

        print(f"   → Componentes en FluidPackage: {components.Count}")

        # Extraer propiedades
        print("\n[4/4] Extrayendo propiedades de componentes...")

        if components.Count == 0:
            print("   ⚠ No hay componentes en el FluidPackage")
        else:
            for i in range(components.Count):
                comp = components.Item(i)
                print(f"\n   {comp.ComponentName}:")
                try:
                    print(f"     Tc = {comp.CriticalTemperature:.2f} K")
                    print(f"     Pc = {comp.CriticalPressure:.2f} kPa")
                    print(f"     MW = {comp.MolecularWeight:.2f} g/mol")
                except Exception as e:
                    print(f"     ⚠ Error al obtener propiedades: {e}")

        print("\n[5/5] Cerrando...")
        time.sleep(2)
        # No guardar cambios al cerrar
        hysys.Quit()

        print("\n" + "="*60)
        print("PRACTICA 2 COMPLETADA!")
        print("="*60)
        print("\nPróxima: Practica 3 - Corrientes")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print(f"   Tipo: {type(e).__name__}")
        if hasattr(e, 'args') and len(e.args) > 0:
            print(f"   Código COM: {e.args[0] if isinstance(e.args[0], int) else 'N/A'}")

        print("\n💡 SOLUCIONES:")
        print("   1. Asegúrate de que HYSYS está completamente abierto")
        print("   2. Intenta cerrar HYSYS y ejecutar el script de nuevo")
        print("   3. Verifica que tienes licencia activa de HYSYS")

        try:
            hysys.Quit()
        except:
            pass

if __name__ == '__main__':
    main()
