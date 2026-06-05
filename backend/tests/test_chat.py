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


USER_A = {
    "telegram_id": 11111, "pseudonym": "Алекс", "about_me": "Тест",
    "gender": "male", "orientation": "hetero", "age": 30, "city": "Москва",
    "pref_gender": "female", "pref_age_min": 25, "pref_age_max": 40,
    "pref_relation_type": "serious"
}
USER_B = {
    "telegram_id": 22222, "pseudonym": "Нина", "about_me": "Тест",
    "gender": "female", "orientation": "hetero", "age": 28, "city": "Москва",
    "pref_gender": "male", "pref_age_min": 25, "pref_age_max": 40,
    "pref_relation_type": "serious"
}


def make_match(client):
    """Регистрирует двух пользователей и создаёт матч через взаимный лайк."""
    r_a = client.post("/users/register", json=USER_A)
    r_b = client.post("/users/register", json=USER_B)
    user_a_id = r_a.json()["user_id"]
    user_b_id = r_b.json()["user_id"]
    client.post(f"/likes/11111/like/{user_b_id}")
    r = client.post(f"/likes/22222/like/{user_a_id}")
    match_id = r.json()["match_id"]
    return match_id, user_a_id, user_b_id


def test_get_messages_empty(client):
    match_id, _, _ = make_match(client)
    r = client.get(f"/chat/{match_id}?telegram_id=11111")
    assert r.status_code == 200
    assert r.json()["messages"] == []


def test_send_message(client):
    match_id, _, _ = make_match(client)
    r = client.post(
        f"/chat/{match_id}/send?telegram_id=11111",
        json={"text": "Привет!"}
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_send_and_receive_message(client):
    match_id, _, _ = make_match(client)
    client.post(f"/chat/{match_id}/send?telegram_id=11111", json={"text": "Привет!"})
    r = client.get(f"/chat/{match_id}?telegram_id=11111")
    messages = r.json()["messages"]
    assert len(messages) == 1
    assert messages[0]["text"] == "Привет!"
    assert messages[0]["is_mine"] is True


def test_message_is_mine_flag(client):
    match_id, _, _ = make_match(client)
    client.post(f"/chat/{match_id}/send?telegram_id=11111", json={"text": "Привет!"})
    r = client.get(f"/chat/{match_id}?telegram_id=22222")
    messages = r.json()["messages"]
    assert messages[0]["is_mine"] is False


def test_access_denied_for_stranger(client):
    match_id, _, _ = make_match(client)
    client.post("/users/register", json={**USER_A, "telegram_id": 33333, "pseudonym": "Чужой"})
    r = client.get(f"/chat/{match_id}?telegram_id=33333")
    assert r.status_code == 403


def test_send_message_resets_expiry(client):
    match_id, _, _ = make_match(client)
    r_before = client.get(f"/chat/{match_id}?telegram_id=11111")
    client.post(f"/chat/{match_id}/send?telegram_id=11111", json={"text": "Сброс!"})
    r_after = client.get(f"/chat/{match_id}?telegram_id=11111")
    new_expiry = r_after.json().get("match_expires_at")
    assert new_expiry is not None
