from fichero.conexion import obtener_conexion

# Crear / Insertar
def crear_farmaco(datos):
    """
    datos: diccionario con claves:
      - codigo_farmaco
      - nombre_farmaco
      - presentacion
      - laboratorio
      - stock_actual (int)
      - fecha_caducidad (YYYY-MM-DD)
    """
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO farmaco 
                (codigo_farmaco, nombre_farmaco, presentacion, laboratorio, stock_actual, fecha_caducidad)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                datos["codigo_farmaco"],
                datos["nombre_farmaco"],
                datos["presentacion"],
                datos["laboratorio"],
                datos["stock_actual"],
                datos["fecha_caducidad"]
            ))
        conexion.commit()
        print("✅ Farmaco creado correctamente")
    except Exception as e:
        print("❌ Error al crear farmaco:", str(e))
    finally:
        if conexion:
            conexion.close()
#################################
# Generar SKU
def generar_sku() :
    conexion = None
    try :
        conexion = obtener_conexion()
        with conexion.cursor() as cursor :
            # Consulta mejorada para manejar tablas vacías
            cursor.execute("SELECT COALESCE(MAX(id_farmaco), 0) + 1 AS next_id FROM farmaco")
            resultado = cursor.fetchone()

            if resultado and resultado['next_id'] :
                return f"SKU-{resultado['next_id']:05d}"
            else :
                return "SKU-00001"
    except Exception as e :
        print(f"❌ Error al generar SKU: {str(e)}")
        # Generar SKU de emergencia basado en timestamp
        import time
        timestamp = int(time.time() * 1000) % 100000
        return f"EMG-{timestamp:05d}"
    finally :
        if conexion :
            conexion.close()
##########################
# Leer / Listar
def listar_farmacos():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM farmaco")
            resultados = cursor.fetchall()
            return resultados
    except Exception as e:
        print("❌ Error al listar farmacos:", str(e))
        return []
    finally:
        if conexion:
            conexion.close()

# Actualizar
def actualizar_farmaco(id_farmaco, datos):
    """
    datos: dict con claves:
      - codigo_farmaco
      - nombre_farmaco
      - presentacion
      - laboratorio
      - stock_actual
      - fecha_caducidad
    """
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
                UPDATE farmaco
                SET codigo_farmaco=%s, nombre_farmaco=%s,
                    presentacion=%s, laboratorio=%s, 
                    stock_actual=%s, fecha_caducidad=%s
                WHERE id_farmaco=%s
            """
            cursor.execute(sql, (
                datos["codigo_farmaco"],
                datos["nombre_farmaco"],
                datos["presentacion"],
                datos["laboratorio"],
                datos["stock_actual"],
                datos["fecha_caducidad"],
                id_farmaco
            ))
        conexion.commit()
        print("✅ Farmaco actualizado correctamente")
    except Exception as e:
        print("❌ Error al actualizar farmaco:", str(e))
    finally:
        if conexion:
            conexion.close()

       #Lista de Presentacion de Medicamentos

def listar_presentaciones():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT DISTINCT presentacion FROM farmaco")
            resultados = cursor.fetchall()
            return [fila['presentacion'] for fila in resultados]
    except Exception as e:
        print("❌ Error al listar presentaciones:", repr(e))
        return []
    finally:
        if conexion:
            conexion.close()

# Eliminar
def eliminar_farmaco(id_farmaco):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM farmaco WHERE id_farmaco=%s", (id_farmaco,))
        conexion.commit()
        print("✅ Farmaco eliminado correctamente")
    except Exception as e:
        print("❌ Error al eliminar farmaco:", str(e))
        raise
    finally:
        if conexion:
            conexion.close()



