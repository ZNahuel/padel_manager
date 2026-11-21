from datetime import datetime, timedelta
from mysql.connector import IntegrityError, errorcode
from base_datos import conectar
from users import pedir_campo


def guardar_reserva(id_usuario, cancha, inicio, modalidad, equipo_A, equipo_B):
    '''Guarda la reserva en la base de datos y devuelve el ID asignado'''
    consulta = '''INSERT INTO reservas (id_usuario, cancha, inicio, modalidad, jugador_a1, jugador_a2, jugador_b1, jugador_b2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    datos = (id_usuario, cancha, inicio, modalidad, equipo_A[0], equipo_A[1], equipo_B[0], equipo_B[1])
    
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, datos)
            id_reserva = cursor.lastrowid
        conexion.commit()
        
    return id_reserva


def crear_reserva(usuario):
    '''Solicita al usuario los datos de la reserva y la guarda en la base de datos'''
    while True:
        cancha = pedir_campo("Cancha (1 a 4): ")
        if cancha in ("1", "2", "3", "4"):
            cancha = int(cancha)
            break
        print("Elegí una cancha del 1 al 4.")

    # Solicita la fecha y hora del turno, asegurándose de que sea una fecha futura y en el formato correcto
    while True:
        texto = pedir_campo("Fecha y hora del turno (DD/MM/AAAA HH:MM) (formato 24hs): ")
        try:
            inicio = datetime.strptime(texto, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Ingresá una fecha y hora válidas, por ejemplo 25/11/2026 18:00.")
            continue
        # Verifica que la fecha y hora sean futuras y que el turno comience a la hora en punto
        if inicio <= datetime.now():
            print("Elegí un turno futuro.")
        elif inicio.minute != 0:
            print("Los turnos empiezan a la hora en punto.")
        else:
            break
        
    modalidad = "Al mejor de tres sets"
    print(f"Modalidad disponible: {modalidad}")
    # Solicita los nombres de los jugadores de ambos equipos
    equipo_A = [pedir_campo("Equipo A, jugador 1: "),
                pedir_campo("Equipo A, jugador 2: ")]
    equipo_B = [pedir_campo("Equipo B, jugador 1: "),
                pedir_campo("Equipo B, jugador 2: ")]
    #Guarda la reserva en la base de datos y maneja posibles errores de duplicación de reservas
    try:
        id_reserva = guardar_reserva(usuario["id_usuario"], cancha, inicio, modalidad, equipo_A, equipo_B)
    # Manejo de errores de duplicación de reservas
    except IntegrityError as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            print("Esa cancha ya está reservada para ese horario.")
            return
        raise
    # Calcula la hora de finalización y muestra la reserva confirmada.
    fin = inicio + timedelta(hours=1)
    print(f"\nReserva #{id_reserva} confirmada a nombre de {usuario['nombre']}.")
    print(f"Cancha {cancha} | {inicio:%d/%m/%Y} de {inicio:%H:%M} a {fin:%H:%M}")
    print(f"Equipo A: {' / '.join(equipo_A)}")
    print(f"Equipo B: {' / '.join(equipo_B)}")
    return id_reserva

def consultar_reservas(id_usuario):
    '''Devuelce las reservas del usuario ordenadas por fecha'''
    consulta = '''SELECT id_reserva, cancha, inicio
                  FROM reservas
                  WHERE id_usuario = %s
                  ORDER BY inicio'''
    with conectar() as conexion:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(consulta, (id_usuario,))
            reservas = cursor.fetchall()
    return reservas

def modificar_reserva(id_reserva, id_usuario, nuevo_inicio):
    """Cambia la fecha y hora de una reserva futura del usuario."""
    if nuevo_inicio <= datetime.now():
        raise ValueError("Elegí un turno futuro.")
    
    if nuevo_inicio.minute or nuevo_inicio.second or nuevo_inicio.microsecond:
        raise ValueError("El turno debe comenzar a la hora en punto.")
    
    consulta = """
        UPDATE reservas
        SET inicio = %s
        WHERE id_reserva = %s AND id_usuario = %s AND inicio > NOW()
    """
    
    try:
        with conectar() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (nuevo_inicio, id_reserva, id_usuario))
                modificada = cursor.rowcount > 0
            conexion.commit()
    except IntegrityError as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise ValueError("Esa cancha ya está reservada para ese horario.") from error
        raise

    return modificada