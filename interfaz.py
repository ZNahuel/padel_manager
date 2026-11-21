import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from mysql.connector import Error, IntegrityError, errorcode
from users import autenticar_usuario
from reservas import consultar_reservas, guardar_reserva, modificar_reserva
from clima import consultar_pronostico

def main():
    '''Ejecuta la interfaz gráfica de la aplicación.'''
    ctk.set_appearance_mode("system")
    
    ventana = ctk.CTk()
    ventana.title("Padel Manager")
    ventana.geometry("540x400")
    ventana.minsize(440, 340)
    contenido = ctk.CTkFrame(ventana)
    contenido.pack(fill="both", expand=True, padx=20, pady=20)
    
    def limpiar_pantalla():
        '''Elimina todos los widgets del frame de contenido.'''
        for elemento in contenido.winfo_children():
            elemento.destroy()
            
    def mostrar_reservas(sesion, reservas):
        '''Muestra la lista de reservas del usuario en la interfaz gráfica.'''
        limpiar_pantalla()
        ctk.CTkLabel(contenido, text=f"Mis reservas · {sesion['nombre']}",
            font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=16, pady=16)
        
        lista = ctk.CTkScrollableFrame(contenido)
        lista.pack(fill="both", expand=True, padx=16)
        
        if not reservas:
            ctk.CTkLabel(lista, text="Todavía no tenés reservas.").pack(pady=12)
            
        for reserva in reservas:
            fila = ctk.CTkFrame(lista)
            fila.pack(fill="x", pady=3)
            
            texto = (
                f"#{reserva['id_reserva']} · Cancha {reserva['cancha']}\n"
                f"{reserva['inicio']:%d/%m/%Y a las %H:%M}")
            ctk.CTkLabel(fila, text=texto, justify="left").pack(side="left", padx=8, pady=5)
            
            ctk.CTkButton(
                fila,
                text="Cambiar horario",
                width=110,
                command=lambda r=reserva: mostrar_formulario(sesion, r)).pack(side="right", padx=8)
        acciones = ctk.CTkFrame(contenido, fg_color="transparent")
        acciones.pack(fill="x", padx=16, pady=12)
        
        ctk.CTkButton(acciones, text="Crear reserva",command=lambda: mostrar_formulario(sesion)).pack(side="left")
        ctk.CTkButton(acciones, text="Cerrar sesión", command=mostrar_login).pack(side="right")
            
    def mostrar_formulario(sesion, reserva=None):
        '''Muestra un formulario para crear o modificar una reserva.'''
        editando = reserva is not None
        titulo = "Cambiar horario" if editando else "Crear reserva"
        formulario = ctk.CTkToplevel(ventana)
        formulario.title(titulo)
        formulario.transient(ventana)
        panel = ctk.CTkFrame(formulario)
        panel.pack(fill="both", expand=True, padx=12, pady=12)
        
        def agregar_entrada(etiqueta):
            '''Agrega un label y un entry al formulario y devuelve el entry creado.'''
            ctk.CTkLabel(panel, text=etiqueta).pack(anchor="w", padx=14)
            entrada = ctk.CTkEntry(panel, width=280)
            entrada.pack(fill="x", padx=14, pady=(0, 6))
            return entrada
        
        if editando:
            ctk.CTkLabel(panel,text=f"Reserva #{reserva['id_reserva']} · Cancha {reserva['cancha']}").pack(pady=8)
        else:
            ctk.CTkLabel(panel, text="Cancha").pack(anchor="w", padx=14)
            cancha = ctk.CTkOptionMenu(panel, values=["1", "2", "3", "4"])
            cancha.pack(fill="x", padx=14, pady=(0, 6))
            
        fecha = agregar_entrada("Fecha y hora (DD/MM/AAAA HH:MM)")
        
        if editando:
            fecha.insert(0, reserva["inicio"].strftime("%d/%m/%Y %H:%M"))
        else:
            jugadores = []
            for etiqueta in ("Equipo A · Jugador 1", "Equipo A · Jugador 2",
                             "Equipo B · Jugador 1", "Equipo B · Jugador 2"):
                jugadores.append(agregar_entrada(etiqueta))
                
        resultado_clima = ctk.CTkLabel(panel, text="", wraplength=280)
        
        def ver_pronostico():
            '''Muestra el pronóstico del clima para la fecha y hora ingresadas'''
            try:
                inicio = datetime.strptime(fecha.get().strip(), "%d/%m/%Y %H:%M")
            except ValueError:
                resultado_clima.configure(text="Ingresá la fecha como DD/MM/AAAA HH:MM.")
                return
            resultado_clima.configure(text=consultar_pronostico(inicio))
        ctk.CTkButton(panel, text="Ver pronóstico", command=ver_pronostico).pack(pady=4)
        resultado_clima.pack(padx=14)
        
        def guardar():
            '''Valida los datos ingresados y guarda la reserva en la base de datos.'''
            try:
                inicio = datetime.strptime(fecha.get().strip(), "%d/%m/%Y %H:%M")
            except ValueError:
                messagebox.showwarning(
                    titulo, "Ingresá la fecha con el formato DD/MM/AAAA HH:MM.",
                    parent=formulario)
                return
            
            if inicio <= datetime.now() or inicio.minute != 0:
                messagebox.showwarning(
                    titulo, "Elegí una fecha futura y una hora en punto.",
                    parent=formulario)
                return
            try:
                if editando:
                    modificada = modificar_reserva(reserva["id_reserva"], sesion["id_usuario"], inicio)
                    if not modificada:
                        messagebox.showinfo(
                            titulo, "No hubo cambios. Revisá el horario elegido.",
                            parent=formulario)
                        return
                else:
                    nombres = [entrada.get().strip() for entrada in jugadores]
                    if not all(nombres):
                        messagebox.showwarning(titulo, "Completá los cuatro jugadores.", parent=formulario)
                        return
                    
                    guardar_reserva(
                        sesion["id_usuario"], int(cancha.get()), inicio,
                        "Al mejor de tres sets", nombres[:2], nombres[2:])
                    
            except IntegrityError as error:
                if error.errno == errorcode.ER_DUP_ENTRY:
                    mensaje = "Esa cancha ya está reservada para ese horario."
                else:
                    mensaje = error.msg
                messagebox.showerror(titulo, mensaje, parent=formulario)
                return
            except (ValueError, Error) as error:
                messagebox.showerror(titulo, str(error), parent=formulario)
                return
            
            formulario.destroy()
            
            try:
                reservas = consultar_reservas(sesion["id_usuario"])
            except Error:
                messagebox.showwarning(
                    titulo,
                    "El cambio se guardó. Volvé a iniciar sesión para actualizar la lista.",
                    parent=ventana)
                return
            
            mostrar_reservas(sesion, reservas)
            
        ctk.CTkButton(panel, text="Guardar", command=guardar).pack(pady=12)
        formulario.wait_visibility()
        formulario.grab_set()
        fecha.focus_set()
        
    def mostrar_login():
        '''Muestra la pantalla de inicio de sesión en la interfaz gráfica.'''
        limpiar_pantalla()
        ctk.CTkLabel(contenido, text="Padel Manager", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(24, 4))
        ctk.CTkLabel(contenido, text="Iniciar sesión").pack(pady=(0, 16))
        
        entrada_email = ctk.CTkEntry(contenido, placeholder_text="Email", width=280)
        entrada_email.pack(pady=6)
        
        entrada_password = ctk.CTkEntry(
            contenido, placeholder_text="Contraseña", show="*", width=280)
        entrada_password.pack(pady=6)
        
        def ingresar():
            '''Autentica al usuario con las credenciales ingresadas.'''
            email = entrada_email.get().strip()
            password = entrada_password.get()
            
            if not email or not password:
                messagebox.showwarning("Ingreso", "Completá el email y la contraseña.")
                return
            
            try:
                sesion = autenticar_usuario(email, password)
                if sesion is None:
                    messagebox.showerror("Ingreso", "Email o contraseña incorrectos.")
                    return
                
                reservas = consultar_reservas(sesion["id_usuario"])
            except KeyError as error:
                if error.args[0] not in ("PADEL_DB_USER", "PADEL_DB_PASSWORD"):
                    raise
                messagebox.showerror(
                    "Configuración",
                    f"Falta {error.args[0]}. Falla de conexion con MYSQL"
                    "Cerra, conecta y volvé a abrir la aplicación.")
                return
            except Error as error:
                messagebox.showerror("MySQL", f"No se pudo consultar la base: {error.msg}")
                return
            
            mostrar_reservas(sesion, reservas)
            
        ctk.CTkButton(contenido, text="Ingresar", command=ingresar, width=280).pack(pady=16)
        
        entrada_password.bind("<Return>", lambda evento: ingresar())
        entrada_email.focus_set()
        
    mostrar_login()
    ventana.mainloop()


if __name__ == "__main__":
    main()