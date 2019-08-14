import connexion
import os
import json
import requests
from swagger_server.models.credit_hour_entry import CreditHourEntry  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.learner import Learner  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server import util, wxLogin, orm


def learner_get():  # noqa: E501
    """返回所有Learner的全部信息

    # noqa: E501
    # 权限限定：mentor限定（未实装）


    :rtype: InlineResponse2001
    """
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
        return {"error": "Failed to validate access token"}, 401
    result_list = []
    query = db_session.query(orm.Learner_db).filter(orm.Learner_db.validated == True).all()
    for learner in query:
        result_list.append({
            "id": learner.id,
            "givenName": learner.givenName,
            "familyName": learner.familyName,
            "isMentor": learner.isMentor
        })
    db_session.remove()
    return result_list, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def learner_head():  # noqa: E501
    """弃用

    # noqa: E501

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def learner_patch(learner):  # noqa: E501
    """更新一个learner

    # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!patch！'


def learner_learner_id_credit_hour_get(learnerId):  # noqa: E501
    """返回一个Learner相关的学时记录

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[CreditHourEntry]
    """
    return 'do some magic!'


def learner_learner_id_get(learnerId):  # noqa: E501
    """返回一个Learner的详细信息

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: Learner
    """
    return 'do some magic!'


def learner_learner_id_project_get(learnerId):  # noqa: E501
    """返回一个Learner相关的课程

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[Project]
    """
    return 'do some magic!'


def learner_post(learner):  # noqa: E501
    """创建一个Learner

    # noqa: E501

    :param learner:
    :type learner: dict | bytes

    :rtype: InlineResponse201
    """
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
        return {"error": "Failed to validate access token"}, 401
    if connexion.request.is_json:
        learner = Learner.from_dict(connexion.request.get_json())  # noqa: E501
        learner_dict = connexion.request.get_json()
    # 获取unionid
    try:
        userInfo = requests.get("https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s" % (validation_result["access_token"], connexion.request.headers['openid']))
        db_session.add(orm.Learner_db(
            validated=False,
            openid=connexion.request.headers['openid'],
            unionid=userInfo.json()['unionid'],
            sessionKey='0',
            openidWeApp='0',
            isAdmin=False,
            status=learner.status,
            isMentor=learner.is_mentor,
            givenName=learner.given_name,
            familyName=learner.family_name,
            nickname=learner.nickname,
            gender=learner.gender,
            ethnicity=learner.ethnicity,
            birthday=learner.birthday,
            mainPersonalIdType=learner.main_personal_id_type,
            mainPersonalId=learner.main_personal_id,
            dateOfRegistration=learner.date_of_registration,
            reasonOfRegistration=learner.reason_of_registration,
            previousStatus=learner.previous_status,
            custodianInfo=json.dumps(learner_dict["custodianInfo"]),
            emergentContact=json.dumps(learner_dict["emergentContact"]),
            contactInfo=json.dumps(learner_dict["contactInfo"]),
            medicalInfo=json.dumps(learner_dict["medicalInfo"]),
            notes=json.dumps(learner_dict["notes"]),
        ))
        db_session.commit()
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 401, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    db_session.remove()
    return {}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
