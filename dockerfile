# 1. Imagem base oficial do Python 3.12 (versão slim para ser mais leve)
FROM python:3.12-slim

# 2. Define onde o código vai morar dentro do contêiner
WORKDIR /app

# 3. Instala o Poetry globalmente no contêiner
RUN pip install poetry

# 4. Copia apenas os arquivos de dependência primeiro (otimização de cache)
COPY pyproject.toml poetry.lock* ./

# 5. Configura o Poetry para não criar ambiente virtual (já estamos isolados no contêiner) 
# e instala as dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 6. Copia todo o resto do código da sua máquina para o contêiner
COPY . .

# 7. Expõe a porta que a API vai usar
EXPOSE 8000

# 8. O comando que mantém o servidor de pé
CMD ["uvicorn", "src.monitoramento_impressoras.main:app", "--host", "0.0.0.0", "--port", "8000"]