from sqlalchemy import Column, Integer, String, Text,Date,Boolean # Importación de tipos de columnas para definir el modelo ORM (campos tipo entero, texto corto y texto largo)
from sqlalchemy.exc import SQLAlchemyError # Importación del manejados de errores de SQLAlchemy para capturar excepciones durante las operaciones con la BD
from Ficheros.Db_Orm import Base, Session, engine

# Definición del modelo
class Paciente(Base):
    __tablename__ = 'Pacientes'

    id_paciente = Column(Integer, primary_key=True, autoincrement=True)
    cedula_id = Column(String(20), unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(Text, nullable=True)
    estado_activo = Column(Boolean, default=True)

    # Agrega más campos aquí según la estructura real
    @staticmethod
    def create(cedula_id, nombre, apellido_paterno, apellido_materno,
               fecha_nacimiento, email, telefono, direccion):
        session = Session()
        try:
            nuevo = Paciente(
                cedula_id=cedula_id,
                nombres=nombre,
                apellido_paterno=apellido_paterno,   # <-- CORRECTO
                apellido_materno=apellido_materno,   # <-- CORRECTO
                fecha_nacimiento=fecha_nacimiento,
                email=email,
                telefono=telefono,
                direccion=direccion
            )
            session.add(nuevo)
            session.commit()
            print("✅ Paciente creado con éxito.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error al crear paciente: {e}")  # Verás el mensaje en la consola
        finally:
            session.close()


    def __repr__(self) :
        return (f"<Paciente("
                f"{self.cedula_id},"
                f" {self.nombres} "
                f"{self.apellido_paterno}"
                f" {self.apellido_materno}"
                f" {self.fecha_nacimiento}"
                f" {self.email}"
                f" {self.telefono}"
                f" {self.direccion} "
                f")>")

    @staticmethod
    def read_all():
        session = Session()
        try:
            pacientes = session.query(Paciente).filter_by(estado_activo=True).all()

            for p in pacientes:
                print(
                    f"{p.id_paciente}"
                    f"  {p.cedula_id} "
                    f"- {p.nombres}"
                    f" {p.apellido_paterno}"
                    f" {p.apellido_materno}- "
                    f"{p.email}"
                    f" {p.telefono}"
                    f"  {p.direccion}"
                )
            return pacientes
        except Exception as e:
            print(f"❌ Error al leer pacientes: {e}")
            return []
        finally:
            session.close() # cierra session del read all

    @staticmethod
    def update(cedula_id, data):
        """
        Actualiza los campos de un paciente identificado por cedula_id con los valores en data.
        Parámetros:
          cedula_id (str): Identificador único del paciente.
          data (dict): Diccionario con los campos a actualizar. Ejemplo:
                       {"nombres": "Nuevo Nombre", "direccion": "Nueva dirección"}
        """
        session = Session()
        try:
            paciente = session.query(Paciente).filter_by(cedula_id=cedula_id).first()
            if paciente:
                for key, value in data.items():
                    # Asegurarse de que el atributo exista
                    if hasattr(paciente, key):
                        setattr(paciente, key, value)
                session.commit()
                print("✅ Paciente actualizado con éxito.")
            else:
                print(f"❌ No se encontró paciente con cédula {cedula_id}.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error al actualizar el paciente: {e}")
        finally:
            session.close()

    @staticmethod
    def delete(cedula_id):
        """
        Elimina el paciente identificado por cedula_id de la base de datos.

        Parámetros:
          cedula_id (str): Identificador único del paciente a eliminar.
        """
        session = Session()
        try:
            paciente = session.query(Paciente).filter_by(cedula_id=cedula_id).first()
            if paciente:
                paciente.estado_activo = False
                session.commit()
                print("🗑️ Paciente eliminado con éxito.")
            else:
                print(f"❌ No se encontró paciente con cédula {cedula_id}.")
        except Exception as e:
            session.rollback()
            print(f"❌ Error al eliminar el paciente: {e}")
        finally:
            session.close()


# Probar conexión y sesión
try:
    with engine.connect() as connection:
        print("✅ Conexión con SQLAlchemy exitosa.")

    session = Session()
    print("✅ Sesión creada con éxito.")
    session.close() # Aquí puedes agregar una prueba con el modelo
except SQLAlchemyError as error:
    print(f"❌ Error al conectar con la base de datos: {error}")
