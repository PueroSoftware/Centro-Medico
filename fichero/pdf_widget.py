import os
from datetime import datetime
from tkinter.constants import CENTER

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from fpdf import FPDF  # ¡IMPORTANTE! Esta línea debe estar al principio

class GeneradorPDF:
    def __init__(self, datos: dict, ruta_archivo: str):
        self.datos = datos
        self.ruta = ruta_archivo

    def exportar(self):
        c = canvas.Canvas(self.ruta, pagesize=A4)
        ancho, alto = A4
        margen_x = 50
        margen_y = 50
        max_ancho_texto = ancho - 2 * margen_x
        espacio_linea = 14
        y = alto - margen_y

        c.setFont("Helvetica-Bold", 16)
        c.drawString(margen_x, y, "📋 Detalles de la Cita")
        y -= 30

        c.setFont("Helvetica", 12)
        text_obj = c.beginText()
        text_obj.setTextOrigin(margen_x, y)
        text_obj.setLeading(espacio_linea)  # espacio entre líneas

        for campo, valor in self.datos.items():
            texto = f"{campo.capitalize().replace('_', ' ')}: {valor}"
            # Dividir texto largo en líneas que quepan
            lineas = simpleSplit(texto, "Helvetica",12, max_ancho_texto)
            for linea in lineas:
                if text_obj.getY() < margen_y:
                    c.drawText(text_obj)
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    text_obj = c.beginText()
                    text_obj.setTextOrigin(margen_x, alto - margen_y)
                    text_obj.setLeading(espacio_linea)
                text_obj.textLine(linea)
        c.drawText(text_obj)

        c.save()
        return self.ruta


class GeneradorPdfRecetas:
    def __init__(self, datos_receta, cedula_paciente) :
        self.datos = datos_receta
        self.cedula = cedula_paciente
        self.pdf = FPDF()
        self.ruta_salida = self._generar_ruta()

    def _generar_ruta(self) :
        directorio = "recetas_generadas"
        if not os.path.exists(directorio) :
            os.makedirs(directorio)
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(directorio, f"Receta_{self.cedula}_{fecha}.pdf")

    def _generar_cabecera(self) :
        self.pdf.set_font('Arial', 'B', 16)
        # CORRECCIÓN: Usar 'C' en lugar de 1 para centrado
        self.pdf.cell(0, 10, 'RECETA MÉDICA', 0, 1, 'C')
        self.pdf.ln(10)

    def _generar_datos_paciente(self) :
        self.pdf.set_font('Arial', 'B', 12)
        # CORRECCIÓN: Usar 'L' en lugar de 1 para alineación izquierda
        self.pdf.cell(0, 10, 'DATOS DEL PACIENTE', 0, 1, 'L')
        self.pdf.set_font('Arial', '', 12)

        datos = [
            f"Nombre: {self.datos.get('nombre_completo', 'N/A')}",
            f"Cédula: {self.cedula}",
            f"Edad: {self.datos.get('edad', 'N/A')}",
            f"Género: {self.datos.get('genero', 'N/A')}",
            f"Fecha de cita: {self.datos.get('fecha_cita', 'N/A')}"
        ]

        for dato in datos :
            # CORRECCIÓN: Usar 'L' en lugar de 1
            self.pdf.cell(0, 10, dato, 0, 1, 'L')
        self.pdf.ln(5)

    def _generar_datos_medicos(self) :
        self.pdf.set_font('Arial', 'B', 12)
        # CORRECCIÓN: Usar 'L' en lugar de 1
        self.pdf.cell(0, 10, 'INFORMACIÓN MÉDICA', 0, 1, 'L')
        self.pdf.set_font('Arial', '', 12)

        secciones = {
            'Especialidad' : self.datos.get('especialidad_doctor', 'N/A'),
            'Diagnóstico' : self.datos.get('diagnostico', 'N/A'),
            'Tratamiento' : self.datos.get('tratamiento', 'N/A'),
            'Observaciones' : self.datos.get('observaciones', 'N/A')
        }

        for titulo, contenido in secciones.items() :
            self.pdf.set_font('Arial', 'B', 12)
            # CORRECCIÓN: Usar 'L' en lugar de 0
            self.pdf.cell(40, 10, f"{titulo}:", 0, 0, 'L')
            self.pdf.set_font('Arial', '', 12)
            # CORRECCIÓN: Especificar align='L' como parámetro nombrado
            self.pdf.multi_cell(0, 10, contenido, align='L')
            self.pdf.ln(2)

    def _generar_pie(self) :
        self.pdf.set_y(-15)
        self.pdf.set_font('Arial', 'I', 8)
        # CORRECCIÓN: Usar 'C' en lugar de 0 para centrado
        self.pdf.cell(0, 10, f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 0, 'C')

    def exportar(self) :
        self.pdf.add_page()
        self._generar_cabecera()
        self._generar_datos_paciente()
        self._generar_datos_medicos()
        self._generar_pie()

        self.pdf.output(self.ruta_salida)
        return self.ruta_salida


def crear_pdf_resumen(resumen, cedula_paciente) :
    generador = GeneradorPdfRecetas(resumen, cedula_paciente)
    return generador.exportar()