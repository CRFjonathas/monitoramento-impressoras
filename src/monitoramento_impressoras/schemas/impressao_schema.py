from pydantic import BaseModel, Field


class DisparoImpressao(BaseModel):
    ip_impressora: str = Field(..., description="IP da impressora de destino")
    caminho_arquivo: str = Field(
        ..., description="Caminho do arquivo PDF local para impressão"
    )
