import win32com.client as win32
import time

def main():
    print("="*60)
    print("PRACTICA 2: COMPONENTES Y PAQUETES (CORREGIDO)")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True

        # Crear nuevo caso de simulación
        case = hysys.SimulationCases.Add()
        print("\n[1/4] HYSYS iniciado y caso creado")

        # --- CORRECCIÓN PRINCIPAL AQUÍ ---
        # No usamos Flowsheet para componentes, usamos BasisManager
        print("\n[2/4] Configurando el entorno Termodinámico (Basis)...")
        basis_manager = case.BasisManager

        # En HYSYS Automation, usualmente creamos primero el Paquete de Fluidos
        print("   → Creando Fluid Package...")
        fluid_pkg = basis_manager.FluidPackages.Add()

        print("   → Accediendo a la lista de componentes del Paquete...")
        # Los componentes se agregan a la lista del paquete de fluidos
        components = fluid_pkg.Components

        print("   → Agregando Methanol...")
        try:
            # El método Add devuelve el componente objeto, podemos capturarlo si queremos
            components.Add("Methanol")
            print("   ✓ Methanol agregado")
        except Exception as e:
            print(f"   ✗ Error al agregar Methanol: {e}")

        print("   → Agregando Water...")
        try:
            components.Add("Water")
            print("   ✓ Water agregado")
        except Exception as e:
            print(f"   ✗ Error al agregar Water: {e}")

        print(f"   → Componentes en el paquete: {components.Count}")

        # --- FIN DE LA SECCIÓN DE COMPONENTES ---

        print("\n[3/4] Configurando Modelo Termodinámico...")

        # PASO CRITICO: Asignar el modelo antes de leerlo.
        # "Peng-Robinson" es la cadena estándar para este modelo.
        try:
            print("   → Asignando Peng-Robinson...")
            fluid_pkg.PropertyPackageName = "Peng-Robinson"
        except Exception as e:
            print(f"   ⚠ No se pudo asignar el modelo directamente: {e}")

        # Ahora que ya tiene un valor, sí podemos leerlo (o confirmar que se asignó)
        try:
            print(f"   → Paquete configurado: {fluid_pkg.PropertyPackageName}")
        except:
            print("   → Paquete configurado (pero no se pudo leer el nombre vía COM)")

        # Extraer propiedades
        print("\n[4/4] Extrayendo propiedades de componentes...")

        for i in range(components.Count):
            comp = components.Item(i)
            print(f"\n   {comp.ComponentName}:")
            try:
                print(f"     Tc = {comp.CriticalTemperature:.2f} K")
                print(f"     Pc = {comp.CriticalPressure:.2f} kPa")
                print(f"     MW = {comp.MolecularWeight:.2f} g/mol")
            except Exception as e:
                print(f"     ⚠ Error al obtener propiedades: {e}")

        print("\n[5/5] Cerrando...")
        time.sleep(2)
        hysys.Quit()

        print("\n" + "="*60)
        print("PRACTICA 2 COMPLETADA!")
        print("="*60)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print(f"   Tipo: {type(e).__name__}")
        # Agregamos más detalle al debug
        import traceback
        traceback.print_exc()

        try:
            hysys.Quit()
        except:
            pass

if __name__ == '__main__':
    main()
