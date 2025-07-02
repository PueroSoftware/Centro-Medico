""" CRUD para la tabla Pacientes usando pymysql """
from fichero.conexion import obtener_conexion


def crear_paciente(cedula_id, nombres, apellidos, fecha_nacimiento, sexo, email, telefono, direccion) :
    """
    Inserta un nuevo paciente.
    apellidos: str con los dos apellidos separados por espacio, ejemplo "Pérez López"
    sexo: uno de los valores definidos en el ENUM ('Masculino', 'Femenino', 'Agenero')
    """
    try :
        lista_apellidos = apellidos.strip().split()
        apellido_paterno = lista_apellidos[0] if len(lista_apellidos) > 0 else ''
        apellido_materno = lista_apellidos[1] if len(lista_apellidos) > 1 else ''

        conexion = obtener_conexion()
        if conexion :
            with conexion.cursor() as cursor :
                sql = """
                INSERT INTO Pacientes 
                (cedula_id, nombres, apellido_paterno, apellido_materno,
                fecha_nacimiento, sexo, email, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    cedula_id, nombres, apellido_paterno, apellido_materno,
                    fecha_nacimiento, sexo, email, telefono, direccion
                ))
            conexion.commit()
            print("✅ Paciente creado correctamente.")
    except Exception as e :
        print(f"❌ Error al crear paciente: {e}")
    finally :
        if conexion :
            conexion.close()


def obtener_pacientes() :
    """ Retorna todos los pacientes activos como lista de diccionarios """
    try :
        conexion = obtener_conexion()
        if conexion :
            with conexion.cursor() as cursor :
                cursor.execute("SELECT * FROM Pacientes WHERE estado_activo = TRUE")
                pacientes = cursor.fetchall()
                return pacientes
    except Exception as e :
        print(f"❌ Error al obtener pacientes: {e}")
    finally :
        if conexion :
            conexion.close()


def obtener_paciente_por_id(id_paciente) :
    """ Retorna un paciente por su id """
    try :
        conexion = obtener_conexion()
        if conexion :
            with conexion.cursor() as cursor :
                sql = "SELECT * FROM Pacientes WHERE id_paciente = %s AND estado_activo = TRUE"
                cursor.execute(sql, (id_paciente,))
                paciente = cursor.fetchone()
                return paciente
    except Exception as e :
        print(f"❌ Error al obtener paciente: {e}")
    finally :
        if conexion :
            conexion.close()


def actualizar_paciente(id_paciente, cedula_id, nombres, apellidos,fecha_nacimiento, sexo, email, telefono, direccion) :

    """
    Actualiza un paciente existente por su ID.
    apellidos: str con los dos apellidos separados por espacio
    """
    try :
        lista_apellidos = apellidos.strip().split()
        apellido_paterno = lista_apellidos[0] if len(lista_apellidos) > 0 else ''
        apellido_materno = lista_apellidos[1] if len(lista_apellidos) > 1 else ''

        conexion = obtener_conexion()
        if conexion :
            with conexion.cursor() as cursor :
                sql = """
                UPDATE Pacientes
                SET cedula_id=%s, nombres=%s, apellido_paterno=%s, apellido_materno=%s,
                    fecha_nacimiento=%s, sexo=%s, email=%s, telefono=%s, direccion=%s
                WHERE id_paciente=%s
                """
                cursor.execute(sql, (
                    cedula_id, nombres, apellido_paterno, apellido_materno,
                    fecha_nacimiento, sexo, email, telefono, direccion, id_paciente
                ))
            conexion.commit()
            print("✅ Paciente actualizado correctamente.")
    except Exception as e :
        print(f"❌ Error al actualizar paciente: {e}")
    finally :
        if conexion :
            conexion.close()


def eliminar_paciente(id_paciente) :
    """ Elimina lógicamente un paciente por ID (cambia estado_activo a FALSE) """
    try :
        conexion = obtener_conexion()
        if conexion :
            with conexion.cursor() as cursor :
                sql = "UPDATE Pacientes SET estado_activo = FALSE WHERE id_paciente = %s"
                cursor.execute(sql, (id_paciente,))
            conexion.commit()
            print("🗑️ Paciente eliminado correctamente (borrado lógico).")
    except Exception as e :
        print(f"❌ Error al eliminar paciente: {e}")
    finally :
        if conexion :
            conexion.close()


if __name__ == "__main__":
    print("🧪 Ejecutando prueba directa de inserción...\n")

    crear_paciente(
        cedula_id="9876543210",
        nombres="Sofía",
        apellidos="Jiménez Moreno",
        fecha_nacimiento="1993-11-15",
        sexo="Femenino",
        email="sofia.jimenez@example.com",
        telefono="0981234567",
        direccion="Av. 9 de Octubre y Loja, Guayaquil"
    )
    crear_paciente(
        cedula_id="1002003001",
        nombres="Carlos Andrés",
        apellidos="Muñoz Vera",
        fecha_nacimiento="1990-05-12",
        sexo="Masculino",
        email="carlos.munoz@example.com",
        telefono="0999999991",
        direccion="Av. Quito y Sucre, Cuenca"
    )
crear_paciente(
    cedula_id="1002003003",
    nombres="José Ángel",
    apellidos="Rodríguez Méndez",
    fecha_nacimiento="1975-01-30",
    sexo="Masculino",
    email="jose.angel@example.com",
    telefono="0977777773",
    direccion="Cdla. El Paraíso, Machala"
)
print("\n📋 Pacientes activos en la base de datos:")
pacientes = obtener_pacientes()
for p in pacientes:
    print(p)


