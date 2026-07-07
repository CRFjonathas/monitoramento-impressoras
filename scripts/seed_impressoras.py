import os
import sys
import pandas as pd

# Adiciona a raiz do projeto ao path para o Python encontrar o pacote 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.monitoramento_impressoras.core.database import SessionLocal, engine, Base
from src.monitoramento_impressoras.models.impressora_model import Impressora

def processar_planilha(caminho_planilha: str):
    # Cria o arquivo banco.db e a estrutura da tabela
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Lê o arquivo Excel garantindo o formato correto
        df = pd.read_excel(caminho_planilha)
        registros = 0
        
        for index, linha in df.iterrows():
            ip = str(linha.get('IP')).strip()
            
            # Pula linhas que não possuem IP válido
            if pd.isna(linha.get('IP')) or not ip:
                continue
                
            # Verifica se o IP já existe no banco para não duplicar dados
            existe = db.query(Impressora).filter(Impressora.ip == ip).first()
            if not existe:
                nova_impressora = Impressora(
                    secao=str(linha.get('SEÇÃO')),
                    modelo=str(linha.get('MODELO')),
                    numero_serie=str(linha.get('N° SÉRIE')),
                    ip=ip,
                    ativa=True
                )
                db.add(nova_impressora)
                registros += 1
                
        db.commit()
        print(f"✅ Carga concluída! {registros} impressoras injetadas com sucesso no banco de dados.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao processar o inventário: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Aponta para o arquivo na raiz do projeto
    caminho_arquivo = "impressoras.xlsx"
    
    if os.path.exists(caminho_arquivo):
        processar_planilha(caminho_arquivo)
    else:
        print(f"⚠️ Atenção: O arquivo '{caminho_arquivo}' não foi encontrado na raiz do projeto.")