import os #os para acceder a las variables de entorno

import mysql.connector


def conectar():
    '''Establece una conexión con la base de datos MySQL y devuelve el objeto de conexión'''
    return mysql.connector.connect(
        host="localhost",
        database="padel_manager",
        user=os.environ["PADEL_DB_USER"],
        password=os.environ["PADEL_DB_PASSWORD"]
    )