import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: COMPONENTES Y PAQUETES (FINAL V2)")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.SimulationCases.Add()
        basis_manager = case.BasisManager

        print("\n[1/4] Accediendo a ComponentLists...")
        # BasisManager tiene ComponentLists (plural), no Components
        comp_lists = basis_manager.ComponentLists
        print(f"   → Número de listas de componentes: {comp_lists.Count}")

        # Crear o acceder a la primera lista de componentes
        if comp_lists.Count == 0:
            print("   → Creando nueva Component List...")
            comp_list = comp_lists.Add()
        else:
            print("   → Usando Component List existente...")
            comp_list = comp_lists.Item(0)

        print("\n[2/4] Agregando componentes a la lista...")
        print("   → Agregando Methanol...")
        comp_list.Add("Methanol")
        print(f"   → Count después de Methanol: {comp_list.Count}")

        print("   → Agregando Water...")
        comp_list.Add("Water")
        print(f"   → Count después de Water: {comp_list.Count}")

        if comp_list.Count > 0:
            print(f"   ✓ Componentes agregados correctamente: {comp_list.Count}")
        else:
            print("   ⚠ ADVERTENCIA: Count sigue en 0")

        print("\n[3/4] Creando Fluid Package...")
        fluid_pkg = basis_manager.FluidPackages.Add()

        # Configurar modelo termodinámico
        print("   → Configurando modelo termodinámico...")
        nombres = ["Peng-Robinson", "PR", "SRK", "Soave-Redlich-Kwong"]

        for nombre in nombres:
            try:
                fluid_pkg.PropertyPackageName = nombre
                if fluid_pkg.PropertyPackageName == nombre:
                    print(f"   ✓ Modelo asignado: {nombre}")
                    break
            except:
                continue

        print("\n[4/4] Extrayendo propiedades de componentes...")

        for i in range(comp_list.Count):
            comp = comp_list.Item(i)
            print(f"\n   Componente: {comp.Name}")

            try:
                print(f"     Tc: {comp.CriticalTemperature} K")
                print(f"     Pc: {comp.CriticalPressure} kPa")
                print(f"     MW: {comp.MolecularWeight}")
            except Exception as prop_err:
                print(f"     ⚠ Error leyendo propiedades: {prop_err}")

        print("\n[5/5] Cerrando...")
        time.sleep(2)
        hysys.Quit()

        print("\n" + "="*60)
        print("✓ PRACTICA 2 COMPLETADA CON ÉXITO")
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
