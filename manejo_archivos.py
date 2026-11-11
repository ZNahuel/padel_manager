import json #json formato de intercambio de datos ligero y facil de leer
from pathlib import Path #permite gestionar archivos y directorios con una interfaz limpia y orientada a objetos
from uuid import uuid4 #permite generar identificadores únicos universales aleatorios


def crear_archivo_historial(): 
    carpeta = Path(__file__).resolve().parent / "historial" #Crea una ruta para la carpeta de historial
    carpeta.mkdir(exist_ok=True) #mkdir crea la carpeta si no existe, y exist_ok=True evita errores si ya existe
    ruta = carpeta / f"partido_{uuid4().hex}.txt" #Crea una ruta para el archivo de historial
    ruta.touch(exist_ok=False) #touch crea el archivo si no existe, y exist_ok=False evita errores si ya existe

    return ruta


def guardar_bloque(ruta, bloque):
    with Path(ruta).open("a", encoding="utf-8") as archivo: #a abre el archivo en modo de append y agrega los datos al final
        texto = json.dumps(bloque, ensure_ascii=False) #Toma un objeto de Python y lo guarda directamente dentro de un archivo .json
        archivo.write(texto + "\n") 


def leer_bloques(ruta):
    bloques = []
    with Path(ruta).open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip():
                bloques.append(json.loads(linea))
    return bloques

# if __name__ == "__main__":
#     ruta = crear_archivo_historial()

#     guardar_bloque(ruta, {
#         "tipo": "inicio",
#         "puntos_A": 0,
#         "puntos_B": 0
#     })

#     guardar_bloque(ruta, {
#         "tipo": "punto",
#         "equipo": "A",
#         "puntos_A": 1,
#         "puntos_B": 0
#     })

#     print(f"Archivo creado: {ruta}")

#     for bloque in leer_bloques(ruta):
#         print(bloque)