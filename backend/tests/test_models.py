import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import models  # noqa: F401

@pytest.fixture
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine

def test_all_tables_created(db_engine):
    inspector = inspect(db_engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "user_profiles" in tables
    assert "likes" in tables
    assert "matches" in tables
    assert "messages" in tables

def test_user_model_fields(db_engine):
    inspector = inspect(db_engine)
    columns = [c["name"] for c in inspector.get_columns("users")]
    assert "telegram_id" in columns
    assert "pseudonym" in columns
    assert "is_premium" in columns
