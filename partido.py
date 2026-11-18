from manejo_archivos import (crear_archivo_historial, guardar_bloque, leer_bloques)

class Partido:
    def __init__(self, cancha, equipo_A, equipo_B):
        '''inicializa un partido con la cancha y los equipos especificados, y establece el estado inicial del partido'''
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
        self.en_tiebreak = False
        self.estado = "pendiente" 
        self.ganador = None 
        self.archivo_historial = crear_archivo_historial()
            
    def iniciar_partido(self):
        '''inicia el partido y guarda el estado inicial en el historial'''
        if self.estado != "pendiente":
            raise Exception("El partido ya ha sido iniciado o finalizado.")
        self.estado = "en curso"
        self.guardar_estado("inicio")
        print(f"Historial: {self.archivo_historial}")
    
    
    def resumen(self):
        '''muestra resumen del partido, cancha, equipos, estado, sets y games'''
        print(f"Partido en la cancha: {self.cancha}")
        print(f"Equipo A: {' / '.join(self.equipo_A)}")
        print(f"Equipo B: {' / '.join(self.equipo_B)}")
        print(f"Estado: {self.estado}")
        print(f"Sets: {self.sets_A} - {self.sets_B}")
            
        for numero, resultado in enumerate(self.resultado_sets, start=1):
            games_A, games_B = resultado
            print(f"Set {numero}: {games_A} - {games_B}")
                
        if self.estado == "finalizado":
            print(f"Ganador: Equipo {self.ganador}")
            
        else:
            puntos_A, puntos_B = self.puntos_mostrar()
            print(f"Games: {self.games_A} - {self.games_B}")
            print(f"Puntos: {puntos_A} - {puntos_B}")
        
    def sumar_punto(self, equipo):
        '''suma un punto al equipo especificado y actualiza el estado del partido'''
        if self.estado != "en curso":
            raise Exception("El partido no está en curso.")
        
        if equipo not in ("A", "B"):
            raise ValueError("Equipo debe ser 'A' o 'B'.")
        
        if equipo == "A":
            self.puntos_A += 1
        elif equipo == "B":
            self.puntos_B += 1
            
        if self.en_tiebreak:
            self.comprobar_tiebreak()
        else:
            self.comprobar_game()
        
        self.guardar_estado("punto", equipo)
        
    def comprobar_game(self):
        '''comprueba si un equipo ha ganado el game actual y actualiza los games y sets en consecuencia'''
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
        '''devuelve los puntos actuales en formato de padel, considerando el tiebreak y el deuce'''
        if self.en_tiebreak:
            return str(self.puntos_A), str(self.puntos_B)
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
        '''comprueba si un equipo ha ganado el set actual y actualiza los sets y el estado del partido en consecuencia'''
        if self.games_A == 6 and self.games_B == 6:
            self.en_tiebreak = True
            print("Comienza el tiebreak.")
            return
        if (self.games_A >= 6 and self.games_A - self.games_B >= 2) or (self.games_A == 7 and self.games_B == 6):
            self.sets_A += 1
            self.resultado_sets.append((self.games_A, self.games_B))
            self.games_A = 0
            self.games_B = 0
        elif (self.games_B >= 6 and self.games_B - self.games_A >= 2) or (self.games_B == 7 and self.games_A == 6):
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
                
    def comprobar_tiebreak(self):
        '''comprueba si un equipo ha ganado el tiebreak y actualiza los games, sets y estado del partido en consecuencia'''
        if self.puntos_A >= 7 and self.puntos_A - self.puntos_B >= 2:
            self.games_A += 1
        elif self.puntos_B >= 7 and self.puntos_B - self.puntos_A >= 2:
            self.games_B += 1
        else:
            return  # No hay ganador aún en el tiebreak
        #el set terminó 7-6 o 6-7
        self.puntos_A = 0
        self.puntos_B = 0
        self.en_tiebreak = False
        self.comprobar_set()
        
    def guardar_estado(self, tipo, equipo=None):
        '''guarda el estado actual del partido en el historial'''
        bloque = {
            "tipo": tipo,
            "equipo": equipo,
            "cancha": self.cancha,
            "equipo_A": self.equipo_A,
            "equipo_B": self.equipo_B,
            "estado": {
                "puntos_A": self.puntos_A,
                "puntos_B": self.puntos_B,
                "games_A": self.games_A,
                "games_B": self.games_B,
                "sets_A": self.sets_A,
                "sets_B": self.sets_B,
                "resultado_sets": self.resultado_sets,
                "en_tiebreak": self.en_tiebreak,
                "estado": self.estado,
                "ganador": self.ganador
            }
        }

        guardar_bloque(self.archivo_historial, bloque)
        
    def deshacer_punto(self):
        '''deshace el último punto registrado y restaura el estado anterior del partido'''
        estados = self.leer_estados()
        if len(estados) <= 1:
            print("No hay puntos para deshacer.")
            return
        
        anterior = estados[-2]
        
        self.puntos_A = anterior["puntos_A"]
        self.puntos_B = anterior["puntos_B"]
        self.games_A = anterior["games_A"]
        self.games_B = anterior["games_B"]
        self.sets_A = anterior["sets_A"]
        self.sets_B = anterior["sets_B"]
        
        self.resultado_sets = [tuple(resultado) for resultado in anterior["resultado_sets"]] #lista de tuplas, busca resultado anterior en el historial
        self.en_tiebreak = anterior["en_tiebreak"]
        self.estado = anterior["estado"]
        self.ganador = anterior["ganador"]

        # Guardar el estado después de deshacer
        self.guardar_estado("deshacer")
    
    def leer_estados (self):
        '''lee los estados del historial y devuelve una lista de estados en orden cronológico'''
        blolques = leer_bloques(self.archivo_historial)
        estados = []
        
        for bloque in blolques:
            if bloque["tipo"] in ("inicio", "punto"):
                estados.append(bloque["estado"])
            elif bloque["tipo"] == "deshacer":
                if len(estados) > 1:
                    estados.pop()
        return estados