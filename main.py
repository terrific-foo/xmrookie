import requests


TARGET_URL = 'https://github.com/terrific-foo/xmrookie/raw/main/target.zip'


def get_update():
    print(requests.get(TARGET_URL).content)
    