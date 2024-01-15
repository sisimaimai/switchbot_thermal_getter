from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    device_ids: list[str]
    switchbot_token: str
    switchbot_secret: str


settings = Settings()
