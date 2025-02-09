from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database.database import Base

class Alerta(Base):
    __tablename__ = "alertas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    mensaje = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    estado = Column(String, default="pendiente")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    usuario = relationship("Usuario", back_populates="alertas")
