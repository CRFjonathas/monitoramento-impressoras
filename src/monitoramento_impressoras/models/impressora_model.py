from sqlalchemy import Column, Integer, String, Boolean
from src.monitoramento_impressoras.core.database import Base

class Impressora(Base):
    __tablename__ = "impressoras"

    id = Column(Integer, primary_key=True, index=True)
    secao = Column(String, index=True)
    modelo = Column(String, index=True)
    numero_serie = Column(String, unique=True, index=True)
    ip = Column(String, unique=True, index=True)
    
    # Controle de vida útil: permite desativar sem apagar do histórico
    ativa = Column(Boolean, default=True)