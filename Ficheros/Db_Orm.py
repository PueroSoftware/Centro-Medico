""" Orm: (Object-Relational Mapping o Mapeo Objeto-Relacional)  """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Aquí defines la conexión a tu base de datos
engine = create_engine(
    "mysql+pymysql://root:Root_1234@127.0.0.1/centromedico", #Localhost jose
    echo=True  # <--- Esto imprime en consola el SQL ejecutado
)

Session = sessionmaker(bind=engine)
Base = declarative_base()

# Crea todas las tablas si no existen
Base.metadata.create_all(engine)

