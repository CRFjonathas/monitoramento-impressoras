from pydantic import BaseModel, Field
from datetime import datetime


# Base para compartilhar campos comuns
class IncidenteBase(BaseModel):
    descricao_defeito: str = Field(
        ..., description="Descrição detalhada do defeito apresentado"
    )


# Schema exigido no POST (Criação)
class IncidenteCreate(IncidenteBase):
    impressora_id: int = Field(..., description="ID da impressora cadastrada no banco")


# Schema exigido no PUT (Atualização/Solução)
class IncidenteUpdate(BaseModel):
    status_resolvido: bool = Field(
        ..., description="Define se o incidente foi solucionado (True) ou não (False)"
    )


# Schema de Saída (O que a API devolve)
class IncidenteResponse(IncidenteBase):
    id: int
    impressora_id: int
    status_resolvido: bool
    data_registro: datetime

    # Permite que o Pydantic leia diretamente os objetos do SQLAlchemy
    class Config:
        from_attributes = True
