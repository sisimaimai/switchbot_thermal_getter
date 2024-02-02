import functions_framework
from api import SwitchBotApi
from settings import Settings
from flask import Response

SETTINGS = Settings()


@functions_framework.http
def main(request) -> Response:
    api = SwitchBotApi()
    device_id = request.args.get("device_id")
    thermal_info = api.get_thermal_info(device_id)

    return thermal_info.model_dump_json()
