from partido import Partido

def main():
    equipo_A = ["Jugador A1", "Jugador A2"]
    equipo_B = ["Jugador B1", "Jugador B2"]
    
    partido = Partido(cancha=1, equipo_A=equipo_A, equipo_B=equipo_B)
    partido.iniciar_partido()
    partido.resumen()
    
if __name__ == "__main__":
    main()