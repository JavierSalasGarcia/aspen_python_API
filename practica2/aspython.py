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

        # Configurar componentes
        fluid_pkg = case.Flowsheet.FluidPackage
        components = fluid_pkg.Components

        components.Add("Methanol")
        components.Add("Water")
        print("[2/4] Componentes agregados: Methanol, Water")

        # Paquete termodinamico
        fluid_pkg.PropertyPackage = "NRTL"
        print("[3/4] Paquete: NRTL")

        # Extraer propiedades
        for i in range(components.Count):
            comp = components.Item(i)
            print(f"\n{comp.ComponentName}:")
            print(f"  Tc = {comp.CriticalTemperature:.2f} K")
            print(f"  Pc = {comp.CriticalPressure:.2f} kPa")
            print(f"  MW = {comp.MolecularWeight:.2f} g/mol")

        print("\n[4/4] Cerrando...")
        time.sleep(3)
        case.SaveRequired = False
        hysys.Quit()

        print("\nPRACTICA 2 COMPLETADA!")
        print("Proxima: Practica 3 - Corrientes")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    main()
