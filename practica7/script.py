# Practica 7

import win32com.client as win32
import time

def main():
    print("PRACTICA 7")
    print("="*60)

    try:
        hysys = win32.Dispatch('HYSYS.Application')
        hysys.Visible = True
        case = hysys.ActiveDocument

        print("Configurando sistema...")
        # Agregar tu implementacion aqui
        
        time.sleep(3)
        case.SaveRequired = False
        hysys.Quit()

        print("COMPLETADA!")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    main()
