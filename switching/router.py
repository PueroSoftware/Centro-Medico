from Gui_Paciente.Paciente_Gui import PacienteFrame
from Gui_Doctor.Doctor_Gui import DoctorFrame
from Gui_Cita.Cita_Gui import CitaFrame
#from Gui_Botica.Botica_Gui import BoticaFrame
#from Gui_Resumen.Resumen_Gui import ResumeFrame

def mostrar_paciente(ventana):
    ventana.mostrar_frame(PacienteFrame)

def mostrar_doctor(ventana):
    ventana.mostrar_frame(DoctorFrame)


def mostrar_cita(ventana) :
    ventana.mostrar_frame(CitaFrame)

"""def mostrar_botica(ventana) :
    ventana.mostrar_frame(BoticaFrame)

def mostrar_resumen(ventana) :
    ventana.mostrar_frame(ResumeFrame)"""

