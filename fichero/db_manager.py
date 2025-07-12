import pymysql

class DatabaseManager:
    def __init__(self):
        self.con = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="Root_1234",
            db="centromedico",
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.con.cursor()

    def obtener_todos(self, tabla):
        self.cursor.execute(f"SELECT * FROM {tabla}")
        return self.cursor.fetchall()

    def actualizar(self, tabla, id_columna, id_valor, campo, nuevo_valor):
        query = f"UPDATE {tabla} SET {campo} = %s WHERE {id_columna} = %s"
        self.cursor.execute(query, (nuevo_valor, id_valor))
        self.con.commit()

    def insertar(self, tabla, datos_dict) :
        try :
            columnas = ", ".join(datos_dict.keys())
            placeholders = ", ".join(["%s"] * len(datos_dict))
            valores = list(datos_dict.values())

            sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
            self.cursor.execute(sql, valores)
            self.con.commit()
        except Exception as e :
            print(f"❌ Error al insertar: {e}")

    def eliminar(self, tabla, id_columna, id_valor):
        query = f"DELETE FROM {tabla} WHERE {id_columna} = %s"
        self.cursor.execute(query, (id_valor,))
        self.con.commit()
