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
    "telegram_id": 12345,
    "pseudonym": "Анна",
    "about_me": "Люблю звёзды и кофе",
    "gender": "female",
    "orientation": "hetero",
    "age": 29,
    "city": "Москва",
    "pref_gender": "male",
    "pref_age_min": 27,
    "pref_age_max": 40,
    "pref_relation_type": "serious"
}

def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register_user(client):
    r = client.post("/users/register", json=USER_DATA)
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_register_duplicate_fails(client):
    client.post("/users/register", json=USER_DATA)
    r = client.post("/users/register", json=USER_DATA)
    assert r.status_code == 400

def test_update_birth_data(client):
    client.post("/users/register", json=USER_DATA)
    r = client.post("/users/12345/birth-data", json={
        "birth_date": "15.03.1995",
        "full_name": "Иванова Анна Сергеевна"
    })
    assert r.status_code == 200
    data = r.json()
    assert "life_path" in data
    assert "zodiac" in data
    assert data["zodiac"] == "Рыбы"

def test_submit_psychotype_test(client):
    client.post("/users/register", json=USER_DATA)
    r = client.post("/users/12345/test", json={
        "test_type": "psychotype",
        "answers": ["I", "F", "N", "J", "F", "I", "N", "J"]
    })
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_get_profile(client):
    client.post("/users/register", json=USER_DATA)
    client.post("/users/12345/birth-data", json={"birth_date": "15.03.1995"})
    r = client.get("/users/12345/profile")
    assert r.status_code == 200
    data = r.json()
    assert data["pseudonym"] == "Анна"
    assert data["zodiac_sign"] == "Рыбы"
