import json
import time
import hashlib
import hmac
import base64
import uuid
import os
import dataclasses
import requests
import click
from urllib.parse import urljoin

from utils.logger import get_logger
from model.switchbot_device import SwitchbotDevice

LOGGER = get_logger(__name__)


@dataclasses.dataclass
class SwitchBotApi:
    base_url: str = "https://api.switch-bot.com"
    token: str = os.environ["SWITCHBOT_TOKEN"]
    secret: str = os.environ["SWITCHBOT_SECRET"]

    def _get_header(self) -> str:
        """SwitchBotのAPIを叩く際に必要な共通ヘッダ

        参考文献: https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#python-3-example-code
        """
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))  # NOTE: *1000ってなんだろう。。
        string_to_sign = "{}{}{}".format(self.token, t, nonce)

        sign = base64.b64encode(
            hmac.new(
                bytes(self.secret, "utf-8"),
                msg=bytes(string_to_sign, "utf-8"),
                digestmod=hashlib.sha256,
            ).digest()
        )

        LOGGER.debug(
            f"Authorization: {self.token}\n"
            f"t: {t}\n"
            f"sign: {str(sign, 'utf-8')}\n"
            f"nonce: {nonce}"
        )

        return {
            "Authorization": self.token,
            "t": str(t),
            "sign": sign,
            "nonce": str(nonce),
            # 本当はPOSTとかのときだけで良い
            "Content-Type": "application/json",
            "charset": "utf8",
        }

    def _do_get_request(self, endpoint: str) -> requests.Response():
        """GETリクエスト

        Args:
            endpoint (str): エンドポイント名

        Raises:
            ValueError: リクエストが失敗したとき

        Returns:
            requests.Response: レスポンス
        """
        url = urljoin(self.base_url, endpoint)
        headers = self._get_header()
        LOGGER.debug(url)
        LOGGER.debug(headers)

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError("request failed: {}".format(response.content))

        return response

    def get_devices(self) -> list[SwitchbotDevice]:
        """デバイス一覧取得

        Returns:
            List[SwitchbotDevice]: デバイスのリスト
        """
        response = self._do_get_request("/v1.1/devices")
        content = json.loads(response.content)
        device_list = content.get("body", {}).get("deviceList", [])
        devices = [
            SwitchbotDevice(
                deviceId=device.get("deviceId"),
                deviceName=device.get("deviceName"),
                deviceType=device.get("deviceType"),
                enableCloudService=device.get("enableCloudService"),
                hubDeviceId=device.get("hubDeviceId")
            )
            for device in device_list
        ]
        return devices

    def get_thermal_info(self, thermal_device_id: str) -> dict:
        """温度情報取得

        Args:
            thermal_device_id (str): センサーのデバイスID

        Returns:
            dict: _description_
        """

        response = self._do_get_request(f"/v1.1/devices/{thermal_device_id}/status")
        content = response.content
        return json.loads(content)


@click.command()
@click.argument("api")
@click.option("--device_id")
def main(api: str, device_id: str):
    if api == "devices":
        print(SwitchBotApi().get_devices())
    elif api == "thermal_info":
        print(SwitchBotApi().get_thermal_info(device_id))


if __name__ == "__main__":
    main()