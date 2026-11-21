-- Crear la base del proyecto si todavía no existe.
CREATE DATABASE IF NOT EXISTS padel_manager
    CHARACTER SET utf8mb4;
    
-- Seleccionar la base donde se creará la tabla.
USE padel_manager;

CREATE TABLE IF NOT EXISTS usuarios (
    -- MySQL asigna este ID al registrar la cuenta. Las reservas usarán este ID.
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    -- Cada campo admite hasta 80 caracteres.
    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,

    -- Desde Python se enviará el DNI solo con dígitos. UNIQUE evita duplicados.
    dni VARCHAR(15) NOT NULL UNIQUE,

    -- Se usa texto para conservar el prefijo +54 o un cero inicial.
    telefono VARCHAR(30) NOT NULL,

    -- El usuario usará este correo para iniciar sesión.
    email VARCHAR(254) NOT NULL UNIQUE,

    -- Python generará el hash de la contraseña antes de guardar la cuenta.
    password_hash VARCHAR(255) NOT NULL,

    -- Las cuentas nuevas reciben el rol 'usuario' por defecto.
    rol ENUM('usuario', 'administrador') NOT NULL DEFAULT 'usuario',

    -- MySQL carga la fecha y la hora al insertar el usuario.
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    cancha INT NOT NULL,
    inicio DATETIME NOT NULL,
    modalidad VARCHAR(50) NOT NULL,
    jugador_a1 VARCHAR(80) NOT NULL,
    jugador_a2 VARCHAR(80) NOT NULL,
    jugador_b1 VARCHAR(80) NOT NULL,
    jugador_b2 VARCHAR(80) NOT NULL,

    -- Vincula la reserva con el usuario que la creó.
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),

    -- Impide reservar dos veces la misma cancha para el mismo turno.
    UNIQUE (cancha, inicio)
);
