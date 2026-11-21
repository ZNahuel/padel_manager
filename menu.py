from datetime import datetime
from mysql.connector import Error
from reservas import consultar_reservas, crear_reserva, modificar_reserva
from users import iniciar_sesion, registrar_usuario

#Menu por consola
def menu_reservas(sesion):
    '''Muestra el menú de reservas para el usuario autenticado.'''
    id_usuario = sesion["id_usuario"]
    print(f"\nBienvenido, {sesion['nombre']}.")

    while True:
        print("\n1. Crear reserva")
        print("2. Ver mis reservas")
        print("3. Cambiar horario")
        print("0. Cerrar sesión")
        opcion = input("Elegí una opción: ").strip()

        try:
            if opcion == "0":
                return
            
            elif opcion == "1":
                crear_reserva(sesion)
                
            elif opcion in ("2", "3"):
                reservas = consultar_reservas(id_usuario)
                if not reservas:
                    print("Todavía no tenés reservas.")
                    continue
                
                for reserva in reservas:
                    print(f"#{reserva['id_reserva']} | Cancha {reserva['cancha']} | "
                          f"{reserva['inicio']:%d/%m/%Y %H:%M}")
                    
                if opcion == "3":
                    numero = input("ID de la reserva que querés cambiar: ").strip()
                    if not numero.isdecimal():
                        print("Ingresá el número de reserva sin el símbolo #.")
                        continue
                    
                    texto = input("Nuevo horario (DD/MM/AAAA HH:MM): ").strip()
                    try:
                        nuevo_inicio = datetime.strptime(texto, "%d/%m/%Y %H:%M")
                    except ValueError:
                        print("Fecha inválida. Usá el formato DD/MM/AAAA HH:MM.")
                        continue

                    if modificar_reserva(int(numero), id_usuario, nuevo_inicio):
                        print("Horario actualizado.")
                    else:
                        print("No hubo cambios. Revisá el ID y el horario elegido.")
            else:
                print("Opción no válida.")
                
        except ValueError as error:
            print(error)  # Por ejemplo, si el nuevo turno está ocupado.
        except Error as error:
            print(f"No se pudo completar la operación en MySQL: {error.msg}")


def main():
    '''Permite al usuario registrar una cuenta o iniciar sesión y acceder al menú de reservas.'''
    while True:
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión")
        print("0. Salir")
        opcion = input("Elegí una opción: ").strip()
        
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            sesion = iniciar_sesion()
            if sesion is not None:
                menu_reservas(sesion)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()