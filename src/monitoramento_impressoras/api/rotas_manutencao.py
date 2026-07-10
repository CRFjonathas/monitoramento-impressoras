from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.monitoramento_impressoras.core.database import get_db
from src.monitoramento_impressoras.models.incidente_model import Incidente
from src.monitoramento_impressoras.models.impressora_model import Impressora
from src.monitoramento_impressoras.schemas.incidente_schema import (
    IncidenteCreate,
    IncidenteUpdate,
    IncidenteResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=IncidenteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registra um novo incidente",
)
def criar_incidente(incidente: IncidenteCreate, db: Session = Depends(get_db)):
    # Validação de integridade: a impressora precisa existir
    impressora = (
        db.query(Impressora).filter(Impressora.id == incidente.impressora_id).first()
    )
    if not impressora:
        raise HTTPException(
            status_code=404, detail="Impressora não encontrada no inventário."
        )

    # model_dump() converte o Schema Pydantic num dicionário para o SQLAlchemy
    novo_incidente = Incidente(**incidente.model_dump())
    db.add(novo_incidente)
    db.commit()
    db.refresh(novo_incidente)
    return novo_incidente


@router.get(
    "/", response_model=List[IncidenteResponse], summary="Lista todos os incidentes"
)
def listar_incidentes(db: Session = Depends(get_db)):
    return db.query(Incidente).all()


@router.put(
    "/{incidente_id}",
    response_model=IncidenteResponse,
    summary="Atualiza o status de um incidente",
)
def atualizar_incidente(
    incidente_id: int,
    incidente_atualizado: IncidenteUpdate,
    db: Session = Depends(get_db),
):
    incidente_db = db.query(Incidente).filter(Incidente.id == incidente_id).first()
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente não encontrado.")

    # Atualiza apenas o status de resolvido
    incidente_db.status_resolvido = incidente_atualizado.status_resolvido
    db.commit()
    db.refresh(incidente_db)
    return incidente_db


@router.delete(
    "/{incidente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um incidente",
)
def deletar_incidente(incidente_id: int, db: Session = Depends(get_db)):
    incidente_db = db.query(Incidente).filter(Incidente.id == incidente_id).first()
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente não encontrado.")

    db.delete(incidente_db)
    db.commit()
    return None
