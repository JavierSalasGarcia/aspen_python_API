import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: COMPONENTES Y PAQUETES (DEBUG API)")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.SimulationCases.Add()
        basis_manager = case.BasisManager

        print("\n[DEBUG] Explorando estructura del BasisManager...")

        # Intentar diferentes rutas para agregar componentes
        print("\n[Intento 1] Buscando lista global de componentes...")
        try:
            # Muchas versiones de HYSYS tienen Components directamente en BasisManager
            global_comps = basis_manager.Components
            print(f"   ✓ basis_manager.Components accesible")
            print(f"   → Count actual: {global_comps.Count}")

            print("\n   → Intentando agregar Methanol a lista global...")
            global_comps.Add("Methanol")
            print(f"   → Count después de Methanol: {global_comps.Count}")

            print("   → Intentando agregar Water a lista global...")
            global_comps.Add("Water")
            print(f"   → Count después de Water: {global_comps.Count}")

            # Si llegamos aquí, funcionó
            if global_comps.Count > 0:
                print("\n   ✓ ÉXITO: Componentes agregados a lista global")

                # Ahora crear el FluidPackage
                print("\n[2/4] Creando Fluid Package...")
                fluid_pkg = basis_manager.FluidPackages.Add()

                print("\n[3/4] Configurando Modelo Termodinámico...")
                nombres = ["Peng-Robinson", "PR", "SRK", "Soave-Redlich-Kwong"]

                for nombre in nombres:
                    try:
                        fluid_pkg.PropertyPackageName = nombre
                        if fluid_pkg.PropertyPackageName == nombre:
                            print(f"   ✓ Modelo asignado: {nombre}")
                            break
                    except:
                        continue

                print("\n[4/4] Extrayendo propiedades...")

                for i in range(global_comps.Count):
                    comp = global_comps.Item(i)
                    print(f"\n   Componente: {comp.Name}")

                    try:
                        print(f"     Tc: {comp.CriticalTemperature} K")
                        print(f"     Pc: {comp.CriticalPressure} kPa")
                        print(f"     MW: {comp.MolecularWeight}")
                    except Exception as prop_err:
                        print(f"     ⚠ Error leyendo propiedades: {prop_err}")

                print("\n✓ PRACTICA 2 COMPLETADA CON ÉXITO")

        except AttributeError as e:
            print(f"   ✗ basis_manager.Components no existe: {e}")
            print("\n   Probando rutas alternativas...")

            # Intentar con CurrentCase
            try:
                print("\n[Intento 2] Usando Flowsheet.Basis...")
                flowsheet = case.Flowsheet
                basis = flowsheet.Basis
                comps = basis.Components
                print(f"   ✓ flowsheet.Basis.Components accesible")
                comps.Add("Methanol")
                comps.Add("Water")
                print(f"   ✓ Componentes agregados: {comps.Count}")
            except Exception as e2:
                print(f"   ✗ También falló: {e2}")

                # Último intento
                print("\n[Intento 3] Listando propiedades disponibles...")
                print("   Propiedades de basis_manager:")
                for attr in dir(basis_manager):
                    if not attr.startswith('_'):
                        print(f"      - {attr}")

        print("\n[5/5] Cerrando...")
        time.sleep(2)
        hysys.Quit()
        print("="*60)

    except Exception as e:
        print(f"\n✗ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()

        try:
            hysys.Quit()
        except:
            pass

if __name__ == '__main__':
    main()
