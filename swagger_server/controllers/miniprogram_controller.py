import connexion
import six
import os
import requests
from flask import Flask, send_from_directory

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util, orm


def miniprogram_qr_get(qrtype):  # noqa: E501
    if qrtype == "dMGsnKEKLe.txt":
        return send_from_directory(os.path.dirname(os.environ["MINIPROGRAM_QR_VERIFICATION_FILE"]), 'dMGsnKEKLe.txt')


def miniprogram_login(js_code):
    MINIPROGRAM_APPID: str = os.environ['MINIPROGRAM_APPID']
    MINIPROGRAM_APPSECRET: str = os.environ['MINIPROGRAM_APPSECRET']
    try:
        result = requests.get("https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (MINIPROGRAM_APPID, MINIPROGRAM_APPSECRET, js_code))
        resultjson = result.json()
    except Exception as e:
        return {"error": str(e)}, 401
    return {'openid': resultjson['openid'], 'token': resultjson['session_key']}, 200


def miniprogram_ping():
    return {'message': 'pinged!'}, 200
