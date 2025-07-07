import customtkinter as ctk
from tkinter import ttk

class AdminFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.selector = ctk.CTkComboBox(self, values=["Pacientes", "Doctores", "Citas", "Farmacos", "Despacho"])
        self.selector.pack(padx=10, pady=10)
        self.selector.bind("<<ComboboxSelected>>", self.cargar_datos)

        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.actualizar_registro).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_registro).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.cargar_datos).pack(side="left", padx=5)

        self.selector.set("Pacientes")
        self.cargar_datos()

    def cargar_datos(self, event=None):
        entidad = self.selector.get()
        self.tabla.delete(*self.tabla.get_children())

        if entidad == "Pacientes":
            from backend.Pacientes_Crud import obtener_pacientes
            datos = obtener_pacientes()
            for p in datos:
                self.tabla.insert("", "end", values=(p['id_paciente'], p['nombres']))
        elif entidad == "Doctores":
            from backend.Doctores_Crud import obtener_especialidades
            datos = obtener_especialidades()
            for idx, esp in enumerate(datos, start=1):
                self.tabla.insert("", "end", values=(idx, esp))
        elif entidad == "Citas":
            from backend.Citas_Crud import obtener_todas_citas
            datos = obtener_todas_citas()
            for c in datos:
                self.tabla.insert("", "end", values=(c['id_cita'], c['motivo_cita']))
        elif entidad == "Farmacos":
            from backend.Bodega_Crud import listar_farmacos
            datos = listar_farmacos()
            for f in datos:
                self.tabla.insert("", "end", values=(f['id_farmaco'], f['nombre_farmaco']))
        elif entidad == "Despacho":
            from backend.Despacho_Crud import lista_farmacos
            datos = lista_farmacos()
            for idx, f in enumerate(datos, start=1):
                self.tabla.insert("", "end", values=(idx, f))

    def actualizar_registro(self):
        selected = self.tabla.focus()
        if selected:
            values = self.tabla.item(selected, "values")
            entidad = self.selector.get()
            id_registro = values[0]
            nuevo_valor = values[1]

            if entidad == "Pacientes":
                from backend.Pacientes_Crud import actualizar_paciente
                actualizar_paciente(id_registro, nuevo_valor)
            elif entidad == "Doctores":
                from backend.Doctores_Crud import registrar_entrada
                registrar_entrada(id_registro)
            elif entidad == "Citas":
                from backend.Citas_Crud import actualizar_cita
                actualizar_cita(id_registro, nuevo_valor)
            elif entidad == "Farmacos":
                from backend.Bodega_Crud import actualizar_farmaco
                actualizar_farmaco(id_registro, nuevo_valor)
            elif entidad == "Despacho":
                from backend.Despacho_Crud import registrar_despacho
                registrar_despacho(id_registro)
        else:
            print("❌ No hay registro seleccionado para actualizar.")

    def eliminar_registro(self):
        selected = self.tabla.focus()
        if selected:
            values = self.tabla.item(selected, "values")
            entidad = self.selector.get()
            id_registro = values[0]

            if entidad == "Pacientes":
                from backend.Pacientes_Crud import eliminar_paciente
                eliminar_paciente(id_registro)
            elif entidad == "Doctores":
                from backend.Doctores_Crud import registrar_salida
                registrar_salida(id_registro)
            elif entidad == "Citas":
                from backend.Citas_Crud import eliminar_cita
                eliminar_cita(id_registro)
            elif entidad == "Farmacos":
                from backend.Bodega_Crud import eliminar_farmaco
                eliminar_farmaco(id_registro)
            elif entidad == "Despacho":
                from backend.Despacho_Crud import verificar_stock_caducidad
                verificar_stock_caducidad(id_registro)
        else:
            print("❌ No hay registro seleccionado para eliminar.")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("900x600")
    app.title("Panel de Administración")
    AdminFrame(app)
    app.mainloop()
