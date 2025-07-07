# --- Receta_Crud.py CORREGIDO ---
from datetime import datetime
from fichero.conexion import obtener_conexion
from fichero.pdf_widget import GeneradorPdfRecetas
import pymysql

class RecetaCrud:
    def __init__(self):
        self.conexion = obtener_conexion()
        self.cursor = self.conexion.cursor(pymysql.cursors.DictCursor)

    def obtener_resumen_completo(self, cedula_paciente):
        try:
            # Buscar paciente
            self.cursor.execute("""
                SELECT id_paciente, nombres, apellido_paterno, apellido_materno,
                       fecha_nacimiento, sexo
                FROM Pacientes
                WHERE cedula_id = %s
            """, (cedula_paciente,))
            paciente = self.cursor.fetchone()
            print("✅ Paciente:", paciente)
            if not paciente:
                return None

            # Calcular edad
            edad = None
            if paciente.get("fecha_nacimiento"):
                fecha_nac = paciente["fecha_nacimiento"]
                hoy = datetime.now().date()
                edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

            # Buscar última cita
            self.cursor.execute("""
                SELECT c.id_cita, c.fecha_cita, d.especialidad_doctor
                FROM Citas c
                JOIN Doctores d ON c.id_doctor = d.id_doctor
                WHERE c.id_paciente = %s
                ORDER BY c.fecha_cita DESC
                LIMIT 1
            """, (paciente["id_paciente"],))
            cita = self.cursor.fetchone()
            print("✅ Cita:",cita)

            # Buscar medicamentos despachados
            self.cursor.execute("""
                SELECT f.nombre_farmaco, dp.cantidad, dp.fecha_despacho
                FROM despacho dp
                JOIN farmaco f ON dp.id_farmaco = f.id_farmaco
                WHERE dp.cedula_paciente = %s
                ORDER BY dp.fecha_despacho DESC
            """,(cedula_paciente,))
            medicamentos = self.cursor.fetchall()
            print("✅ Medicamentos:", medicamentos)

            # Elegimos el último medicamento como tratamiento
            tratamiento = ""
            if medicamentos :
                ultimo = medicamentos[0]
                tratamiento = f"{ultimo['nombre_farmaco']} (Cant: {ultimo['cantidad']})"
            # Resumen final
            resumen = {
                "nombre_completo": f"{paciente.get('nombres', '')} {paciente.get('apellido_paterno', '')} {paciente.get('apellido_materno', '')}",
                "edad": edad,
                "genero": paciente.get("sexo"),
                "fecha_cita": cita["fecha_cita"] if cita else None,
                "especialidad_doctor": cita["especialidad_doctor"] if cita else None,
                "diagnostico" : cita.get("motivo_cita","N/A") if cita else "N/A",
                "tratamiento" : tratamiento if tratamiento else "N/A",
                "observaciones" : "Sin observaciones por ahora"
            }
            return resumen

        except Exception as e:
            print("❌ Error al obtener resumen:", e)
            return None

    def generar_pdf(self, resumen, cedula_paciente) :
        try :


            if not resumen or not isinstance(resumen, dict) :
                raise ValueError("Datos de receta inválidos")
            generador = GeneradorPdfRecetas(resumen, cedula_paciente)
            ruta_pdf = generador.exportar()
            print(f"✅ PDF generado correctamente en: {ruta_pdf}")
            return ruta_pdf

        except Exception as e :
            print(f"❌ Error al generar PDF: {e}")
            return None

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()