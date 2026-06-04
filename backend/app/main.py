from fastapi import FastAPI
from app.database import engine, Base
from app import models  # noqa: F401

app = FastAPI(title="Душа в душу API", version="1.0.0")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok", "app": "Душа в душу"}
