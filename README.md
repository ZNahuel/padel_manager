# Padel Manager
Trabajo Practico Final en py.
Sistema de reservas y seguimiento de partidos de pádel.
Python 3.13

## Avance actual + Seguimiento de desarrollo

-Clase Partido.
-Registro de equipos y cancha.
-Inicio del encuentro.
-Consulta del estado.
-Suma de puntos
-Suma de games
-Al mejor de 3 sets
-Determina el ganador
-Input de jugadores de ambos equipos
-Input de cancha
Se corrigió el nombre del atributo en __init__ -> antes = en_tiebreke ahora -> en_tiebreak
-Se implementa el tie-break
-Se agrego manejo_archivos.py para crear, lectura, escritura y guardado de archivos del historial.
-Cada partido guarda su estado inicial y el marcador despues de cada punto en un archivo .txt, con un bloque por jugada.
-El comando "deshacer" lee el historial y restaura el marcador anterior al ultimo punto vigente, incluidos los games, los sets y el estado del partido. Si el punto había definido al ganador, el encuentro vuelve a quedar en curso.
-Cada correcion se resgistra en el mismo archivo y conserva la jugada original
-archivo users.py para crear usuarios
-base_datos.py para establecer conexion con servior local de mysql

-libreria de mysql: python -m pip install mysql-connector-python argon2-cffi

-se agrega inicio de sesion

'''powershell - inicio de mysql
$env:PADEL_DB_USER = Read-Host "Usuario de MySQL"
$env:PADEL_DB_PASSWORD = [System.Net.NetworkCredential]::new('', (Read-Host "Contraseña de MySQL" -AsSecureString)).Password
'''

-Funcion de inicio de sesion.
-menu para elegir entre crear usuario o iniciar sesion
-