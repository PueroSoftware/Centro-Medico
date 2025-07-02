import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
from tkinter import Canvas, Frame, Scrollbar
from fichero.custom_widgets import Marcos_P, Etiqueta_P, Entradas_P, Botones_P

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ScrollableFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0, bg="#1F1F1F")
        self.frame = Frame(self.canvas, bg="#1F1F1F")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # para scroll con mouse

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class BoticaFrame(Marcos_P):
    def __init__(self, master=None):
        super().__init__(master=master, fg_color="#1F1F1F")
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        Etiqueta_P(
            self,
            text="💊 GESTIÓN DE BOTICA",
            font=("Roboto", 18, "bold"),
            text_color="white"
        ).grid(row=0, column=0, pady=10)

        cont = Marcos_P(self, fg_color="#1F1F1F")
        cont.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        cont.grid_columnconfigure((0, 1), weight=1)
        cont.grid_rowconfigure(0, weight=1)

        # Scrollable Frame Izquierdo - Ingreso a Bodega
        self.scroll_ingreso = ScrollableFrame(cont)
        self.scroll_ingreso.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        self.scroll_ingreso.frame.grid_columnconfigure((0, 1), weight=1)

        Etiqueta_P(
            self.scroll_ingreso.frame,
            text="📦 Ingreso a Bodega",
            font=("Roboto", 16, "bold"),
            text_color="white"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 10))

        campos_bodega = ["Código", "Nombre", "Presentación", "Laboratorio", "Cantidad"]
        self.campos_ingreso = {}
        for i, campo in enumerate(campos_bodega, start=1):
            Etiqueta_P(self.scroll_ingreso.frame, text=f"{campo}:", text_color="white").grid(
                row=i, column=0, sticky="e", padx=10, pady=4
            )
            entrada = Entradas_P(self.scroll_ingreso.frame)
            entrada.grid(row=i, column=1, sticky="ew", padx=10, pady=4)
            self.campos_ingreso[campo] = entrada

        Etiqueta_P(self.scroll_ingreso.frame, text="Fecha Caducidad:", text_color="white").grid(
            row=6, column=0, sticky="e", padx=10, pady=5
        )
        self.fecha_caducidad = DateEntry(self.scroll_ingreso.frame, date_pattern="yyyy-mm-dd")
        self.fecha_caducidad.grid(row=6, column=1, sticky="ew", padx=10, pady=5)

        Botones_P(
            self.scroll_ingreso.frame,
            text="Guardar en Bodega",
            command=self.guardar_bodega,
            width=160,
            text_color="white"
        ).grid(row=7, column=0, columnspan=2, pady=10)

        # Scrollable Frame Derecho - Entrega a Paciente
        self.scroll_entrega = ScrollableFrame(cont)
        self.scroll_entrega.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        self.scroll_entrega.frame.grid_columnconfigure((0, 1), weight=1)

        Etiqueta_P(
            self.scroll_entrega.frame,
            text="🚚 Entrega a Paciente",
            font=("Roboto", 16, "bold"),
            text_color="white"
        ).grid(row=0, column=0, columnspan=2, pady=(10, 10))

        campos_entrega = ["Paciente", "Fecha", "Medicamento", "Cantidad"]
        self.campos_entrega = {}
        for i, campo in enumerate(campos_entrega, start=1):
            Etiqueta_P(self.scroll_entrega.frame, text=f"{campo}:", text_color="white").grid(
                row=i, column=0, sticky="e", padx=10, pady=4
            )
            entrada = Entradas_P(self.scroll_entrega.frame)
            entrada.grid(row=i, column=1, sticky="ew", padx=10, pady=4)
            self.campos_entrega[campo] = entrada

        Etiqueta_P(self.scroll_entrega.frame, text="Fecha Caducidad:", text_color="white").grid(
            row=5, column=0, sticky="e", padx=10, pady=5
        )
        self.fecha_caducidad_entrega = DateEntry(self.scroll_entrega.frame, date_pattern="yyyy-mm-dd")
        self.fecha_caducidad_entrega.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

        Etiqueta_P(self.scroll_entrega.frame, text="¿Producto Caducado?", text_color="white").grid(
            row=6, column=0, sticky="e", padx=10, pady=4
        )
        self.radio_caducado = ctk.StringVar(value="No")
        ctk.CTkRadioButton(self.scroll_entrega.frame, text="Sí", variable=self.radio_caducado, value="Sí").grid(
            row=6, column=1, sticky="w", padx=(10, 80)
        )
        ctk.CTkRadioButton(self.scroll_entrega.frame, text="No", variable=self.radio_caducado, value="No").grid(
            row=6, column=1, sticky="e", padx=(80, 10)
        )

        Etiqueta_P(self.scroll_entrega.frame, text="¿Stock Disponible?", text_color="white").grid(
            row=7, column=0, sticky="e", padx=10, pady=4
        )
        self.radio_stock = ctk.StringVar(value="Sí")
        ctk.CTkRadioButton(self.scroll_entrega.frame, text="Sí", variable=self.radio_stock, value="Sí").grid(
            row=7, column=1, sticky="w", padx=(10, 80)
        )
        ctk.CTkRadioButton(self.scroll_entrega.frame, text="No", variable=self.radio_stock, value="No").grid(
            row=7, column=1, sticky="e", padx=(80, 10)
        )

        # Botones de acción - aquí sí con grid y sticky para que se vean
        frame_botones_entrega = ctk.CTkFrame(self.scroll_entrega.frame, fg_color="transparent")
        frame_botones_entrega.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        frame_botones_entrega.grid_columnconfigure(0, weight=1)
        frame_botones_entrega.grid_columnconfigure(1, weight=1)

        Botones_P(frame_botones_entrega, text="Agregar", command=self.agregar_medicamento, width=120,
                  text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        Botones_P(frame_botones_entrega, text="Despachar", command=self.despachar_medicamentos, width=120,
                  text_color="white").grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # --- Descripción del Medicamento (abajo) ---
        self.frame_descripcion = Marcos_P(self, fg_color="#1F1F1F", height=140)
        self.frame_descripcion.grid(row=2, column=0, sticky="ew", padx=10, pady=(10, 10))
        self.frame_descripcion.grid_columnconfigure(0, weight=1)

        Etiqueta_P(
            self.frame_descripcion,
            text="📖 Descripción del Medicamento",
            font=("Roboto", 14, "bold"),
            text_color="white"
        ).grid(row=0, column=0, pady=(10, 5))

        self.descripcion_txt = ctk.CTkTextbox(
            self.frame_descripcion, height=100, fg_color="#E0E0E0", text_color="black"
        )
        self.descripcion_txt.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def guardar_bodega(self):
        try:
            datos = {k: v.get().strip() for k, v in self.campos_ingreso.items()}
            if not all(datos.values()):
                raise ValueError("Todos los campos de ingreso deben estar completos.")
            datos["Fecha Caducidad"] = self.fecha_caducidad.get_date().isoformat()
            print("📦 Guardando en bodega:", datos)
        except Exception as e:
            print("⚠️ Error al guardar en bodega:", str(e))

    def agregar_medicamento(self):
        try:
            datos = {k: v.get().strip() for k, v in self.campos_entrega.items()}
            if not all(datos.values()):
                raise ValueError("Todos los campos de entrega deben estar completos.")
            datos["Fecha Caducidad"] = self.fecha_caducidad_entrega.get_date().isoformat()
            datos["Caducado"] = self.radio_caducado.get()
            datos["Stock"] = self.radio_stock.get()
            print("➕ Agregando medicamento:", datos)

            nombre = datos.get("Medicamento", "")
            if nombre:
                self.mostrar_descripcion(nombre)
            else:
                print("⚠️ Campo 'Medicamento' vacío, no se puede mostrar la descripción.")

            for entrada in self.campos_entrega.values():
                entrada.delete(0, "end")
            self.radio_caducado.set("No")
            self.radio_stock.set("Sí")
            self.fecha_caducidad_entrega.set_date(datetime.datetime.now().date())

        except Exception as e:
            print("⚠️ Error al agregar medicamento:", str(e))

    def despachar_medicamentos(self):
        print("🚚 Medicamento despachado al paciente.")

    def mostrar_descripcion(self, nombre_medicamento):
        self.descripcion_txt.delete("1.0", "end")
        self.descripcion_txt.insert("1.0", f"Información del medicamento: {nombre_medicamento}")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x600")
    app.title("Gestión de Botica")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    BoticaFrame(app)
    app.mainloop()
