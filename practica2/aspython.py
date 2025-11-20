import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: EXPLORANDO COMPONENT LIST")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.SimulationCases.Add()
        basis_manager = case.BasisManager

        print("\n[1] Accediendo a ComponentLists...")
        comp_lists = basis_manager.ComponentLists
        print(f"   → Número de listas: {comp_lists.Count}")

        # Crear una ComponentList
        if comp_lists.Count == 0:
            print("   → Creando nueva Component List...")
            comp_list = comp_lists.Add()
            print("   ✓ Component List creada")
        else:
            comp_list = comp_lists.Item(0)

        print("\n[2] Explorando métodos y propiedades de ComponentList:")
        print("   Propiedades/métodos disponibles:")
        for attr in dir(comp_list):
            if not attr.startswith('_'):
                print(f"      - {attr}")

        print("\n[3] Probando métodos comunes para agregar componentes...")

        # Intentar varias alternativas
        alternativas = [
            ("comp_list.Add('Methanol')", lambda: comp_list.Add('Methanol')),
            ("comp_list.AddComponent('Methanol')", lambda: comp_list.AddComponent('Methanol')),
            ("comp_list.Components.Add('Methanol')", lambda: comp_list.Components.Add('Methanol')),
            ("comp_list.AddCompound('Methanol')", lambda: comp_list.AddCompound('Methanol')),
        ]

        for nombre, metodo in alternativas:
            try:
                print(f"\n   Intentando: {nombre}")
                resultado = metodo()
                print(f"   ✓ ÉXITO con: {nombre}")
                print(f"   → Resultado: {resultado}")
                print(f"   → Count ahora: {comp_list.Count if hasattr(comp_list, 'Count') else 'N/A'}")
                break  # Si funciona, salir del loop
            except AttributeError as e:
                print(f"   ✗ Método no existe: {e}")
            except Exception as e:
                print(f"   ✗ Error ejecutando: {e}")

        print("\n[4] Información adicional sobre ComponentList:")
        try:
            print(f"   → TypeName: {comp_list.TypeName if hasattr(comp_list, 'TypeName') else 'N/A'}")
            print(f"   → Count: {comp_list.Count if hasattr(comp_list, 'Count') else 'N/A'}")
        except Exception as e:
            print(f"   ⚠ Error obteniendo info: {e}")

        print("\n[5] Cerrando...")
        time.sleep(3)  # Más tiempo para ver HYSYS
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
