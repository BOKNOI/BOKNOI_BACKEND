from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import urllib
import urllib.request
import json

REPLY_ENDPOINT_URL = 'https://api.line.me/v2/bot/message/push'

ACCESSTOKEN = '+Ewuw0RQ9uyMvALJFQ4mcIZyUWqZhGX5Fmr2xUYIq/ZVukpyqTSnocHTB1M3kRciFlco6c1Q7aUU0yBAdIHiyBG5M4vBPamBPE+D4MOMygwDGbGEkHR0MF+1/LfUyU8Tb+M7SEOsB0AYhCi+OaCXIwdB04t89/1O/w1cDnyilFU='

HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

@csrf_exempt
class LineMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token): 
        body = {
            'to': reply_token,
            'messages': self.messages
        }

        # print(body)

        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)

        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)