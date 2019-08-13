import connexion
import six
import os
import requests
import datetime
import random
import base64

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util, orm, wxLogin, weapp, graphAPI


def connectToMicrosoft(connectToMicrosoftBody):
    MICROSOFT_CLIENT_ID: str = os.environ['MICROSOFT_CLIENT_ID']
    MICROSOFT_CLIENT_SECRET: str = os.environ['MICROSOFT_CLIENT_SECRET']
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    connectToMicrosoftBody_dict = connexion.request.get_json()
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401
    try:
        tokenPostBody = {
            "client_id": MICROSOFT_CLIENT_ID,
            "scope": "offline_access openid profile https://graph.microsoft.com/calendars.readwrite https://graph.microsoft.com/user.readwrite",
            "code": connectToMicrosoftBody_dict["code"],
            "redirect_uri": "http://localhost:8000/connectToMicrosoft",  # TODO: 此处redirect_uri应当存入config
            "grant_type": "authorization_code",
            "client_secret": MICROSOFT_CLIENT_SECRET
        }
        tokenResponse = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=tokenPostBody)
        microsoftAccessToken = tokenResponse.json()["access_token"]
        microsoftRefreshToken = tokenResponse.json()["refresh_token"]
        learner.microsoftAccessToken = microsoftAccessToken
        learner.microsoftRefreshToken = microsoftRefreshToken
        me = graphAPI.getMe(microsoftAccessToken)
        learner.microsoftId = me['id']
        learner.microsoftUserPrincipalName = me['userPrincipalName']
        db_session.commit()
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400
    db_session.remove()
    return {"message": "成功写入Microsoft账号相关信息", "microsoftId": me['id']}, 200


def project_cover_post():  # noqa: E501

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    img = connexion.request.files.get('project_cover')
    extension = os.path.splitext(img.filename)[-1]
    uid = create_uuid()
    if not allowed_file(img.filename):
        db_session.remove()
        return {"error": "文件类型错误"}, 403, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    path = os.path.join(os.environ["STORAGEURL"], str(learner.id))
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, uid + extension)
    url = uid + extension
    img.save(file_path)
    db_session.remove()
    return {"url": url}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def project_cover_get(learnerId, uid):  # noqa: E501
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    img_local_path = os.path.join(os.environ["STORAGEURL"], learnerId, uid)
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    db_session.remove()
    return {"projectCover": img_stream.decode("utf-8")}, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def course_cover_post():  # noqa: E501

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    img = connexion.request.files.get('course_cover')
    extension = os.path.splitext(img.filename)[-1]
    uid = create_uuid()
    if not allowed_file(img.filename):
        db_session.remove()
        return {"error": "文件类型错误"}, 403, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    path = os.path.join(os.environ["STORAGEURL"], "courseCover")
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, uid + extension)
    url = uid + extension
    img.save(file_path)
    db_session.remove()
    return {"url": url}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def course_cover_get(coverImageURL):  # noqa: E501
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    img_local_path = os.path.join(os.environ["STORAGEURL"], "courseCover", coverImageURL)
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    db_session.remove()
    return {"courseCover": img_stream.decode("utf-8")}, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def config_get():
    # 获取基本设置。没有加密，切勿放置敏感信息。
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    config = db_session.query(orm.Config_db).all()
    response = []
    for item in config:
        response.append({
            item.name: item.value
        })
    db_session.remove()
    return response, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
