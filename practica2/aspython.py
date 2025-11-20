import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: COMPONENTES Y PAQUETES (FINAL)")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.SimulationCases.Add()
        basis_manager = case.BasisManager

        print("\n[1/4] Creando Fluid Package...")
        fluid_pkg = basis_manager.FluidPackages.Add()

        # --- CORRECCIÓN 1: Usar ComponentList ---
        print("   → Accediendo a la lista de componentes interna...")
        # No usamos .Components, usamos .ComponentList
        comp_list = fluid_pkg.ComponentList

        print("   → Agregando Methanol...")
        comp_list.Add("Methanol")

        print("   → Agregando Water...")
        comp_list.Add("Water")

        # Verificamos el contador en la lista, no en el paquete
        print(f"   ✓ Componentes en la lista: {comp_list.Count}")

        print("\n[2/4] Configurando Modelo Termodinámico...")
        # Tu código de "Fuerza Bruta" que funcionó bien:
        nombres = ["Peng-Robinson", "PR", "SRK", "Soave-Redlich-Kwong"]
        asignado = False

        for nombre in nombres:
            try:
                fluid_pkg.PropertyPackageName = nombre
                if fluid_pkg.PropertyPackageName == nombre:
                    print(f"   ✓ Modelo asignado: {nombre}")
                    asignado = True
                    break
            except:
                continue

        print("\n[3/4] Extrayendo propiedades...")
        # Usamos la lista para iterar
        count = comp_list.Count

        for i in range(count):
            # --- CORRECCIÓN 2: Propiedades correctas ---
            comp = comp_list.Item(i)

            # La propiedad es .Name, no .ComponentName
            print(f"\n   Componente: {comp.Name}")

            try:
                # Nota: A veces las propiedades directas como CriticalTemperature
                # pueden fallar dependiendo de la versión. Si fallan, avísame.
                print(f"     Tc: {comp.CriticalTemperature} K")
                print(f"     Pc: {comp.CriticalPressure} kPa")
                print(f"     MW: {comp.MolecularWeight}")
            except Exception as prop_err:
                print(f"     ⚠ No se pudieron leer detalles físicos: {prop_err}")

        print("\n[4/4] Cerrando con éxito...")
        time.sleep(2)
        hysys.Quit()
        print("="*60)

    except Exception as e:
        print(f"\n✗ ERROR FATAL: {e}")
        # Si falla, intentamos cerrar HYSYS para no dejar procesos colgados
        try:
            hysys.Quit()
        except:
            pass

if __name__ == '__main__':
    main()
