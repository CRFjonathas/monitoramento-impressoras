from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Centro de Comando de Telemetria",
    description="Sistema de gerenciamento, monitoramento (Zabbix) e manutenção do parque de impressão.",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
async def root():
    # Redireciona a raiz direto para a documentação interativa (Swagger)
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Sistema"])
async def health_check():
    return {"status": "Online", "sistema": "Centro de Comando de Telemetria"}