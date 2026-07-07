import socket
import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MotorImpressaoService:
    def __init__(self, porta_tcp: int = 9100):
        self.porta_tcp = porta_tcp

    def _converter_pdf_para_pcl(self, caminho_pdf: str, caminho_pcl: str) -> bool:
        """
        Converte um arquivo PDF para binário PCL utilizando Ghostscript.
        Resolve o problema de loop nas impressoras HP.
        """
        comando = [
            "gs",
            "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER",
            "-sDEVICE=ljet4",
            f"-sOutputFile={caminho_pcl}",
            caminho_pdf
        ]
        
        try:
            subprocess.run(comando, check=True, capture_output=True, text=True)
            logger.info(f"Conversão concluída com sucesso: {caminho_pcl}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro na conversão do Ghostscript: {e.stderr}")
            return False

    def enviar_arquivo(self, ip_impressora: str, caminho_pdf: str) -> dict:
        """
        Orquestra o fluxo de impressão: converte, envia via Socket TCP e limpa os rastros.
        """
        caminho_pcl = caminho_pdf.replace(".pdf", ".pcl")
        
        if not self._converter_pdf_para_pcl(caminho_pdf, caminho_pcl):
            return {"status": "erro", "mensagem": "Falha na conversão para PCL."}

        try:
            with open(caminho_pcl, "rb") as arquivo_binario:
                dados = arquivo_binario.read()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((ip_impressora, self.porta_tcp))
                s.sendall(dados)
                
            return {"status": "sucesso", "mensagem": f"Impresso com sucesso em {ip_impressora}."}
        
        except socket.error as e:
            logger.error(f"Erro de conexão com {ip_impressora}: {e}")
            return {"status": "erro", "mensagem": f"Falha de rede: {str(e)}"}
            
        finally:
            if os.path.exists(caminho_pcl):
                os.remove(caminho_pcl)