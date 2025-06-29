from Gui_Doctor.Doctor_Crud import Doctor
from Gui_Paciente.Paciente_Crud import Paciente


def guardar_desde_formulario(campos, fecha_nacimiento) :
    """
    Recolecta los datos del formulario de paciente y los pasa al CRUD para guardar.
    - campos: diccionario de widgets Entradas_P
    - fecha_nacimiento: string en formato 'dd/mm/yyyy' desde CalendarWidget
    """
    datos = {
        "nombres" : campos["nombres"].get(),
        "apellidos" : campos["apellidos"].get(),
        "cedula" : campos["cedula"].get(),
        "email" : campos["email"].get(),
        "telefono" : campos["telefono"].get(),
        "direccion" : campos["direccion"].get(),
        "fecha_nacimiento" : fecha_nacimiento
    }
    Paciente(datos)  # Envía los datos al CRUD real


def guardar_doctor_formulario(campos, especialidad) :
    datos = {
        "nombres_doctor" : campos["nombres"].get(),
        "apellidos" : campos["apellidos"].get(),
        "cedula_doctor" : campos["cedula"].get(),
        "telefono_doctor" : campos["telefono"].get(),
        "email_doctor" : campos["email"].get(),
        "especialidad_doctor" : especialidad
    }
    Doctor(datos)  # Envía los datos al CRUD real
