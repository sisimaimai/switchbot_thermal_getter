from pydantic import BaseSettings

class Settings(BaseSettings):
    device_ids: list[str]
    switchbot_token: str
    switchbot_secret: str