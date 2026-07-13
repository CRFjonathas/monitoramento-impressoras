from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.monitoramento_impressoras.core.database import get_db
from src.monitoramento_impressoras.models.impressora_model import Impressora
from src.monitoramento_impressoras.services.zabbix_service import ZabbixService

router = APIRouter()
zabbix_service = ZabbixService()


@router.get("/{ip}", summary="Busca os níveis de toner e contadores em tempo real")
def obter_telemetria(ip: str, db: Session = Depends(get_db)):
    # 1. Validação local: a impressora é nossa?
    impressora = db.query(Impressora).filter(Impressora.ip == ip).first()
    if not impressora:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Impressora com IP {ip} não está no nosso inventário.",
        )

    # 2. Busca os dados vivos na rede corporativa
    dados_zabbix = zabbix_service.buscar_dados_impressora(ip)

    # Trata caso o Zabbix esteja fora do ar ou recuse a conexão
    if dados_zabbix and "erro" in dados_zabbix:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=dados_zabbix["erro"]
        )

    return {
        "equipamento": impressora.modelo,
        "secao": impressora.secao,
        "zabbix": dados_zabbix,
    }
