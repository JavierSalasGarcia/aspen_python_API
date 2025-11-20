import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: DEBUG PROPIEDADES DE COMPONENTES")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.SimulationCases.Add()
        basis_manager = case.BasisManager

        print("\n[1/4] Creando Component List...")
        comp_lists = basis_manager.ComponentLists
        comp_list = comp_lists.Add()
        print("   ✓ Component List creada")

        components = comp_list.Components

        print("\n[2/4] Agregando componentes...")
        print("   → Agregando Methanol...")
        components.Add("Methanol")
        print(f"   ✓ Methanol agregado (Count: {components.Count})")

        print("   → Agregando H2O...")
        components.Add("H2O")
        print(f"   ✓ H2O agregado (Count: {components.Count})")

        print("\n[3/4] Creando Fluid Package...")
        fluid_pkg = basis_manager.FluidPackages.Add()

        # Configurar modelo termodinámico
        nombres = ["Peng-Robinson", "PR", "SRK"]
        for nombre in nombres:
            try:
                fluid_pkg.PropertyPackageName = nombre
                if fluid_pkg.PropertyPackageName == nombre:
                    print(f"   ✓ Modelo termodinámico asignado: {nombre}")
                    break
            except:
                continue

        print("\n[4/4] Explorando estructura del componente...")

        # Tomar el primer componente (Methanol)
        comp = components.Item(0)
        print(f"\n   Componente: {comp.Name}")

        print("\n   Propiedades disponibles:")
        for attr in dir(comp):
            if not attr.startswith('_'):
                print(f"      - {attr}")

        print("\n   Intentando acceder a propiedades termodinámicas:")

        # Probar diferentes formas de acceder
        propiedades_a_probar = [
            ("comp.CriticalTemperature", lambda: comp.CriticalTemperature),
            ("comp.MolecularWeight", lambda: comp.MolecularWeight),
            ("comp.CriticalPressure", lambda: comp.CriticalPressure),
        ]

        for nombre_prop, getter in propiedades_a_probar:
            try:
                valor = getter()
                print(f"\n   {nombre_prop}:")
                print(f"      Tipo: {type(valor)}")
                print(f"      Valor directo: {valor}")

                # Si es CDispatch, explorar sus propiedades
                if hasattr(valor, '_oleobj_'):
                    print(f"      Es objeto COM, explorando...")
                    for attr in dir(valor):
                        if not attr.startswith('_') and attr[0].isupper():
                            print(f"         - {attr}")

                    # Intentar acceder a GetValue si existe
                    if hasattr(valor, 'GetValue'):
                        try:
                            val = valor.GetValue()
                            print(f"      GetValue(): {val} (tipo: {type(val)})")
                        except:
                            pass

                    # Intentar acceder a Value si existe
                    if hasattr(valor, 'Value'):
                        try:
                            val = valor.Value
                            print(f"      Value: {val} (tipo: {type(val)})")
                        except:
                            pass

            except Exception as e:
                print(f"\n   ✗ Error con {nombre_prop}: {e}")

        print("\n[5/5] Cerrando...")
        time.sleep(3)
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
