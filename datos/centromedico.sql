CREATE DATABASE centromedico;
USE centromedico;

CREATE TABLE Pacientes (
    id_paciente INT PRIMARY KEY AUTO_INCREMENT,
    cedula_id VARCHAR(20) UNIQUE,
    nombres VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    fecha_nacimiento DATE,
    sexo ENUM('Masculino','Femenino','Agenero') NOT NULL DEFAULT 'Agenero',
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    estado_activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Doctores (
    id_doctor INT PRIMARY KEY AUTO_INCREMENT,
    cedula_doctor VARCHAR(20) UNIQUE,
    nombres_doctor VARCHAR(100),
    apellido_paterno_doctor VARCHAR(100),
    apellido_materno_doctor VARCHAR(100),
    especialidad_doctor VARCHAR(100),
    email_doctor VARCHAR(100),
    telefono_doctor VARCHAR(20),
    estado_activo BOOLEAN DEFAULT TRUE
);
CREATE TABLE Especialidades (
    id_especialidad INT PRIMARY KEY AUTO_INCREMENT,
    nombre_especialidad VARCHAR(100)
);

CREATE TABLE RegistroAsistencia (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_doctor INT NOT NULL,
    fecha DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME,
    CONSTRAINT fk_doctor
        FOREIGN KEY (id_doctor)
        REFERENCES Doctores(id_doctor)
        ON DELETE CASCADE
);

CREATE TABLE Citas (
    id_cita INT PRIMARY KEY AUTO_INCREMENT,
    id_paciente INT ,
    id_doctor INT,
    fecha_cita DATE,
    hora_cita TIME,
    motivo_cita TEXT,
    estado_cita BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
    FOREIGN KEY (id_doctor) REFERENCES Doctores(id_doctor)
);

CREATE TABLE farmaco (
    id_farmaco INT AUTO_INCREMENT PRIMARY KEY,
    codigo_farmaco VARCHAR(50) NOT NULL,
    nombre_farmaco VARCHAR(255) NOT NULL,
    presentacion VARCHAR(100) NOT NULL,
    laboratorio VARCHAR(100) NOT NULL,
    stock_actual INT UNSIGNED NOT NULL DEFAULT 0,
    fecha_caducidad DATE NOT NULL,
    -- Índices adicionales para consultas rápidas
    INDEX idx_codigo (codigo_medicamento),
    INDEX idx_nombre (nombre_medicamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE despacho (
    id_despacho INT AUTO_INCREMENT PRIMARY KEY,
    cedula_paciente VARCHAR(20) NOT NULL,
    id_farmaco INT NOT NULL,
    cantidad INT NOT NULL,
    fecha_despacho DATE NOT NULL,
    FOREIGN KEY (id_farmaco) REFERENCES farmaco(id_farmaco)
);








