import connexion
import six
import os

from swagger_server.models.credit_hour_entry import CreditHourEntry  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.learner import Learner  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server import util


def learner_get():  # noqa: E501
    headers = connexion.request.headers
    try:
        access_token = headers['Authorization']
        refresh_token = headers['refresh_token']
    except Exception as e:
        return {"error": e}
    
    
    return 'do some magic!'


def learner_head():  # noqa: E501
    """返回所有Learner的关键信息

    # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'


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


def learner_post(login):  # noqa: E501
    """创建一个Learner

    # noqa: E501

    :param login: 
    :type login: dict | bytes

    :rtype: InlineResponse201
    """
    if connexion.request.is_json:
        login = Learner.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
