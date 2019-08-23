import connexion
from flask import make_response
import six
import os
import requests
import datetime
import random
import base64

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util, orm, wxLogin, weapp


def miniprogram_picture_post(pictureType: str):  # noqa: E501

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
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    if pictureType not in ["event", "announcement", "project", "course", "club"]:
        return {'code': -4001, "message": "图片类别不支持"}, 200
    img = connexion.request.files.get('picture')
    extension = os.path.splitext(img.filename)[-1]
    uid = create_uuid()
    if not allowed_file(img.filename):
        db_session.remove()
        return {'code': -4002, 'message': '文件类型不支持'}, 200
    path = os.path.join(os.environ["STORAGEURL"], pictureType)
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        file_path = os.path.join(path, uid + extension)
        url = uid + extension
        img.save(file_path)
    except Exception as e:
        db_session.remove()
        return {'code': -4003, 'message': '文件储存失败', 'log': str(e)}, 200
    db_session.remove()
    return {'code': 0, 'data': {"url": url}, 'message': '成功'}, 200


def miniprogram_picture_get(uid, pictureType):  # noqa: E501
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    if pictureType not in ["event", "announcement", "project", "course", "club"]:
        return {'code': -4001, "message": "图片类别不支持"}, 200
    img_local_path = os.path.join(os.environ["STORAGEURL"], pictureType, uid)
    img_stream = ''
    try:
        with open(img_local_path, 'rb') as img_f:
            img_stream = img_f.read()
            response = make_response(img_stream)
            response.headers['Content-Type'] = 'image'
    except Exception as e:
        db_session.remove()
        return {'code': -4004, 'message': '图片文件读取失败', 'log': str(e)}, 200
    db_session.remove()
    return response, 200
