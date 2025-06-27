from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
from Ficheros.Db_Orm import Base, Session, engine

class Doctor(Base):
    __tablename__ = 'Doctores'

    id_doctor = Column(Integer, primary_key=True, autoincrement=True)
    cedula_doctor = Column(String(20), unique=True, nullable=False)
    nombres_doctor = Column(String(100), nullable=False)
    apellido_paterno_doctor = Column(String(100), nullable=False)
    apellido_materno_doctor = Column(String(100), nullable=False)
    telefono_doctor = Column(String(20), nullable=False)
    email_doctor = Column(String(100), nullable=False)
    especialidad_doctor = Column(String(100), nullable=False)
    estado_activo = Column(Boolean, default=True)

    @staticmethod
    def create(
            id_doctor,
            cedula_doctor,
            nombres_doctor,
            apellido_paterno_doctor,
            apellido_materno_doctor,
            especialidad_doctor,
            email_doctor,
            telefono_doctor
    ):
        session = Session()
        try:
            nuevo = Doctor(
                cedula=cedula_doctor,
                nombres=nombres_doctor ,
                apellidos=f"{apellido_paterno_doctor} {apellido_materno_doctor}",
                telefono=telefono_doctor,
                email=email_doctor,
                especialidad=especialidad_doctor  # se usa como campo 'especialidad' en modelo
            )
            session.add(nuevo)
            session.commit()
            print("✅ Doctor creado con éxito.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error al crear doctor: {e}")
        finally:
            session.close()

    @staticmethod
    def read_all():
        session = Session()
        try:
            doctores = session.query(Doctor).filter_by(estado_activo=True).all()
            for d in doctores:
                print(
                    f"{d.id_doctor}"
                    f" - {d.nombres_doctor}"
                    f" {d.apellidos} "
                    f"- {d.especialidad_doctor}"
                    f" - {d.telefono_doctor}"
                    f" - {d.email_doctor}")
            return doctores
        except Exception as e:
            print(f"❌ Error al leer doctores: {e}")
            return []
        finally:
            session.close()

    @staticmethod
    def update(cedula_doctor, data):
        session = Session()
        try:
            doctor = session.query(Doctor).filter_by(cedula=cedula_doctor).first()
            if doctor:
                for key, value in data.items():
                    if hasattr(doctor, key):
                        setattr(doctor, key, value)
                session.commit()
                print("🔄 Doctor actualizado con éxito.")
            else:
                print(f"❌ No se encontró doctor con cédula {cedula_doctor}.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error al actualizar doctor: {e}")
        finally:
            session.close()

    @staticmethod
    def delete(cedula_doctor):
        session = Session()
        try:
            doctor = session.query(Doctor).filter_by(cedula=cedula_doctor).first()
            if doctor:
                doctor.estado_activo = False
                session.commit()
                print("🗑️ Doctor eliminado correctamente.")
            else:
                print(f"❌ No se encontró doctor con cédula {cedula_doctor}.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error al eliminar doctor: {e}")
        finally:
            session.close()
