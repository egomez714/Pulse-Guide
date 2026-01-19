from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # app will refuse to start if missing
    GEMINI_API_KEY: str
    # api model version
    GEMINI_MODEL_ID : str = "gemini-3-flash-preview"

    #connection to .env file
    model_config = SettingsConfigDict(env_file=".env")

# caches env variables only created once
@lru_cache
def get_settings():
    return Settings()