from database import database
from models.usuario import Usuario
from models.registro import RegistroSistema
from models.alerta import Alerta

def create_tables():
    database.Base.metadata.create_all(bind=database.engine)
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    create_tables()
