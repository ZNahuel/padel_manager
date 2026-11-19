from getpass import getpass
from argon2 import PasswordHasher #argon2 para encriptar la contraseña
from argon2.exceptions import VerifyMismatchError
from mysql.connector import Error, IntegrityError
from base_datos import conectar
from reservas import crear_reserva
from users import iniciar_sesion



def pedir_campo(mensaje):
    '''Solicita al usuario que ingrese un valor para un campo obligatorio y valida que no esté vacío'''
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print ("Campo obligatorio.")
        
def guardar_usuario(nombre, apellido, dni, telefono, email, password):
    '''guarda el user en mysql y devuelve el ID asignado'''
    pasword_hash = PasswordHasher().hash(password) #encripta la contraseña
    
    consulta = "INSERT INTO usuarios (nombre, apellido, dni, telefono, email, password_hash) VALUES (%s, %s, %s, %s, %s, %s)"
    
    datos = (nombre, apellido, dni, telefono, email, pasword_hash)
    
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, datos)
            id_usuario = cursor.lastrowid
        conexion.commit()
    return id_usuario

def registrar_usuario():
    '''Solicita al usuario que ingrese sus datos y los guarda en la base de datos'''
    nombre = pedir_campo("Nombre: ")
    apellido = pedir_campo("Apellido: ")
    dni = pedir_campo("DNI: ")
    telefono = pedir_campo("Teléfono: ")
    email = pedir_campo("Email: ").lower()
    
    #Bucle para solicitar la contraseña y su confirmación hasta que coincidan y no estén vacías
    while True:
        password = getpass("Contraseña: ")
        password_confirm = getpass("Confirmar contraseña: ")
        
        if not password.strip() or not password_confirm.strip():
            print("La contraseña es obligatoria.")
            continue
        elif password == password_confirm:
            break
        print("Las contraseñas no coinciden. Intente nuevamente.")
    #informa un DNI o email duplicado en mySQL y no guarda el usuario.
    try:
        id_usuario = guardar_usuario(nombre, apellido, dni, telefono, email, password)
    except IntegrityError as error:
        if error.errno == 1062: #1062 es el código de error de MySQL para una violación de clave única (duplicado)
            print("Ya existe una cuenta con ese DNI o email.")
        else:
            print(f"No se pudo guardar el usuario: {error.msg}")
    except Error as error:
        print(f"Error de MySQL: {error.msg}")
    else:
        print(f"Usuario {nombre} {apellido} registrado con ID {id_usuario}.")

def iniciar_sesion():
    """Verifica las credenciales del jugador y devuelve sus datos de sesión."""
    email = pedir_campo("Email: ").lower()
    password = getpass("Contraseña: ")

    consulta = "SELECT id_usuario, nombre, rol, password_hash FROM usuarios WHERE email = %s"
    try:
        #conexión con la base de datos y consulta el usuario por email
        with conectar() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                cursor.execute(consulta, (email,))
                usuario = cursor.fetchone() #fetchone() devuelve una sola fila de la consulta, o None si no hay resultados
    # Manejo de errores de conexión y consulta a la base de datos
    except Error as error:
        print(f"No se pudo consultar MySQL: {error.msg}")
        return None

    # Verifica si el usuario existe y si la contraseña es correcta
    if usuario is None:
        print("Email o contraseña incorrectos.")
        return None

    try:
        # Verifica la contraseña utilizando PasswordHasher
        PasswordHasher().verify(usuario["password_hash"], password)
    except VerifyMismatchError:
        print("Email o contraseña incorrectos.")
        return None
    
    # Si la verificación es exitosa, devuelve los datos del usuario
    return {
        "id_usuario": usuario["id_usuario"],
        "nombre": usuario["nombre"],
        "rol": usuario["rol"]
    }

if __name__ == "__main__":
    '''Permite al usuario registrar una cuenta o iniciar sesión'''
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    opcion = input("Elegí una opción: ").strip()

    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        sesion = iniciar_sesion()
        if sesion is not None:
            print(f"Bienvenido, {sesion['nombre']}. Tu ID es {sesion['id_usuario']}.")
    else:
        print("Opción no válida.")
    