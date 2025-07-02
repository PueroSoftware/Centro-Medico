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
    id_paciente INT,
    id_doctor INT,
    fecha_hora_cita DATETIME,
    motivo_cita TEXT,
    estado_cita VARCHAR(50),
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
    FOREIGN KEY (id_doctor) REFERENCES Doctores(id_doctor)
);

CREATE TABLE Medicamentos (
    id_medicamento INT PRIMARY KEY AUTO_INCREMENT,
    codigo_medicamento VARCHAR(50),
    nombre_medicamento VARCHAR(255),
    descripcion_medicamento TEXT,
    presentacion VARCHAR(100),
    laboratorio VARCHAR(100),
    precio_unitario DECIMAL(10,2),
    stock_actual INT,
    fecha_caducidad DATE
);
