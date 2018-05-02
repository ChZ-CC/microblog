import json
import requests
from flask import current_app
from flask_babel import _
from hashlib import md5
from urllib.parse import quote
import random


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))

def baidu_translate(text, source_language, dest_language):
    if 'BD_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['BD_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    appid = current_app.config['BD_TRANSLATOR_ID']
    secret_key = current_app.config['BD_TRANSLATOR_KEY']
    prefix_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secret_key
    sign = md5(sign.encode('utf-8')).hexdigest()
    myurl = '{}?appid={}&q={}&from={}&to={}&salt={}&sign={}'.format(
                prefix_url, appid, quote(text), 
                source_language, dest_language, str(salt), sign)
    r = requests.get(myurl)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    else:
        result = json.loads(r.content.decode('utf-8'))
        if 'trans_result' in result.keys():
            return result['trans_result'][0]['dst']
        else:
            return _('Error: No translation from baidu.')
