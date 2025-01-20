from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TG_TOKEN: str = ""
    BROKER_URL: str = ""
    S3_API: str = ""
    CHAT_ID: str = ""


settings = Settings()
