from datetime import datetime

import pymysql.cursors
from dateutil.relativedelta import relativedelta
from fichero.conexion import obtener_conexion

class crear_despacho:
    def __init__(self):
        self.conexion = obtener_conexion()

    def lista_farmacos(self):
        """Lista todos los medicamentos agregados en bodega."""
        try:
            with self.conexion.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id_farmaco, codigo_farmaco, nombre_farmaco, stock_actual, fecha_caducidad FROM farmaco")
                return cursor.fetchall()
        except Exception as e:
            print("❌ Error al listar fármacos:", e)
            return []

    def calcular_caducidad(self, fecha_produccion_str, meses=24):
        """Calcula la fecha de caducidad sumando meses a la fecha de producción."""
        fecha_produccion = datetime.strptime(fecha_produccion_str, "%Y-%m-%d")
        fecha_caducidad = fecha_produccion + relativedelta(months=+meses)
        return fecha_caducidad.strftime("%Y-%m-%d")
#######
    def verificar_stock_caducidad(self, id_farmaco, cantidad_solicitada, fecha_actual_str) :
        """
        Verifica que haya stock suficiente y que el medicamento no esté caducado.
        """
        try :
            with self.conexion.cursor() as cursor :
                cursor.execute(
                    "SELECT stock_actual, fecha_caducidad FROM farmaco WHERE id_farmaco = %s",
                    (id_farmaco,)
                )
                resultado = cursor.fetchone()
                if not resultado :
                    return False, "Medicamento no encontrado"

                stock_actual = resultado["stock_actual"]
                fecha_caducidad = resultado["fecha_caducidad"]

                fecha_actual = datetime.strptime(fecha_actual_str, "%Y-%m-%d").date()

                # ✅ Convertir fecha_caducidad a date si es necesario
                if isinstance(fecha_caducidad, str) :
                    try :
                        fecha_caducidad = datetime.strptime(fecha_caducidad, "%Y-%m-%d").date()
                    except ValueError :
                        return False, f"Formato inválido de fecha_caducidad: {fecha_caducidad}"
                elif isinstance(fecha_caducidad, datetime) :
                    fecha_caducidad = fecha_caducidad.date()

                if stock_actual < cantidad_solicitada :
                    return False, "Stock insuficiente"

                if fecha_actual > fecha_caducidad :
                    return False, "Medicamento caducado"

                return True, "OK"

        except Exception as e :
            print("❌ Error al verificar stock y caducidad:", e)
            return False, "Error en verificación"

    ##########
    def registrar_despacho(self, cedula_paciente, id_farmaco, cantidad, fecha_despacho):
        """Registra el despacho y actualiza el stock."""
        try:
            # Verificar stock y caducidad
            ok, mensaje = self.verificar_stock_caducidad(id_farmaco, cantidad, fecha_despacho)
            if not ok:
                return False, mensaje

            with self.conexion.cursor() as cursor:
                # Insertar en tabla despacho
                cursor.execute("""
                    INSERT INTO despacho (cedula_paciente, id_farmaco, cantidad, fecha_despacho)
                    VALUES (%s, %s, %s, %s)
                """, (cedula_paciente, id_farmaco, cantidad, fecha_despacho))

                # Actualizar stock
                cursor.execute("""
                    UPDATE farmaco SET stock_actual = stock_actual - %s WHERE id_farmaco = %s
                """, (cantidad, id_farmaco))

            self.conexion.commit()
            return True, "Despacho registrado correctamente"
        except Exception as e:
            self.conexion.rollback()
            print("❌ Error al registrar despacho:", e)
            return False, "Error al registrar despacho"

    def buscar_paciente_por_cedula(self, cedula):
        """Busca un paciente por cédula."""
        try:
            with self.conexion.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT id_paciente, nombres, apellido_paterno, apellido_materno
                    FROM Pacientes
                    WHERE cedula_id = %s
                """, (cedula,))
                paciente = cursor.fetchone()
                return paciente
        except Exception as e:
            print("❌ Error al buscar paciente:", e)
            return None

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
