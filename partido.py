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
        
    def sumar_punto(self, equipo):
        if self.estado != "en curso":
            raise Exception("El partido no está en curso.")
        
        if equipo == "A":
            self.puntos_A += 1
        elif equipo == "B":
            self.puntos_B += 1
        else:
            raise ValueError("Equipo debe ser 'A' o 'B'.")

        self.comprobar_game()
        
    def comprobar_game(self):
        if self.puntos_A >= 4 and self.puntos_A - self.puntos_B >= 2:
            self.games_A += 1
            self.puntos_A = 0
            self.puntos_B = 0
            self.comprobar_set()
        elif self.puntos_B >= 4 and self.puntos_B - self.puntos_A >= 2:
            self.games_B += 1
            self.puntos_A = 0
            self.puntos_B = 0
            self.comprobar_set()

    def puntos_mostrar(self):
        valores = [0, 15, 30, 40]
        if self.puntos_A >= 3 and self.puntos_B >= 3:
            if self.puntos_A == self.puntos_B:
                return "40", "40 (Deuce)"
            elif self.puntos_A > self.puntos_B:
                return "AD", "40"
            else:
                return "40", "AD"
        return str(valores[self.puntos_A]), str(valores[self.puntos_B])
            
    def comprobar_set(self):
        if self.games_A >= 6 and self.games_A - self.games_B >= 2:
            self.sets_A += 1
            self.resultado_sets.append((self.games_A, self.games_B))
            self.games_A = 0
            self.games_B = 0
        elif self.games_B >= 6 and self.games_B - self.games_A >= 2:
            self.sets_B += 1
            self.resultado_sets.append((self.games_A, self.games_B))
            self.games_A = 0
            self.games_B = 0
        
        if (self.sets_A == 2 or self.sets_B == 2):
            self.estado = "finalizado"
            if self.sets_A == 2:
                self.ganador = "A"
            else:
                self.ganador = "B"