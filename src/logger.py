import logging
import json
from pathlib import Path

CONFIG_PATH = 'config.json'

PURE_NAME = Path(__file__).stem
_LEVEL = json.load(open(CONFIG_PATH, 'r'))[PURE_NAME]['level']
_SAVE_IN_FILE = json.load(open(CONFIG_PATH, 'r'))[PURE_NAME]['save_in_file']
_FORMAT = json.load(open(CONFIG_PATH, 'r'))[PURE_NAME]['format']

class Logger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name, level=_LEVEL)
        formatter = logging.Formatter(_FORMAT)
        if _SAVE_IN_FILE:
            handler = logging.FileHandler(
                name=f'{name}.log',
                mode='a'
            )
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(_LEVEL)
        self.addHandler(handler)