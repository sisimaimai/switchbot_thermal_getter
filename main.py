import datetime

import functions_framework
import flask

from api import SwitchBotApi
from settings import Settings

SETTINGS = Settings()


@functions_framework.http
def main(request: flask.Request) -> flask.Response:
    device_id = request.args.get("device_id")
    now = datetime.datetime.now()

    api = SwitchBotApi()
    thermal_info = api.get_thermal_info(device_id)

    return thermal_info.model_dump_json()
