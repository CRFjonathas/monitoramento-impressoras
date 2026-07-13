def test_criar_incidente_com_sucesso(client):
    """Garante que a API consegue criar um incidente no banco de dados."""
    
    # Arrange: Prepara os dados (Sabemos que o conftest inseriu a impressora ID 1)
    payload = {
        "descricao_defeito": "Cilindro danificado",
        "impressora_id": 1
    }
    
    # Act: Dispara a requisição POST
    response = client.post("/api/v1/manutencao/", json=payload)
    
    # Assert: Verifica se tudo ocorreu como esperado
    assert response.status_code == 201
    dados = response.json()
    assert dados["descricao_defeito"] == "Cilindro danificado"
    assert dados["status_resolvido"] is False
    assert "id" in dados # Verifica se o banco gerou um ID

def test_criar_incidente_impressora_inexistente(client):
    """Garante que a API bloqueia incidentes para impressoras que não existem."""
    
    payload = {
        "descricao_defeito": "Erro genérico",
        "impressora_id": 999  # ID que não existe
    }
    
    response = client.post("/api/v1/manutencao/", json=payload)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Impressora não encontrada no inventário."