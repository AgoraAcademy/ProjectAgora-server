import connexion
import six
import os
import datetime

from swagger_server.models.project import Project  # noqa: E501
from swagger_server import util, wxLogin, orm

db_session = None
db_session = orm.init_db(os.environ["DATABASEURI"])


def project_get():  # noqa: E501
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    """返回所有Project

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[Project]
    """
    return 'do some magic!'


def project_head():  # noqa: E501
    """返回所有Project的关键信息

    # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def project_patch(learner):  # noqa: E501
    """更新一个Project

    # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def project_post(project):  # noqa: E501
    """创建一个Learner

    # noqa: E501

    :param learner:
    :type learner: dict | bytes

    :rtype: InlineResponse201
    """
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        return {"error": "Learner not validated"}, 401
    if connexion.request.is_json:
        project = Project.from_dict(connexion.request.get_json())
    try:
        db_session.add(orm.Project_db(
            name=project.name,
            status="审核中",
            createdTime=str(datetime.date.today()),
            createdByID=learner.id,
            createdBy=learner.familyName + learner.givenName,
            relatedCourseId=project.related_course_id,
            relatedCourse=project.related_course,
            projectTerm=project.project_term,
            projectTermLength=project.project_term_length,
            projectStartDate=project.project_start_date,
            averageIntendedCreditHourPerWeek=project.average_intended_credit_hour_per_week,
            totalIntendedCreditHour=project.total_intended_credit_hour,
            projectMentorID=project.project_mentor_id,
            projectMentor=project.project_mentor,
            averageGuidingHourPerWeek=project.average_guiding_hour_per_week,
            projectMeta=project.project_meta,
            projectApprovalInfo=project.project_approval_info,
            conclusionInfo=project.conclusion_info
        ))
        db_session.commit()
    except Exception as e:
        print(e)
        return {"error": "Failed to create new project"}, 401
    return {}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
