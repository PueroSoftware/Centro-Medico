# backend/Cita_Crud.py
from fichero.conexion import obtener_conexion

def insertar_cita(cedula_paciente, especialidad, fecha, hora, motivo):
    """
    Inserta una nueva cita.
    Busca el ID del paciente y del doctor usando cedula_paciente y especialidad.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Buscar id_paciente
            cursor.execute("SELECT id_paciente FROM Pacientes WHERE cedula_id = %s", (cedula_paciente,))
            paciente = cursor.fetchone()
            if not paciente:
                print("❌ Paciente no encontrado.")
                return False
            id_paciente = paciente['id_paciente']

            # Buscar id_doctor por especialidad
            cursor.execute("""
                SELECT id_doctor 
                FROM Doctores 
                WHERE especialidad_doctor = %s 
                LIMIT 1
            """, (especialidad,))
            doctor = cursor.fetchone()
            if not doctor:
                print("❌ Doctor con especialidad no encontrado.")
                return False
            id_doctor = doctor['id_doctor']

            # 🔍 DEBUG: mostrar datos antes de insertar
            print("🧪 Datos a insertar:")
            print(f"id_paciente={id_paciente}, id_doctor={id_doctor}, fecha={fecha}, hora={hora}, motivo={motivo}, estado_cita={False}")

            # Insertar cita
            cursor.execute("""
                INSERT INTO Citas (id_paciente, id_doctor, fecha_cita, hora_cita, motivo_cita, estado_cita)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_paciente, id_doctor, fecha, hora, motivo, False))
            conexion.commit()
            print("✅ Cita insertada correctamente.")
            return True
    except Exception as e:
        print(f"❌ Error insertando cita: {e}")
        return False
    finally:
        conexion.close()

def obtener_todas_citas():
    """
    Devuelve todas las citas como lista de diccionarios.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT c.id_cita, p.cedula_id, p.nombres, p.apellido_paterno, p.apellido_materno,
                       d.nombres_doctor, d.especialidad_doctor, c.fecha_cita, c.hora_cita, c.motivo_cita, c.estado_cita
                FROM Citas c
                JOIN Pacientes p ON c.id_paciente = p.id_paciente
                JOIN Doctores d ON c.id_doctor = d.id_doctor
                ORDER BY c.fecha_cita DESC
            """)
            columnas = [col[0] for col in cursor.description]
            return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        conexion.close()

def obtener_cita_por_id(id_cita):
    """
    Devuelve una cita específica por su id_cita.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Citas WHERE id_cita = %s
            """, (id_cita,))
            fila = cursor.fetchone()
            if fila:
                columnas = [col[0] for col in cursor.description]
                return dict(zip(columnas, fila))
            return None
    finally:
        conexion.close()

def actualizar_cita(id_cita, fecha, hora, motivo, estado_cita):
    """
    Actualiza los datos de una cita existente.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE Citas
                SET fecha_cita=%s, hora_cita=%s, motivo_cita=%s, estado_cita=%s
                WHERE id_cita=%s
            """, (fecha, hora, motivo, estado_cita, id_cita))
            conexion.commit()
            print("✅ Cita actualizada correctamente.")
            return True
    except Exception as e:
        print(f"❌ Error actualizando cita: {e}")
        return False
    finally:
        conexion.close()

def eliminar_cita(id_cita):
    """
    Elimina una cita por su id_cita.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM Citas WHERE id_cita=%s", (id_cita,))
            conexion.commit()
            print("✅ Cita eliminada correctamente.")
            return True
    except Exception as e:
        print(f"❌ Error eliminando cita: {e}")
        return False
    finally:
        conexion.close()
