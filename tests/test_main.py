from fastapi.testclient import TestClient
from src.monitoramento_impressoras.main import app

# Cria um "cliente falso" que consegue fazer requisições para a nossa API
client = TestClient(app)


def test_health_check_deve_retornar_200_e_status_online():
    """Testa se o endpoint de saúde da API está respondendo corretamente."""
    # Act: Executa a ação (faz o GET na rota)
    response = client.get("/health")

    # Assert: Verifica se o resultado é exatamente o que esperávamos
    assert response.status_code == 200
    assert response.json() == {
        "status": "Online",
        "sistema": "Centro de Comando de Telemetria",
    }
