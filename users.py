from getpass import getpass
from argon2 import PasswordHasher #argon2 para encriptar la contraseña
from mysql.connector import Error, integrity_error
from base_datos import conectar



def pedir_campo(mensaje):
    '''Solicita al usuario que ingrese un valor para un campo obligatorio y valida que no esté vacío'''
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print ("Campo obligatorio.")

def registrar_usuario():
    '''Solicita al usuario que ingrese sus datos y los guarda en la base de datos'''
    nombre = pedir_campo("Nombre: ")
    apellido = pedir_campo("Apellido: ")
    dni = pedir_campo("DNI: ")
    telefono = pedir_campo("Teléfono: ")
    email = pedir_campo("Email: ").lower()
    
    
    while True:
        password = getpass("Contraseña: ")
        password_confirm = getpass("Confirmar contraseña: ")
        
        if not password or not password_confirm.strip():
            print("La contraseña es obligatoria.")
            continue
        elif password == password_confirm:
            break
        print("Las contraseñas no coinciden. Intente nuevamente.")
    
    print (f"Usuario {nombre} {apellido} registrado exitosamente.")
    
if __name__ == "__main__":
    registrar_usuario()
    