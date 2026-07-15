import os
import requests
from typing import Optional
from dotenv import load_dotenv


load_dotenv()

class ZabbixService:
    def __init__(self):
        # Busca as credenciais de forma segura do .env
        self.url = os.getenv("ZABBIX_URL")
        self.user = os.getenv("ZABBIX_USER")
        self.password = os.getenv("ZABBIX_PASSWORD")
        self.auth_token: Optional[str] = None

    def _fazer_requisicao(self, metodo: str, parametros: dict) -> dict:
        """Método base para padronizar as chamadas JSON-RPC do Zabbix"""
        payload = {"jsonrpc": "2.0", "method": metodo, "params": parametros, "id": 1}

        # Se já estivermos autenticados, injeta o token na requisição
        if self.auth_token:
            payload["auth"] = self.auth_token

        try:
            resposta = requests.post(self.url, json=payload, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()

            if "error" in dados:
                raise Exception(f"Erro na API do Zabbix: {dados['error']['data']}")

            return dados.get("result")
        except Exception as e:
            print(f"Erro de comunicação com o Zabbix: {e}")
            return None

    def autenticar(self) -> bool:
        """Gera o token de sessão na API do Zabbix"""
        if not self.url or not self.user or not self.password:
            print("Credenciais do Zabbix ausentes no arquivo .env")
            return False

        parametros = {"user": self.user, "password": self.password}

        token = self._fazer_requisicao("user.login", parametros)
        if token:
            self.auth_token = token
            return True

        return False

    def buscar_dados_impressora(self, ip: str) -> dict:
        """Busca o Host no Zabbix pelo IP e extrai os itens (toner/contador)"""

    
        if not self.auth_token:
            sucesso = self.autenticar()
            if not sucesso:
                return {"erro": "Falha de autenticação com o Zabbix"}

        # 1. Busca o ID do Host usando o IP
        hosts = self._fazer_requisicao(
            "host.get",
            {
                "output": ["hostid", "name"],
                "filter": {
                    "ip": [ip]
                },  # O Zabbix permite filtrar hosts pelas interfaces (IP)
            },
        )

        if not hosts:
            return {"erro": f"Impressora com IP {ip} não monitorada pelo Zabbix"}

        host_id = hosts[0]["hostid"]

        # 2. Busca os itens desse Host (Atenção: A chave de busca dos itens vai depender
        # do template SNMP que você usa no Zabbix. Aqui traremos os itens gerais)
        itens = self._fazer_requisicao(
            "item.get",
            {
                "output": ["name", "lastvalue", "units"],
                "hostids": host_id,
                "search": {
                    "name": "Toner"
                },  # Busca itens que contenham "Toner" no nome
                "searchByAny": True,
            },
        )

        return {"host": hosts[0]["name"], "itens": itens}
