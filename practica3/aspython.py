# Practica 3: Corrientes

import win32com.client as win32
import time

def main():
    print("PRACTICA 3: CORRIENTES")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True

        # Crear nuevo caso de simulación
        case = hysys.SimulationCases.Add()
        basis_manager = case.BasisManager

        # Configurar componentes usando ComponentLists
        comp_lists = basis_manager.ComponentLists
        comp_list = comp_lists.Add()
        components = comp_list.Components

        components.Add("Methanol")

        # Crear FluidPackage y asignar modelo termodinámico
        fluid_pkg = basis_manager.FluidPackages.Add()

        # Probar nombres de paquetes termodinámicos
        nombres_pkg = ["NRTL", "SRK", "PR", "Peng-Robinson"]
        for nombre in nombres_pkg:
            try:
                fluid_pkg.PropertyPackageName = nombre
                if fluid_pkg.PropertyPackageName == nombre:
                    break
            except:
                continue

        # Crear corriente
        flowsheet = case.Flowsheet
        streams = flowsheet.MaterialStreams
        stream1 = streams.Add("Metanol_Entrada")

        # Especificar propiedades
        stream1.ComponentMolarFractionValue("Methanol", 1.0)
        stream1.TemperatureValue = 25 + 273.15  # K
        stream1.PressureValue = 101.325          # kPa
        stream1.MolarFlowValue = 100.0           # kgmole/h

        # Esperar cálculos
        time.sleep(2)

        print(f"Corriente creada: {stream1.StreamName}")
        print(f"  T = {stream1.TemperatureValue.GetValue() - 273.15:.2f} C")
        print(f"  P = {stream1.PressureValue.GetValue():.2f} kPa")
        print(f"  F = {stream1.MolarFlowValue.GetValue():.2f} kgmole/h")
        print(f"  Densidad = {stream1.DensityValue.GetValue():.2f} kg/m3")

        time.sleep(3)
        hysys.Quit()

        print("\nCOMPLETADA! => Practica 4: Mixer")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
