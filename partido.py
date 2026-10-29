class Partido:
    def __init__(self, cancha, equipo_A, equipo_B):
        self.cancha = cancha
        #cada equipo cointiene los nombres de sus jugadores
        self.equipo_A = equipo_A
        self.equipo_B = equipo_B
        #cantidad de puntos del game actual
        self.puntos_A = 0
        self.puntos_B = 0
        #Games del set actual
        self.games_A = 0
        self.games_B = 0
        #Sets ganados por cada equipo
        self.sets_A = 0
        self.sets_B = 0
        #resutado de los sets
        self.resultado_sets = []
        self.en_tiebrake = False
        self.estado = "pendiente"
        self.ganador = None
        
    def iniciar_partido(self):
        if self.estado != "pendiente":
            raise Exception("El partido ya ha sido iniciado o finalizado.")
        self.estado = "en curso"
    
    def resumen(self):
        print(f"Partido en la cancha: {self.cancha}")
        print(f"Equipo A: {' / '.join(self.equipo_A)}")
        print(f"Equipo B: {' / '.join(self.equipo_B)}")
        print(f"Estado: {self.estado}")
        print(f"sets: {self.sets_A} - {self.sets_B}")
        print(f"games: {self.games_A} - {self.games_B}")
        print(f"puntos: {self.puntos_A} - {self.puntos_B}")