from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.monitoramento_impressoras.core.database import get_db
from src.monitoramento_impressoras.models.impressora_model import Impressora
from src.monitoramento_impressoras.schemas.impressao_schema import DisparoImpressao
from src.monitoramento_impressoras.services.impressao_service import (
    MotorImpressaoService,
)

router = APIRouter()
motor_service = MotorImpressaoService()


@router.post("/disparar", summary="Dispara uma impressão para um IP específico")
def disparar_impressao(dados: DisparoImpressao, db: Session = Depends(get_db)):
    # 1. Verifica se a impressora existe no nosso inventário
    impressora = (
        db.query(Impressora).filter(Impressora.ip == dados.ip_impressora).first()
    )

    if not impressora:
        raise HTTPException(
            status_code=404,
            detail=f"Impressora com IP {dados.ip_impressora} não encontrada no banco.",
        )

    # Aqui, no futuro, faremos um IF baseando-se em impressora.modelo
    # para passar uma flag de cores para o motor, se for a Ricoh IM C300.

    # 2. Executa a regra de negócio
    resultado = motor_service.enviar_arquivo(dados.ip_impressora, dados.caminho_arquivo)

    if resultado["status"] == "erro":
        raise HTTPException(status_code=500, detail=resultado["mensagem"])

    return {
        "mensagem": resultado["mensagem"],
        "equipamento": impressora.modelo,
        "secao": impressora.secao,
    }
