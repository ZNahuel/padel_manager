from partido import Partido

def main():
    '''Función principal que permite al usuario interactuar con el sistema de gestión de partidos de pádel'''
    # equipo_A = input("Ingrese los nombres de los jugadores del equipo A separados por comas: ").strip().split(",")
    # equipo_B = input("Ingrese los nombres de los jugadores del equipo B separados por comas: ").strip().split(",")
    # cancha = input("Ingrese el número de la cancha: ")
    equipo_A = ["Jugador A1", "Jugador A2"]
    equipo_B = ["Jugador B1", "Jugador B2"]
    cancha = "Cancha 1"

    partido = Partido(cancha=cancha, equipo_A=equipo_A, equipo_B=equipo_B)
    partido.iniciar_partido()
    print("Estado después de iniciar:", repr(partido.estado))
    # # # Preparación temporal para probar el tie-break.
    # partido.games_A = 6
    # partido.games_B = 6
    # partido.comprobar_set()
    while True:
        equipo = input("\nSumar punto al (equipo_A/equipo_B), deshacer, o salir: ").strip().lower()

        if equipo == "salir":
            break
        
        if equipo == "deshacer":
            partido.deshacer_punto()
                    
        elif equipo in ("equipo_a", "equipo_b"):
            if partido.estado == "finalizado":
                print("El partido finalizado. Deshacer o salir.")
                continue
            if equipo == "equipo_a":
                partido.sumar_punto("A")
            elif equipo == "equipo_b":
                partido.sumar_punto("B")
                
        else:
            print("No válido.")
            continue
        
        #se muestra despues de sumar o deshacer.
        puntos_A, puntos_B = partido.puntos_mostrar()
        print(f"Puntos: {puntos_A} - {puntos_B}")
        print(f"Games: {partido.games_A} - {partido.games_B}")
        print(f"Sets: {partido.sets_A} - {partido.sets_B}")
        
        if partido.estado == "finalizado":
            print(f"\nEl partido ha finalizado. Ganó {partido.ganador}.")
            

    partido.resumen()
    
if __name__ == "__main__":
    main()