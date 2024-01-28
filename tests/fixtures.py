import pytest
from unittest.mock import patch


@pytest.fixture
def mock_settings():
    with patch.dict(
        "os.environ",
        {
            "SWITCHBOT_TOKEN": "dummy_token",
            "SWITCHBOT_SECRET": "THISISSECRET",
            "DEVICE_IDS": '["dummy_device_id1", "dummy_device_id2"]',
        },
    ):
        yield
