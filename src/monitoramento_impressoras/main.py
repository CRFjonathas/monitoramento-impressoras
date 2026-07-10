from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.monitoramento_impressoras.api import (
    rotas_impressao,
    rotas_manutencao,
)  # <--- NOVA IMPORTAÇÃO
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


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Sistema"])
async def health_check():
    return {"status": "Online", "sistema": "Centro de Comando de Telemetria"}
