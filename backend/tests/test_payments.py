import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture
def client():
    engine = create_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


USER_DATA = {
    "telegram_id": 12345, "pseudonym": "Тест", "about_me": "",
    "gender": "female", "orientation": "hetero", "age": 25, "city": "Москва",
    "pref_gender": "male", "pref_age_min": 20, "pref_age_max": 40,
    "pref_relation_type": "serious"
}


def test_activate_premium(client):
    client.post("/users/register", json=USER_DATA)
    r = client.post("/payments/activate/12345")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_activate_premium_sets_expiry(client):
    client.post("/users/register", json=USER_DATA)
    r = client.post("/payments/activate/12345")
    assert "premium_expires" in r.json()


def test_activate_premium_unknown_user(client):
    r = client.post("/payments/activate/99999")
    assert r.status_code == 404
