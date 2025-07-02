# Gui_Doctor/HorarioDoc_Crud.py
"""
from datetime import datetime


class RegistroAsistenciaService:

    @staticmethod
    def registrar_entrada(cedula_doctor, fecha, hora_entrada):
       
        session = Session()
        try:
            doctor = session.query(Doctor).filter_by(cedula_doctor=cedula_doctor).first()
            if not doctor:
                print(f"❌ No se encontró doctor con cédula {cedula_doctor}")
                return

            nuevo_registro = RegistroAsistencia(
                id_doctor=doctor.id_doctor,
                fecha=fecha,
                hora_entrada=hora_entrada
            )
            session.add(nuevo_registro)
            session.commit()
            print(f"✅ Entrada registrada para doctor ID {doctor.id_doctor} en {fecha} a las {hora_entrada}")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Error al registrar entrada: {e}")
        finally:
            session.close()

    @staticmethod
    def registrar_salida(cedula_doctor):
       
        session = Session()
        try:
            doctor = session.query(Doctor).filter_by(cedula_doctor=cedula_doctor).first()
            if not doctor:
                print(f"❌ No se encontró doctor con cédula {cedula_doctor}")
                return

            ahora = datetime.now().time()

            # Buscar el registro más reciente sin hora_salida
            registro = session.query(RegistroAsistencia).filter_by(
                id_doctor=doctor.id_doctor,
                hora_salida=None
            ).order_by(RegistroAsistencia.fecha.desc(), RegistroAsistencia.hora_entrada.desc()).first()

            if not registro:
                print(f"⚠️ No había registro pendiente de salida para doctor ID {doctor.id_doctor}")
                return

            registro.hora_salida = ahora
            session.commit()
            print(f"✅ Salida registrada para doctor ID {doctor.id_doctor} a las {ahora}")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Error al registrar salida: {e}")
        finally:
            session.close() """
