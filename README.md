# Padel Manager
Trabajo Practico Final en py.
Sistema de reservas y seguimiento de partidos de pádel.
Python 3.13

## Requisitos y configuración

1. Instalá Python 3.13 y MySQL. Desde la carpeta del proyecto, instalá las dependencias:

- MySQL Server para guardar usuarios y reservas.
- Una clave de OpenWeather y conexión a internet para consultar el pronóstico.
python -m pip install customtkinter
python -m pip install mysql-connector-python
python -m pip install argon2-cffi
python -m pip install requests

2. En MySQL Workbench, abrí y ejecutá el archivo sql-usuarios.sql completo para crear la base padel_manager y las tablas usuarios y reservas.

3. Creá 'claves.py' junto a 'base_datos.py' con tus credenciales locales. Este archivo debe estar incluido en '.gitignore'.

   '''python
   MYSQL_USER = "tu_usuario_mysql"
   MYSQL_PASSWORD = "tu_contraseña_mysql"
   OPENWEATHER_API_KEY = "tu_clave_openweather"
   '''

## Cómo usar el sistema

- **Registrar una cuenta:** ejecutá 'python menu.py' y elegí Registrar usuario.
- **Reservar una cancha:** ejecutá 'python interfaz.py', iniciá sesión y elegí Crear reserva. Seleccioná la cancha, ingresá una fecha y hora futuras y cargá los cuatro jugadores. Los turnos duran una hora y comienzan a la hora en punto.
- **Consultar o modificar:** desde Mis reservas podés ver tus turnos y cambiar el horario. El sistema impide reservar la misma cancha dos veces para la misma fecha y hora.
- **Consultar el clima:** en el formulario, pulsá Ver pronóstico para consultar la temperatura y las condiciones previstas en General Deheza mediante OpenWeather.

## Marcador e historial

Al iniciar un partido desde main.py, se crea un archivo .txt en la carpeta historial/ que funciona como log del partido. Cada línea contiene un bloque en formato JSON con el estado inicial, un punto o una corrección. Al usar deshacer, el sistema lee el log, restaura el marcador anterior y agrega un bloque que registra la corrección. Así se conserva la jugada original.

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


-Funcion de inicio de sesion.
-menu para elegir entre crear usuario o iniciar sesion
-consultar reserva


-Interfaz grafica
-API del clima