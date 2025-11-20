import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: COMPONENTES Y PAQUETES")
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

        # Methanol funciona
        print("   → Agregando Methanol...")
        components.Add("Methanol")
        print(f"   ✓ Methanol agregado (Count: {components.Count})")

        # Probar diferentes nombres para Water
        print("   → Agregando Water (probando variantes)...")
        nombres_water = ["H2O", "Water", "WATER", "H20", "water"]

        water_agregado = False
        for nombre in nombres_water:
            try:
                print(f"      Intentando: '{nombre}'...")
                components.Add(nombre)
                print(f"   ✓ Water agregado como '{nombre}' (Count: {components.Count})")
                water_agregado = True
                break
            except Exception as e:
                print(f"      ✗ '{nombre}' no funciona")
                continue

        if not water_agregado:
            print("   ⚠ No se pudo agregar Water con ningún nombre conocido")

        comp_count = components.Count
        print(f"\n   → Total de componentes: {comp_count}")

        print("\n[3/4] Creando Fluid Package y configurando modelo...")
        fluid_pkg = basis_manager.FluidPackages.Add()

        # Configurar modelo termodinámico
        nombres = ["Peng-Robinson", "PR", "SRK", "Soave-Redlich-Kwong"]

        for nombre in nombres:
            try:
                fluid_pkg.PropertyPackageName = nombre
                if fluid_pkg.PropertyPackageName == nombre:
                    print(f"   ✓ Modelo termodinámico asignado: {nombre}")
                    break
            except:
                continue

        print("\n[4/4] Extrayendo propiedades de componentes...")

        for i in range(comp_count):
            comp = components.Item(i)
            print(f"\n   Componente: {comp.Name}")

            try:
                print(f"     Tc = {comp.CriticalTemperature:.2f} K")
                print(f"     Pc = {comp.CriticalPressure:.2f} kPa")
                print(f"     MW = {comp.MolecularWeight:.2f} g/mol")
            except Exception as prop_err:
                print(f"     ⚠ Error leyendo propiedades: {prop_err}")

        print("\n[5/5] Cerrando...")
        time.sleep(2)
        hysys.Quit()

        print("\n" + "="*60)
        print("✓ PRACTICA 2 COMPLETADA CON ÉXITO!")
        print("="*60)
        print("\nPróxima: Practica 3 - Corrientes")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()

        try:
            hysys.Quit()
        except:
            pass

if __name__ == '__main__':
    main()
