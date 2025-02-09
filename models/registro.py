from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database.database import Base

class RegistroSistema(Base):
    __tablename__ = "registros_sistema"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cpu_uso = Column(Float, nullable=False)
    memoria_uso = Column(Float, nullable=False)
    red_subida = Column(Float, nullable=False)
    red_bajada = Column(Float, nullable=False)
    procesos_activos = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    usuario = relationship("Usuario", back_populates="registros")
