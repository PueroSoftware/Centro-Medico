import os
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from Ficheros.AltCentro import *
from switching.router import mostrar_paciente  # ← arriba del archivo o del bloque de botones

#Clase Principal Donde cada objeto de las clases que están arriba son llamadas
class Ventana_P(ctk.CTk) :
    def __init__(self) :
        super().__init__()
        ancho = 1320
        alto =680
        alt_centro(self,ancho,alto)
        self.title("Centro Medico") #Título de la Ventana
        self.resizable(False,False)
        # Asignar el ícono .ico directamente (solo Windows)
        if os.path.exists(icono) :
            self.iconbitmap(icono)
        else :
            print("¡ERROR! No se encontró el archivo de ícono:", icono)

    def mostrar_frame(self, frame_class) :
        # Elimina lo que esté dentro de m_cuerpo
        for widget in self.m_cuerpo.winfo_children() :
            widget.destroy()

        # Crea e inserta el nuevo frame
        nuevo_frame = frame_class(master=self.m_cuerpo)
        nuevo_frame.pack(fill="both", expand=True)

#-------------------------- Rutas dinámicas con la biblioteca os y Pillow------------------------------------- """
RutaRaiz = os.path.dirname(__file__)
RutaPrincipal = os.path.dirname(RutaRaiz)
RutaImg = os.path.join(RutaPrincipal, "img")
icono = os.path.join(RutaImg, "logo.ico")  # Variable para asignar una Ruta Relativa
logo = os.path.join(RutaImg, "perfil.png")
imagen_pil = Image.open(logo)

# Crear un CTkImage (puedes definir tamaños para dark/light si lo deseas)--------------------------------
imagen_ctk = CTkImage(light_image=imagen_pil, size=(200,200))

#Clase Principal de Botones---------------------------------------
class Botones_P(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


#Clase Principal de Etiquetas---------------------------------------
class Etiqueta_P(ctk.CTkLabel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

#Clase Principal de Entradas por teclados---------------------------------------
class Entradas_P(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

#Clase Principal de checkbox---------------------------------------
class Cajas_P(ctk.CTkCheckBox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

#Clase Principal de Marcos para agrupar Elementos---------------------------------------
class Marcos_P(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

# Clase de Botón Radio---------------------------------------
class R_Botones_P(ctk.CTkRadioButton):
    def __init__(self,master=None,**kwargs):
        super().__init__(master, **kwargs)

# Instancia de la ventana principal---------------------------------------
ventana = Ventana_P()

#Ahora puedes crear el marco y asociarlo a la ventana---------------------------------------
m_superior = Marcos_P(master=ventana,height=10,border_color="#373837")
m_superior.pack(side="top",fill="x")

#Barra inferior---------------------------------------
m_sidebar= Marcos_P(master=ventana,height=50,border_width=2)
m_sidebar.pack(side="bottom",fill="x")

#Distribuir espacio entre columnas---------------------------------------
for i in range(8):  # total de columnas usadas hasta column=7
    m_sidebar.grid_columnconfigure(i, weight=1)

#Contenedor central (para sidebar y contenido)---------------------------------------
m_principal = Marcos_P(master=ventana,fg_color="#F8F8F8",border_width=1)
m_principal.pack(side="top",fill="both",expand=True)

# --- INICIO DE LA CORRECCIÓN ---
# Configura la cuadrícula del contenedor principal para que se expanda
m_principal.grid_rowconfigure(0, weight=1)  # Parte superior (logo)
m_principal.grid_rowconfigure(1, weight=2)  # Parte inferior (botones)
m_principal.grid_columnconfigure(0, weight=0) # Lado izquierdo (fijo)
m_principal.grid_columnconfigure(1,weight=1)  # Cuerpo (debe expandirse)
# --- FIN DE LA CORRECCIÓN ---

"""
Dentro del marco llamado cuerpo entrará toda la lógica 
"""
m_cuerpo = Marcos_P(master=m_principal,fg_color="#373837")
m_cuerpo.grid(row=0, column=1, rowspan=2, pady=10, padx=10, sticky="nsew")  # <= clave: rowspan=2

#Barra lateral izquierda---------------------------------------
m_izquierdo = Marcos_P(master=m_principal,width=200,border_width=1,border_color="#fbf8f8")
m_izquierdo.grid(row=1,column=0,pady=(10,5),padx=10,sticky="w")
for m in range(7):#weight	Define cómo se reparte el espacio adicional entre columnas.
    m_izquierdo.grid_columnconfigure(m,weight=2)

#Este Frame de CTK tiene UN Label y Una Imagen.................................................
m1_izquierdo = Marcos_P(master=m_principal,width=200,height=200,border_width=1,border_color="#fbf8f8")
m1_izquierdo.grid(row=0,column=0,pady=(5,10),padx=10,sticky="w")

# 2. ¡LÍNEA CLAVE! Evita que el frame cambie de tamaño por su contenido
m1_izquierdo.grid_propagate(False)

lbl_logo = Etiqueta_P(master=m1_izquierdo, image=imagen_ctk,text="")
lbl_logo.pack(pady=10)


#Botones Principales
btn_paciente = Botones_P(master=m_izquierdo, text="Paciente", width=180, height=30)
btn_paciente.pack(pady=10,padx=10) # Más espacio arriba
btn_paciente.configure(command=lambda: mostrar_paciente(self))  # ← aquí llamas a la función externa

btn_cita = Botones_P(master=m_izquierdo, text="Citas", width=180, height=30)
btn_cita.pack(pady=10, padx=10)

btn_doctor = Botones_P(master=m_izquierdo, text="Doctor", width=180, height=30)
btn_doctor.pack(pady=10, padx=10)

btn_botica = Botones_P(master=m_izquierdo, text="Botica", width=180, height=30)
btn_botica.pack(pady=10, padx=10)

btn_resumen = Botones_P(master=m_izquierdo, text="Resumen", width=180, height=30).pack(pady=10, padx=10)

""" Botones para el frame de abajo  """
#Botón atrás (columna 0)
btn_atras = Botones_P(master=m_sidebar, text="<< Atrás", width=200, height=35)
btn_atras.grid(row=0, column=0, pady=10, padx=(20, 5), sticky="w")

#Columnas vacías para simular espacio (columnas 1 y 2)
#No se colocan widgets, solo sirven de separación

#Botón Guardar (columna 3)
btn_guardar = Botones_P(master=m_sidebar, text="Guardar", width=200, height=35)
btn_guardar.grid(row=0, column=3, pady=10, padx=5)

#Botón Limpiar (columna 4)
btn_limpiar = Botones_P(master=m_sidebar, text="Limpiar", width=200, height=35)
btn_limpiar.grid(row=0, column=4, pady=10, padx=5)

#-------------------Columnas 5 y 6 como espacio---------------------------------

#----------------------------Botón avanzar----(columna 7)--------------------------
btn_adelantar = Botones_P(master=m_sidebar, text="Avanzar >>", width=200, height=35)
btn_adelantar.grid(row=0, column=7, pady=10, padx=(5, 20), sticky="e")
letras = ctk.CTkFont(family="Roboto", size=20, weight="bold", slant="italic")#---------CTkFont
Titulo_P=Etiqueta_P(master=m_superior,text="Centro Medico Alianza Medica Popular",font=letras)
Titulo_P.pack(pady=10)

if __name__ == "__main__":
    ventana.mainloop()



""" (#2E2E2E oscuros), (#373837 oscuros),(#000000 negro),(#FBF8F8 blanco) #85929e  """


















