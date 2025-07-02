"""Conexión a la base de datos del sistema Centro Médico (MySQL, pymysql)"""
import pymysql

def obtener_conexion():
	"""
    Establece y retorna una conexión activa a la base de datos 'centromedico'.
    Devuelve None si ocurre un error durante la conexión.
    """
	try:
		conexion = pymysql.connect(
				host='127.0.0.1',
				user='root',
				password='Root_1234',
				database='centromedico',
				cursorclass=pymysql.cursors.DictCursor  # Acceso a resultados como diccionarios
		)
		print("✅ Conexión establecida con éxito a la base de datos 'centromedico'")
		return conexion
	except pymysql.MySQLError as error:
		print(f"❌ Error al conectar con la base de datos: {error}")
		return None


# Test manual si se ejecuta este archivo directamente
if __name__ == "__main__":
	conexion = obtener_conexion()
	if conexion:
		try:
			with conexion.cursor() as cursor:
				cursor.execute("SELECT VERSION()")
				version = cursor.fetchone()
				print(f"🔍 Versión del servidor MySQL: {version['VERSION()']}")
		except pymysql.MySQLError as error:
			print(f"⚠️ Error ejecutando consulta de prueba: {error}")
		finally:
			conexion.close()
			print("🔌 Conexión cerrada correctamente.")
