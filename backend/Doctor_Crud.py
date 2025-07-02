# Módulo de conexión a MySQL
from fichero.conexion import obtener_conexion
from datetime import datetime, date, time


# Función para insertar un nuevo doctor
def crear_doctor(cedula, nombres, ap_paterno, ap_materno, especialidad, email, telefono):
    """
    Inserta un nuevo registro en la tabla Doctores.
    """
    try:
        conexion = obtener_conexion()
        if conexion:
            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO Doctores 
                    (cedula_doctor, nombres_doctor, apellido_paterno_doctor, 
                    apellido_materno_doctor, especialidad_doctor, 
                    email_doctor, telefono_doctor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (cedula, nombres, ap_paterno, ap_materno,especialidad, email, telefono))

            conexion.commit()
            print("✅ Doctor insertado exitosamente.")
    except Exception as e:
        print("❌ Error al insertar doctor:", repr(e))
    finally:
        if conexion:
            conexion.close()


# Traer listado de especialidades desde la tabla Especialidades
def obtener_especialidades():
    """
    Retorna todas las especialidades registradas (solo nombre).
    """
    try:
        conexion = obtener_conexion()
        if conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT nombre_especialidad FROM Especialidades")
                resultados = cursor.fetchall()
                return [r["nombre_especialidad"] for r in resultados]
    except Exception as e:
        print("❌ Error al obtener especialidades:", repr(e))
        return []
    finally:
        if conexion:
            conexion.close()


# Registrar nueva especialidad médica
def crear_especialidad(nombre):
    """
    Inserta una nueva especialidad si no existe.
    """
    try:
        conexion = obtener_conexion()
        if conexion:
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO Especialidades (nombre_especialidad) VALUES (%s)", (nombre,))
            conexion.commit()
            print("✅ Especialidad agregada.")
    except Exception as e:
        print("❌ Error al agregar especialidad:", repr(e))
    finally:
        if conexion:
            conexion.close()


#  Insertar entrada del doctor usando cédula como referencia
def registrar_entrada(cedula, fecha, hora_entrada):
    """
    Registra la hora de entrada del doctor en la fecha dada.

    Utiliza una subconsulta para convertir la cédula (valor visible en GUI)
    en id_doctor (PK requerido por la FK en RegistroAsistencia):
    SELECT id_doctor FROM Doctores WHERE cedula_doctor = %s
    """
    try:
        conexion = obtener_conexion()
        if conexion:
            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO RegistroAsistencia (id_doctor, fecha, hora_entrada)
                    SELECT id_doctor, %s, %s FROM Doctores WHERE cedula_doctor = %s
                """
                cursor.execute(sql, (fecha, hora_entrada, cedula))
            conexion.commit()
            print("✅ Entrada registrada.")
    except Exception as e:
        print("❌ Error al registrar entrada:", repr(e))
    finally:
        if conexion:
            conexion.close()


#  Registrar salida del doctor
def registrar_salida(cedula, fecha, hora_salida):
    """
    Actualiza la hora de salida para el registro de ese doctor en esa fecha.
    """
    try:
        conexion = obtener_conexion()
        if conexion:
            with conexion.cursor() as cursor:
                sql = """
                    UPDATE RegistroAsistencia SET hora_salida = %s
                    WHERE id_doctor = (
                        SELECT id_doctor FROM Doctores WHERE cedula_doctor = %s
                    ) AND fecha = %s
                """
                cursor.execute(sql, (hora_salida, cedula, fecha))
            conexion.commit()
            print("✅ Salida registrada.")
    except Exception as e:
        print("❌ Error al registrar salida:", repr(e))
    finally:
        if conexion:
            conexion.close()

#  Bloque principal de pruebas unitarias vía consola
if __name__ == "__main__":

    """ 
    print(" Iniciando pruebas de CRUD para Doctores...\n")

    # Doctor de prueba
    crear_doctor(
        cedula="0102030405",
        nombres="Luis Fernando",
        ap_paterno="Guerrero",
        ap_materno="Zambrano",
        especialidad="Pediatría",
        email="luis.guerrero@example.com",
        telefono="0998888777"
    )

    # Insertar entrada
    registrar_entrada(
        cedula="0102030405",
        fecha=date.today(),  # fecha actual
        hora_entrada=datetime.now().time()  # hora actual
    )

    # Registrar salida simulada
    registrar_salida(
        cedula="0102030405",
        fecha=date.today(),
        hora_salida=datetime.now().replace(microsecond=0).time()
    )

    print("\n Pruebas finalizadas correctamente.") """
