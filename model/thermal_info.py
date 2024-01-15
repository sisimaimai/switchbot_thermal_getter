from pydantic import BaseModel
from pydantic import BaseModel, validator
from typing import Optional

from utils import logger

LOGGER = logger.get_logger(__name__)

class ThermalInfo(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]

    @validator('temperature', 'humidity')
    def validate_none(cls, value):
        if value is None:
            LOGGER.warning(f"Attribute is set to None.")
        return value

