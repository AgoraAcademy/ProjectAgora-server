import base64
import json
import os
import connexion
from flask import current_app
from Crypto.Cipher import AES
from swagger_server import util, wxLogin, orm
from swagger_server.orm import Learner_db


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
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


def getLearner() -> Learner_db or None:
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    headers = connexion.request.headers
    try:
        sessionKey = headers['token']
    except Exception as e:
        current_app.logger.error(str(e))
        db_session.remove()
        return None
    if db_session.query(orm.Config_db).filter(orm.Config_db.name == 'mode').one_or_none().value == "audit":
        auditAccountList = json.loads(db_session.query(orm.Config_db).filter(orm.Config_db.name == 'auditAccountList').one_or_none().value)
        auditAccount = None
        for account in auditAccountList:
            if account['sessionKey'] == sessionKey:
                auditAccount = db_session.query(orm.Learner_db).filter(orm.Learner_db.id == account['learnerId']).one_or_none()
                return auditAccount
    learner: Learner_db = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    db_session.remove()
    return learner
