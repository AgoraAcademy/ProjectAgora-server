import connexion
import six
import os

from swagger_server.models.course import Course  # noqa: E501
from swagger_server import util, wxLogin, orm

db_session = None
if "DEVMODE" in os.environ:
    if os.environ["DEVMODE"] == "True":
        db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
else:
    db_session = orm.init_db(os.environ["DATABASEURI"])


def course_get():  # noqa: E501
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    """返回所有Course

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[Course]
    """
    return 'do some magic!'


def course_head():  # noqa: E501
    """返回所有Course的关键信息

    # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def course_patch(learner):  # noqa: E501
    """更新一个Course

    # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def course_post(course):  # noqa: E501
    """创建一个Learner

    # noqa: E501

    :param learner:
    :type learner: dict | bytes

    :rtype: InlineResponse201
    """
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    if connexion.request.is_json:
        course = Course.from_dict(connexion.request.get_json())
    return {}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
