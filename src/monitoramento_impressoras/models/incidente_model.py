from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from src.monitoramento_impressoras.core.database import Base


class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)

    # Chave estrangeira ligando o incidente à impressora específica
    impressora_id = Column(Integer, ForeignKey("impressoras.id"), nullable=False)

    # Detalhes do defeito
    descricao_defeito = Column(String, nullable=False)

    # Status atual (Se False, é um defeito atual. Se True, já foi solucionado)
    status_resolvido = Column(Boolean, default=False)

    # Timestamp automático gerenciado pelo próprio banco de dados
    data_registro = Column(DateTime(timezone=True), server_default=func.now())
