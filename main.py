from partido import Partido

def main():
    equipo_A = input("Ingrese los nombres de los jugadores del equipo A separados por comas: ").strip().split(",")
    equipo_B = input("Ingrese los nombres de los jugadores del equipo B separados por comas: ").strip().split(",")
    cancha = input("Ingrese el número de la cancha: ")

    partido = Partido(cancha=cancha, equipo_A=equipo_A, equipo_B=equipo_B)
    partido.iniciar_partido()
    # # Preparación temporal para probar el tie-break.
    # partido.games_A = 6
    # partido.games_B = 6
    # partido.comprobar_set()
    while True:
        equipo = input("\nSumar punto al equipo (equipo_A/equipo_B) o salir: ").strip().lower()

        if equipo == "salir":
            break
        if equipo == "equipo_a":
            partido.sumar_punto("A")
        elif equipo == "equipo_b":
            partido.sumar_punto("B")
        else:
            print("No válido.")
            continue

        puntos_A, puntos_B = partido.puntos_mostrar() #muestra los puntos en formato de padel
        print(f"Puntos: {puntos_A} - {puntos_B}")
        print(f"Games: {partido.games_A} - {partido.games_B}")
        print(f"Sets: {partido.sets_A} - {partido.sets_B}")
        
        if partido.estado == "finalizado":
            print(f"\nEl partido ha finalizado. Ganó {partido.ganador}.")
            break

    partido.resumen()
    
if __name__ == "__main__":
    main()