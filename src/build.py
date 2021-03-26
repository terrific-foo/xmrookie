import json
from shutil import make_archive
from pathlib import Path

from logger import Logger


_CONFIG_PATH = 'config.json'

_PURE_NAME = Path(__file__).stem
_TARGET_FOLDER = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_folder']
_TARGET_ZIP = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_zip']

logger = Logger(_PURE_NAME)


def compress():
    logger.info('started compressing')
    make_archive(_TARGET_ZIP.replace('.zip', ''), 'zip', _TARGET_FOLDER)
    logger.info('finished compressing')


if __name__ == '__main__':
    compress()
