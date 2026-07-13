from unittest.mock import patch

def test_obter_telemetria_com_sucesso(client):
    """Simula a resposta do Zabbix e testa a rota de telemetria sem usar a rede."""
    
    # 1. Arrange: Dados falsos que fingiremos que o Zabbix retornou
    dados_mockados = {
        "host": "Impressora Teste Zabbix",
        "itens": [
            {"name": "Toner Preto", "lastvalue": "80", "units": "%"}
        ]
    }
    
    # O 'patch' intercepta a função real exatamente onde ela foi importada no arquivo de rotas
    with patch("src.monitoramento_impressoras.api.rotas_telemetria.zabbix_service.buscar_dados_impressora") as mock_zabbix:
        
        # Dizemos ao mock: "Quando você for chamado, devolva este dicionário mágico"
        mock_zabbix.return_value = dados_mockados
        
        # 2. Act: Fazemos a requisição para a NOSSA API usando o IP da impressora do conftest.py
        response = client.get("/api/v1/telemetria/192.168.0.1")
        
        # 3. Assert: Verificamos se a nossa API processou o Mock corretamente
        assert response.status_code == 200
        dados = response.json()
        
        # Valida dados que vieram do NOSSO banco de dados em memória
        assert dados["equipamento"] == "Impressora Teste"
        # Valida dados que vieram do ZABBIX (nosso mock)
        assert dados["zabbix"]["host"] == "Impressora Teste Zabbix"
        assert dados["zabbix"]["itens"][0]["lastvalue"] == "80"

        # Garante que a função do Zabbix foi realmente chamada durante o teste
        mock_zabbix.assert_called_once_with("192.168.0.1")

def test_obter_telemetria_impressora_nao_cadastrada(client):
    """Garante que a API retorna 404 antes de tentar chamar o Zabbix."""
    
    # Usa um IP que não colocamos no nosso banco em memória (conftest.py)
    response = client.get("/api/v1/telemetria/10.0.0.99")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Impressora com IP 10.0.0.99 não está no nosso inventário."