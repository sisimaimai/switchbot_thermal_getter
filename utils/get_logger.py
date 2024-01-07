import logging
import os

def get_logger(name: str) -> logging.Logger:
    loglevel = os.environ.get("LOGLEVEL", logging.INFO)

    # 出力設定作成
    channel = logging.StreamHandler()
    channel.setLevel(loglevel)
    channel.setFormatter(
        logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    )

    # ロガー作成
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    logger.addHandler(channel)

    return logger
