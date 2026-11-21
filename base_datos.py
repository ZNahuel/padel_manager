#import os #os para acceder a las variables de entorno
import mysql.connector
from claves import MYSQL_USER, MYSQL_PASSWORD

# def conectar():
#     '''Establece una conexión con la base de datos MySQL y devuelve el objeto de conexión'''
#     return mysql.connector.connect(
#         host="localhost",
#         database="padel_manager",
#         user=os.environ["PADEL_DB_USER"],
#         password=os.environ["PADEL_DB_PASSWORD"]
#     )
    
def conectar():
    """Abre la conexión con la base de datos de Padel Manager."""
    return mysql.connector.connect(
        host="localhost",
        database="padel_manager",
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )