import customtkinter as ctk
from tkcalendar import DateEntry
import datetime


class Registro_Horas(ctk.CTkFrame):
	def __init__(self, master=None, titulo="Registro", color="#eeeeee", color_texto="black", on_aplicar=None):
		super().__init__(master, fg_color=color, corner_radius=8)
		self.on_aplicar = on_aplicar
		self.grid_columnconfigure(0, weight=1)
		
		# Título
		ctk.CTkLabel(self, text=titulo, font=("Roboto", 18, "bold"), text_color=color_texto) \
			.grid(row=0, column=0, pady=(10, 5), padx=10)
		
		# Cédula
		self.cedula_entry = ctk.CTkEntry(self, placeholder_text="Cédula", width=220)
		self.cedula_entry.grid(row=1, column=0, pady=5, padx=10)
		
		# Fecha
		self.fecha_entry = DateEntry(self, date_pattern="yyyy-mm-dd", width=15)
		self.fecha_entry.set_date(datetime.datetime.now().date())
		self.fecha_entry.configure(state="disabled")
		self.fecha_entry.grid(row=2, column=0, pady=5, padx=10)
		
		# Hora actual
		self.hora_var = ctk.StringVar(value=datetime.datetime.now().strftime("%H:%M:%S"))
		self.hora_label = ctk.CTkLabel(self, textvariable=self.hora_var, font=("Roboto", 16, "bold"))
		self.hora_label.grid(row=3, column=0, pady=5)
		
		# Botones Aplicar + Limpiar
		btn_frame = ctk.CTkFrame(self, fg_color="transparent")
		btn_frame.grid(row=4, column=0, pady=10)
		
		ctk.CTkButton(btn_frame, text="Aplicar", command=self.aplicar, width=100).pack(side="left", padx=5)
		ctk.CTkButton(btn_frame, text="Limpiar", command=self.limpiar, width=100).pack(side="left", padx=5)
	
	def aplicar(self):
		cedula = self.cedula_entry.get().strip()
		fecha = self.fecha_entry.get_date()
		hora = datetime.datetime.now().time()
		self.hora_var.set(hora.strftime("%H:%M:%S"))
		
		if not cedula:
			print("⚠️ Debe ingresar una cédula.")
			return
		
		if self.on_aplicar:
			self.on_aplicar(cedula, fecha, hora)
	
	def limpiar(self):
		self.cedula_entry.delete(0, "end")
		self.fecha_entry.set_date(datetime.datetime.now().date())
		self.hora_var.set(datetime.datetime.now().strftime("%H:%M:%S"))
	
	def get_datos(self):
		return (
				self.cedula_entry.get().strip(),
				self.fecha_entry.get_date(),
				datetime.datetime.now().time()
		)


class RegistroHorarioWidget(ctk.CTkFrame):
	def __init__(self, master=None):
		super().__init__(master)
		self.grid_columnconfigure((0, 1), weight=1)
		
		# 🧾 Encabezado
		encabezado = ctk.CTkFrame(self, fg_color="transparent")
		encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(25, 10), padx=10)
		encabezado.grid_columnconfigure(0, weight=1)
		
		titulo = ctk.CTkLabel(encabezado, text="🩺 ESTADO ACTUAL DEL DOCTOR", font=("Roboto", 26, "bold"))
		titulo.grid(row=0, column=0, sticky="w")
		
		subtitulo = ctk.CTkLabel(encabezado, text="Seleccione su rol para registrar entrada o salida",
		                         font=("Roboto", 14), text_color="#666666")
		subtitulo.grid(row=1, column=0, sticky="w", pady=(5, 0))
		
		# Estado dinámico de entrada/salida
		self.label_estado_entrada = ctk.CTkLabel(self, text="🟢 Entrada: No registrada", text_color="green")
		self.label_estado_salida = ctk.CTkLabel(self, text="🔴 Salida: No registrada", text_color="red")
		self.label_estado_entrada.grid(row=1, column=0, sticky="w", padx=20)
		self.label_estado_salida.grid(row=1, column=1, sticky="w", padx=20)
		
		# Paneles de Entrada y Salida
		self.panel_entrada = Registro_Horas(
				self,
				titulo="🟢 Registro de Entrada",
				color="#ddf7e6",
				color_texto="green",
				on_aplicar=self.aplicar_entrada
		)
		self.panel_entrada.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")
		
		self.panel_salida = Registro_Horas(
				self,
				titulo="🔴 Registro de Salida",
				color="#fbe4e4",
				color_texto="red",
				on_aplicar=self.aplicar_salida
		)
		self.panel_salida.grid(row=2, column=1, padx=15, pady=15, sticky="nsew")
		
		self.callback_entrada = None
		self.callback_salida = None
	
	def aplicar_entrada(self, cedula, fecha, hora):
		texto = f"🟢 Entrada: {hora.strftime('%H:%M:%S')} - {fecha.strftime('%Y-%m-%d')}"
		self.label_estado_entrada.configure(text=texto)
		if self.callback_entrada:
			self.callback_entrada(cedula, fecha, hora)
	
	def aplicar_salida(self, cedula, fecha, hora):
		texto = f"🔴 Salida: {hora.strftime('%H:%M:%S')} - {fecha.strftime('%Y-%m-%d')}"
		self.label_estado_salida.configure(text=texto)
		if self.callback_salida:
			self.callback_salida(cedula, fecha, hora)
	
	def set_callback_entrada(self, func):
		self.callback_entrada = func
	
	def set_callback_salida(self, func):
		self.callback_salida = func


# Prueba directa
if __name__ == "__main__":
	ctk.set_appearance_mode("light")
	ctk.set_default_color_theme("blue")
	
	root = ctk.CTk()
	root.title("Prueba RegistroHorarioWidget")
	root.geometry("950x600")
	
	widget = RegistroHorarioWidget(root)
	widget.pack(fill="both", expand=True)
	
	
	def guardar_entrada(ced, fecha, hora):
		print("💾 ENTRADA:", ced, fecha, hora)
	
	
	def guardar_salida(ced, fecha, hora):
		print("💾 SALIDA:", ced, fecha, hora)
	
	
	widget.set_callback_entrada(guardar_entrada)
	widget.set_callback_salida(guardar_salida)
	
	root.mainloop()
