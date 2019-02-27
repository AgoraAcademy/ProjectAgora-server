import connexion
import six
import os
import requests

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util, orm


def oauth2_get(code, state):  # noqa: E501
    """OAUTH2回调接口

    # noqa: E501

    :param code: Code
    :type code: str
    :param state: state
    :type state: str

    :rtype: InlineResponse200
    """
    print(code)
    db_session = orm.init_db(os.environ["DATABASEURI"])
    WXLOGINAPPID: str = os.environ['WXLOGINAPPID']
    WXLOGINSECRET: str = os.environ['WXLOGINSECRET']
    result = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (WXLOGINAPPID, WXLOGINSECRET, code))
    resultjson = result.json()
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == resultjson['openid']).one_or_none()
    if not learner:
        try:
            db_session.remove()
            return {
                'access_token': resultjson['access_token'],
                'expires_in': resultjson['expires_in'],
                'refresh_token': resultjson['refresh_token'],
                'openid': resultjson['openid'],
                'isLearner': False
            }
        except Exception as e:
            db_session.remove()
            return {"error": str(e)}, 401
    else:
        try:
            db_session.remove()
            return {
                'access_token': resultjson['access_token'],
                'expires_in': resultjson['expires_in'],
                'refresh_token': resultjson['refresh_token'],
                'openid': resultjson['openid'],
                'fullname': learner.familyName + learner.givenName,
                'learnerId': learner.id,
                'validated': learner.validated,
                'isLearner': True,
                'isMentor': learner.isMentor,
                'isAdmin': learner.isAdmin
            }
        except Exception as e:
            db_session.remove()
            return {"error": str(e)}, 401
