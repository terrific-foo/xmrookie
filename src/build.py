import os
import json
from zipfile import ZipFile
from pathlib import Path

from logger import Logger


_CONFIG_PATH = 'src/config.json'

_PURE_NAME = Path(__file__).stem
_TARGET_FOLDER = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_folder']
_TARGET_ACHIEVE = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_achieve']

logger = Logger(_PURE_NAME)


def compress():
    logger.info('started compressing')
    with ZipFile(_TARGET_ACHIEVE, 'w') as zip_obj:
        for root, _, files in os.walk(_TARGET_FOLDER):
            for file in files:
                logger.debug(f'added {file} to achieve')
                zip_obj.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file),
                        os.path.join(_TARGET_FOLDER, '..')
                    )
                )
    logger.info('finished compressing')


if __name__ == '__main__':
    compress()
