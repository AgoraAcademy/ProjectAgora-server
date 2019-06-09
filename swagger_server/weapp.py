import base64
import json
import os
import connexion
from Crypto.Cipher import AES
from swagger_server import util, wxLogin, orm


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def getLearner() -> str:
    db_session = orm.init_db(os.environ["DATABASEURI"])
    headers = connexion.request.headers
    try:
        sessionKey = headers['token']
    except Exception as e:
        db_session.remove()
        return {"error": e}
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    db_session.remove()
    return learner
