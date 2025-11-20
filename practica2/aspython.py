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

        # Acceder al Basis Manager
        print("   → Accediendo al Basis Manager...")
        basis = case.BasisManager

        # Obtener o crear FluidPackage
        print("   → Obteniendo FluidPackages...")
        fluid_packages = basis.FluidPackages

        # Si no hay FluidPackages, crear uno
        if fluid_packages.Count == 0:
            print("   → Creando nuevo FluidPackage...")
            fluid_pkg = fluid_packages.Add()
        else:
            print("   → Usando FluidPackage existente...")
            fluid_pkg = fluid_packages.Item(0)

        # Acceder a Components
        print("   → Accediendo a Components...")
        components = fluid_pkg.Components

        print("\n[2/4] Agregando componentes...")
        print("   → Agregando Methanol...")
        components.Add("Methanol")
        print("   ✓ Methanol agregado")

        print("   → Agregando Water...")
        components.Add("Water")
        print("   ✓ Water agregado")

        print("\n[3/4] Configurando componentes en el Flowsheet...")
        # El FluidPackage ya está activo, no necesitamos asignarlo manualmente
        print("   ✓ FluidPackage configurado y listo para usar")

        # Extraer propiedades
        print("\n[4/4] Extrayendo propiedades de componentes...")
        for i in range(components.Count):
            comp = components.Item(i)
            print(f"\n   {comp.ComponentName}:")
            print(f"     Tc = {comp.CriticalTemperature:.2f} K")
            print(f"     Pc = {comp.CriticalPressure:.2f} kPa")
            print(f"     MW = {comp.MolecularWeight:.2f} g/mol")

        print("\n[5/5] Cerrando...")
        time.sleep(2)
        case.SaveRequired = False
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
