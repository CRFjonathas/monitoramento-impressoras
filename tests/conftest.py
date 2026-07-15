import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.monitoramento_impressoras.main import app
from src.monitoramento_impressoras.core.database import Base, get_db
from src.monitoramento_impressoras.models.impressora_model import Impressora
from src.monitoramento_impressoras.models.incidente_model import Incidente

# 1. Cria um banco de dados SQLite temporário na memória RAM
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Mantém o banco vivo na memória para todas as conexões
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Cria um banco novo em folha para cada teste e depois o destrói."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Injeta uma impressora falsa para que possamos testar a criação de incidentes
    impressora_mock = Impressora(
        id=1,
        secao="TI",
        modelo="Impressora Teste",
        numero_serie="TXT-123",
        ip="192.168.0.1",
        ativa=True,
    )
    db.add(impressora_mock)
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Substitui o banco real pelo banco de memória dentro da nossa API."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
