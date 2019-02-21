import requests
import os
import connexion
from swagger_server import util, wxLogin, orm

db_session = None
db_session = orm.init_db(os.environ["DATABASEURI"])


def validateAccessToken(openid, access_token) -> bool:
    try:
        result = requests.get("https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s" % (access_token, openid)).json()
        errcode = result["errcode"]
    except Exception as e:
        return {"error": e, "result": result}
    if errcode == 0:
        return True
    else:
        return False


def refreshToken(refresh_token) -> dict:
    WXLOGINAPPID: str = os.environ['WXLOGINAPPID']
    try:
        refresh_result = requests.get("https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s" % (WXLOGINAPPID, refresh_token)).json()
        access_token = refresh_result["access_token"]
        refresh_token = refresh_result["refresh_token"]
    except Exception as e:
        return {"error": e, "refresh_result": refresh_result}
    return {"access_token": access_token, "refresh_token": refresh_token}


def getWeChatInfo(openid, access_token) -> dict:
    try:
        result = requests.get("https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s" % (access_token, openid)).json()
        nickname = result["nickname"]
        sex = result["sex"]
        unionid = result["unionid"]
    except Exception as e:
        return {"error": e, "result": result}
    return {"nickname": nickname, "sex": sex, "unionid": unionid}


def validateUser() -> dict:
    headers = connexion.request.headers
    try:
        access_token = headers['Authorization']
        refresh_token = headers['refresh_token']
        openid = headers['openid']
        if not validateAccessToken(openid, access_token):
            try:
                refresh_result = refreshToken(refresh_token)
                access_token = refresh_result["access_token"]
                refresh_token = refresh_result["refresh_token"]
            except Exception:
                return {"result": False}
    except Exception:
        return {"result": False}
    return {"result": True, "access_token": access_token, "refresh_token": refresh_token, "openid": openid}
