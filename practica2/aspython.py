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

        # Lista de variantes comunes del nombre en distintas versiones de HYSYS
        # El orden importa: HYSYS suele preferir "Peng-Robinson" o "Peng Robinson"
        posibles_nombres = [
            "Peng-Robinson",      # Estándar más común
            "Peng Robinson",      # Sin guion
            "PR",                 # Abreviatura
            "Peng-Robinson EOS",  # Nombre largo
            "Soave-Redlich-Kwong", # Alternativa si PR falla (para probar)
            "SRK"
        ]

        modelo_asignado = False

        for nombre in posibles_nombres:
            try:
                print(f"   → Intentando asignar: '{nombre}'...")
                fluid_pkg.PropertyPackageName = nombre

                # Si no falla la línea anterior, verificamos que se haya guardado
                if fluid_pkg.PropertyPackageName == nombre:
                    print(f"   ✓ ÉXITO: Modelo asignado correctamente: {nombre}")
                    modelo_asignado = True
                    break
            except Exception:
                # Si falla, simplemente continuamos al siguiente nombre
                continue

        if not modelo_asignado:
            print("   ⚠ ADVERTENCIA: No se pudo asignar ningún modelo automáticamente.")
            print("   → Se usará el modelo por defecto de HYSYS (si existe).")

        # Intentar leer el modelo final
        try:
            print(f"   → Estado final del paquete: {fluid_pkg.PropertyPackageName}")
        except:
            pass

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
