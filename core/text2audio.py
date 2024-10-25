# coding=utf-8
import json

import argparse
import datetime
import random
import os

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

IS_PY3 = True

API_KEY = 'eArDHkaeEEHc4bx9fZGjzUDn'
SECRET_KEY = 'pZOtzJ2tDXupCjuvh4M0a1dEvFYjsYxz'

TEXT = "欢迎使用百度语音合成。"

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
PER = 4103
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 3

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def get_audio_from_text(text):
    parser = argparse.ArgumentParser(description='Text to Speech conversion using Baidu API.')
    parser.add_argument('--out', type=str, default='result.mp3', help='Output MP3 filename')
    parser.add_argument('--input', type=str, default='input.txt', help='Input txt filename')

    args = parser.parse_args()

    token = fetch_token()
    tex = quote_plus(text)  # 此处TEXT需要两次urlencode
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    req = Request(TTS_URL, data.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read()
    except  URLError as err:
        return ""

    random_audio_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join([str(random.randint(1,10)) for i in range(5)])
    audio_path = os.path.join("temp", "image", random_audio_name + ".mp3")
    with open(audio_path, 'wb') as of:
        of.write(result_str)
    return audio_path
