from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./dusha.db"
    telegram_bot_token: str = ""
    secret_key: str = "dev-secret"
    # В Railway задать: https://yourapp.railway.app
    backend_url: str = "http://localhost:8000"
    # В Railway задать: https://yourapp.railway.app/app/
    mini_app_url: str = "http://localhost:8000/app/"

    class Config:
        env_file = ".env"

settings = Settings()
