""" Librería de conexión a la base de datos del proyecto """
import pymysql

def crear_conexion() :
    """
    Crea y devuelve una conexión pymysql a la base de datos.
    Retorna None si falla la conexión.
    """
    try :
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='Root_1234',
            database='centromedico'
        )
        print("¡Conexión a la base de datos 'centromedico' establecida con éxito!")
        return conn
    except pymysql.Error as error :
        print(f"Error al conectar con la base de datos: {error}")
        return None


if __name__ == "__main__" :
    # Solo para pruebas en modo standalone
    Data_Db = crear_conexion()
    if Data_Db :
        try :
            cursor = Data_Db.cursor()

            # Ejemplo de SELECT
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Versión de la base de datos: {version[0]}")

            # Ejemplo de DML (INSERT/UPDATE/DELETE)
            # cursor.execute("INSERT INTO ...")
            # Data_Db.commit()   # <-- Aquí va el commit tras un INSERT/UPDATE/DELETE

        except pymysql.Error as error :
            print(f"Error ejecutando la consulta: {error}")
        finally :
            Data_Db.close()
            print("Conexión cerrada.")
