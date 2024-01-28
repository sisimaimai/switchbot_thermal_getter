from pydantic import BaseModel
from typing import Optional

from utils import logger

LOGGER = logger.get_logger(__name__)


class ThermalInfo(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]

    def validate(self):
        if self.temperature is None or self.humidity is None:
            LOGGER.warning(f"Attribute is set to None.")
