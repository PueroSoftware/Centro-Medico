import customtkinter as ctk
from tkinter import ttk
from fichero.db_manager import DatabaseManager #Fichero para Conexion y Funciones

class AdminFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.db = DatabaseManager()
        self.pack(fill="both", expand=True)
        self.selector = ctk.CTkComboBox(self, values=[
            "Pacientes",
            "Doctores",
            "Especialidades",
            "Citas",
            "Farmaco",
            "Despacho",
            ])
        self.selector.pack(padx=10, pady=10)
        self.selector.bind("<<ComboboxSelected>>", self.cargar_datos)
        self.buscador = ctk.CTkEntry(self, placeholder_text="Buscar...")
        self.buscador.pack(padx=10, pady=5)
        self.buscador.bind("<KeyRelease>", self.filtrar_datos)
        self.tabla = ttk.Treeview(self, show="headings")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.actualizar_registro).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_registro).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Insertar", command=self.abrir_insercion).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.cargar_datos).pack(side="left", padx=5)
        self.selector.set("pacientes")
        self.cargar_datos()

    def cargar_datos(self, event=None):
        tabla = self.selector.get()
        datos = self.db.obtener_todos(tabla)
        columnas = list(datos[0].keys()) if datos else []
        self.tabla.delete(*self.tabla.get_children())
        self.tabla["columns"] = columnas

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")

        for fila in datos:
            valores = [fila[col] for col in columnas]
            self.tabla.insert("", "end", values=valores)

    def filtrar_datos(self, event=None):
        filtro = self.buscador.get().lower()
        tabla = self.selector.get()
        datos = self.db.obtener_todos(tabla)
        columnas = list(datos[0].keys()) if datos else []

        self.tabla.delete(*self.tabla.get_children())
        for fila in datos:
            if any(filtro in str(valor).lower() for valor in fila.values()):
                valores = [fila[col] for col in columnas]
                self.tabla.insert("", "end", values=valores)

    def actualizar_registro(self):
        selected = self.tabla.focus()
        if selected:
            values = self.tabla.item(selected, "values")
            tabla = self.selector.get()
            id_columna = self.tabla["columns"][0]
            campo = self.tabla["columns"][1]
            id_valor = values[0]
            nuevo_valor = values[1]
            self.db.actualizar(tabla, id_columna, id_valor, campo, nuevo_valor)
            self.cargar_datos()

    def eliminar_registro(self):
        selected = self.tabla.focus()
        if selected:
            values = self.tabla.item(selected, "values")
            tabla = self.selector.get()
            id_columna = self.tabla["columns"][0]
            id_valor = values[0]
            self.db.eliminar(tabla, id_columna, id_valor)
            self.cargar_datos()

    def abrir_insercion(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Insertar registro")
        tabla = self.selector.get()
        datos = self.db.obtener_todos(tabla)
        campos = list(datos[0].keys()) if datos else []
        entradas = {}

        for campo in campos:
            ctk.CTkLabel(ventana, text=campo).pack()
            entrada = ctk.CTkEntry(ventana)
            entrada.pack()
            entradas[campo] = entrada

        def guardar():
            valores = {campo: entrada.get() for campo, entrada in entradas.items()}
            self.db.insertar(tabla, valores)
            ventana.destroy()
            self.cargar_datos()

        ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)


# Ejecutable principal
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x600")
    app.title("Panel de Administración")
    AdminFrame(app)
    app.mainloop()
