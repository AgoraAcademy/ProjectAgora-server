import connexion
import six
import os
import datetime
import json

from swagger_server.models.project import Project  # noqa: E501
from swagger_server import util, wxLogin, orm


def project_get():  # noqa: E501
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
        return {"error": "Failed to validate access token"}, 401
    result_list = []
    query = db_session.query(orm.Project_db).all()
    for project in query:
        result_list.append({
            "id": project.id,
            "name": project.name,
            "createdTime": project.createdTime,
            "createdBy": project.createdBy,
            "createdByID": project.createdByID,
            "relatedCourse": project.relatedCourse,
            "projectMentorID": project.projectMentorID,
            "projectMentor": project.projectMentor,
            "status": project.status,
            "coverImageURL": project.coverImageURL
        })
    db_session.remove()
    return result_list, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


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
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401
    if connexion.request.is_json:
        project = Project.from_dict(connexion.request.get_json())
    project_dict = connexion.request.get_json()
    try:
        db_session.add(orm.Project_db(
            name=project.name,
            status="未提交",
            createdTime=datetime.date.today().strftime('%Y-%m-%d'),
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
            projectMeta=json.dumps(project_dict["projectMeta"]),
            projectApprovalInfo=json.dumps(project_dict["projectApprovalInfo"]),
            conclusionInfo=json.dumps(project_dict["conclusionInfo"]),
            content='[]',
            coverImageURL=project_dict["coverImageURL"]
        ))
        db_session.commit()
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 401
    db_session.remove()
    return {}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def project_project_id_get(projectId):  # noqa: E501
    """返回一个Project的详细信息

    # noqa: E501

    :param projectId:
    :type projectId: int

    :rtype: Learner
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
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401
    project = db_session.query(orm.Project_db).filter(orm.Project_db.id == projectId).one_or_none()
    projectInfo = {
        "id": project.id,
        "name": project.name,
        "status": project.status,
        "createdTime": project.createdTime,
        "createdByID": project.createdByID,
        "createdBy": project.createdBy,
        "relatedCourseId": project.relatedCourseId,
        "relatedCourse": project.relatedCourse,
        "projectTerm": project.projectTerm,
        "projectTermLength": project.projectTermLength,
        "projectStartDate": project.projectStartDate,
        "averageIntendedCreditHourPerWeek": project.averageIntendedCreditHourPerWeek,
        "totalIntendedCreditHour": project.totalIntendedCreditHour,
        "projectMentorID": project.projectMentorID,
        "projectMentor": project.projectMentor,
        "averageGuidingHourPerWeek": project.averageGuidingHourPerWeek,
        "projectMeta": json.loads(project.projectMeta),
        "projectApprovalInfo": json.loads(project.projectApprovalInfo),
        "content": json.loads(project.content),
        "conclusionInfo": json.loads(project.conclusionInfo),
        "lastUpdatedTime": project.lastUpdatedTime,
        "coverImageURL": project.coverImageURL
    }
    db_session.remove()
    return projectInfo, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def project_project_id_patch(projectId):  # noqa: E501
    """返回一个Project的详细信息

    # noqa: E501

    :param projectId:
    :type projectId: int

    :rtype: Learner
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
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401
    project = db_session.query(orm.Project_db).filter(orm.Project_db.id == projectId).one_or_none()
    if connexion.request.is_json:
        patch = Project.from_dict(connexion.request.get_json())
    patchDict = {
        "name": patch.name,
        "status": patch.status,
        "projectTerm": patch.project_term,
        "projectTermLength": patch.project_term_length,
        "projectStartDate": patch.project_start_date,
        "averageIntendedCreditHourPerWeek": patch.average_intended_credit_hour_per_week,
        "totalIntendedCreditHour": patch.total_intended_credit_hour,
        "projectMentorID": patch.project_mentor_id,
        "projectMentor": patch.project_mentor,
        "averageGuidingHourPerWeek": patch.average_guiding_hour_per_week,
        "projectMeta": json.dumps(connexion.request.get_json()["projectMeta"] if patch.project_meta is not None else None),
        "projectApprovalInfo": json.dumps(connexion.request.get_json()["projectApprovalInfo"] if patch.project_approval_info is not None else None),
        "content": json.dumps(connexion.request.get_json()["content"] if patch.content is not None else None),
        "conclusionInfo": json.dumps(connexion.request.get_json()["conclusionInfo"] if patch.conclusion_info is not None else None),
        "coverImageURL": connexion.request.get_json().get("coverImageURL", ""),
    }
    patchDict = {k: v for k, v in patchDict.items() if v is not None}
    # patchMapper = {
    #     "name": project.name,
    #     "status": project.status,
    #     "projectTerm": project.projectTerm,
    #     "projectTermLength": project.projectTermLength,
    #     "projectStartDate": project.projectStartDate,
    #     "averageIntendedCreditHourPerWeek": project.averageIntendedCreditHourPerWeek,
    #     "totalIntendedCreditHour": project.totalIntendedCreditHour,
    #     "projectMentorID": project.projectMentorID,
    #     "projectMentor": project.projectMentor,
    #     "averageGuidingHourPerWeek": project.averageGuidingHourPerWeek,
    #     "projectMeta": project.projectMeta,
    #     "projectApprovalInfo": project.projectApprovalInfo,
    #     "content": project.content,
    #     "conclusionInfo": project.conclusionInfo,
    #     "lastUpdatedTime": project.lastUpdatedTime,
    # }
    try:
        for item, value in patchDict.items():
            setattr(project, item, value)
        db_session.commit()
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 401
    db_session.remove()
    return {}, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
