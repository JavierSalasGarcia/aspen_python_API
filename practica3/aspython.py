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

        # Componentes
        fluid_pkg = case.FluidPackage
        fluid_pkg.Components.Add("Methanol")
        fluid_pkg.PropertyPackage = "NRTL"

        # Crear corriente
        flowsheet = case.Flowsheet
        streams = flowsheet.MaterialStreams
        stream1 = streams.Add("Metanol_Entrada")

        # Especificar propiedades
        stream1.ComponentMolarFractionValue("Methanol", 1.0)
        stream1.TemperatureValue = 25 + 273.15  # K
        stream1.PressureValue = 101.325          # kPa
        stream1.MolarFlowValue = 100.0           # kgmole/h

        print(f"Corriente creada: {stream1.StreamName}")
        print(f"  T = {stream1.TemperatureValue - 273.15:.2f} C")
        print(f"  P = {stream1.PressureValue:.2f} kPa")
        print(f"  F = {stream1.MolarFlowValue:.2f} kgmole/h")
        print(f"  Densidad = {stream1.DensityValue:.2f} kg/m3")

        time.sleep(3)
        case.SaveRequired = False
        hysys.Quit()

        print("\nCOMPLETADA! => Practica 4: Mixer")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    main()
