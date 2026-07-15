from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Depends
from src.monitoramento_impressoras.core.database import get_db
from src.monitoramento_impressoras.models.impressora_model import Impressora

from src.monitoramento_impressoras.api import (
    rotas_impressao,
    rotas_manutencao,
    rotas_telemetria,
)

app = FastAPI(
    title="Centro de Comando de Telemetria",
    description="Sistema de gerenciamento, monitoramento (Zabbix) e manutenção do parque de impressão.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="src/monitoramento_impressoras/static"),
    name="static",
)
templates = Jinja2Templates(directory="src/monitoramento_impressoras/templates")

origens_permitidas = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Acoplamento das Rotas
app.include_router(
    rotas_impressao.router, prefix="/api/v1/impressao", tags=["Motor de Impressão"]
)
app.include_router(
    rotas_manutencao.router, prefix="/api/v1/manutencao", tags=["Manutenção"]
)
app.include_router(
    rotas_telemetria.router, prefix="/api/v1/telemetria", tags=["Monitoramento Zabbix"]
)


@app.get("/", tags=["Frontend"], include_in_schema=False)
async def renderizar_dashboard(request: Request, db: Session = Depends(get_db)):
    # Busca todas as impressoras no banco de dados
    lista_impressoras = db.query(Impressora).all()

    # Injeta a lista no contexto do Jinja2
    contexto = {
        "titulo": "Centro de Comando de Telemetria",
        "impressoras": lista_impressoras,
    }

    return templates.TemplateResponse(
        request=request, name="index.html", context=contexto
    )


@app.get("/health", tags=["Sistema"])
async def health_check():
    return {"status": "Online", "sistema": "Centro de Comando de Telemetria"}
