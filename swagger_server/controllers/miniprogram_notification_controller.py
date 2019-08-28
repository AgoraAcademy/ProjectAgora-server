import os
import datetime
import json
import pytz
from typing import List
from exchangelib import EWSDateTime
from swagger_server import util, orm, weapp
from swagger_server.orm import Event_db, Notification_db

tzinfo = pytz.timezone('Asia/Shanghai')


def miniprogram_notification_get(isGetAll: bool = False):
    def constructContent(notification: Notification_db):
        if notification.notificationType == "活动日程":
            event: Event_db = db_session.query(orm.Event_db).filter(orm.Event_db.id == notification.entityId).one_or_none()
            return {
                "startDateTime": json.loads(event.eventInfo)["startDateTime"],
                "endDateTime": json.loads(event.eventInfo)["endDateTime"]
            }
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
    response = []
    if isGetAll:
        notificationList: List[Notification_db] = db_session.query(orm.Notification_db).filter(orm.Notification_db.learnerId == learner.id).all()
    else:
        notificationList = db_session.query(orm.Notification_db).filter(orm.Notification_db.learnerId == learner.id).filter(orm.Notification_db.expireDateTime > datetime.datetime.utcnow()).all()
    for notification in notificationList:
        response.append({
            "notificationType": notification.notificationType,
            "entityId": notification.entityId,
            "createdDateTime": EWSDateTime.from_datetime(tzinfo.localize(notification.createdDateTime)).ewsformat(),
            "expireDateTime": EWSDateTime.from_datetime(tzinfo.localize(notification.expireDateTime)).ewsformat(),
            "status": notification.status,
            "title": notification.title,
            "description": notification.description,
            "content": constructContent(notification)
        })
    db_session.remove()
    return {'code': 0, 'data': response, 'message': '成功'}, 200
