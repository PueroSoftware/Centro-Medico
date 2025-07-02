from frontend.Botica_Gui import BoticaFrame
from frontend.Cita_Gui import CitaFrame
from frontend.Doctor_Gui import DoctorGui
from frontend.Paciente_Gui import PacienteFrame
from frontend.Resumen_Gui import ResumenFrame


def mostrar_paciente(ventana):
    ventana.mostrar_frame(PacienteFrame)


def mostrar_doctor(ventana):
    ventana.mostrar_frame(DoctorGui)


def mostrar_cita(ventana):
    ventana.mostrar_frame(CitaFrame)


def mostrar_botica(ventana):
    ventana.mostrar_frame(BoticaFrame)


def mostrar_resumen(ventana):
    ventana.mostrar_frame(ResumenFrame)
