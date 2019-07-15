import connexion
import six

from swagger_server.models.credit_hour_entry import CreditHourEntry  # noqa: E501
from swagger_server import util


def learner_learner_id_credit_hour_get(learnerId):  # noqa: E501
    """返回一个Learner相关的学时记录

     # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[CreditHourEntry]
    """
    return 'do some magic!'
