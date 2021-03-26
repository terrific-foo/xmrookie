import json
from zipfile import ZipFile
from pathlib import Path
from urllib import request

from logger import Logger


_CONFIG_PATH = 'config.json'

_PURE_NAME = Path(__file__).stem
_TARGET_URL = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_url']
_TARGET_FOLDER = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_folder']
_TARGET_ZIP = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_zip']

logger = Logger(_PURE_NAME)


def get_update():
    logger.info(f'started updating from {_TARGET_URL}')
    target = request.urlopen(_TARGET_URL).read()
    logger.debug('target file downloaded')
    open(_TARGET_ZIP, 'wb').write(target)
    logger.debug('target file dumped')
    ZipFile(_TARGET_ZIP, 'r').extractall(_TARGET_FOLDER)
    logger.debug('target file extarcted')
    logger.info('finished updating')


if __name__=='__main__':
    get_update()