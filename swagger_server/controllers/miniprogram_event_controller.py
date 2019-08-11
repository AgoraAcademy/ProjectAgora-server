import connexion
import six
import os
import requests
import json
from tzlocal import get_localzone
from flask import Flask, send_from_directory
from exchangelib import Credentials, Account, Configuration, DELEGATE, RoomList, CalendarItem, EWSDateTime
from exchangelib.services import GetRooms
from exchangelib.items import MeetingRequest, MeetingCancellation, SEND_TO_ALL_AND_SAVE_COPY

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util, orm, weapp

credentials = Credentials(
    os.environ["EWS_admin_email"],
    os.environ["EWS_admin_password"])

config = Configuration(server='outlook.office365.com', credentials=credentials)

account = Account(
    primary_smtp_address='admin@agoraacademy.cn',
    credentials=credentials,
    autodiscover=False,
    config=config,
    access_type=DELEGATE
)


def miniprogram_event_post(eventPostBody):
    # 创建活动接口
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    eventPostBody_dict = connexion.request.get_json()
    sessionKey = connexion.request.headers['token']
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    if not learner:
        db_session.remove()
        return {"message": "learner not found"}, 401
    # 自定义鉴权
    if not learner.isAdmin:
        if "initiatorDisplayName" in eventPostBody:
            db_session.remove()
            return {"message": "非管理员不可自定义发起者名称"}, 403
        initiatorDisplayName = learner.familyName + learner.givenName
    else:
        initiatorDisplayName = eventPostBody_dict["initiatorDisplayName"] if "initiatorDisplayName" in eventPostBody_dict else learner.familyName + learner.givenName
    try:
        newEvent = orm.Event_db(
            initiatorId=learner.id,
            initiatorDisplayName=initiatorDisplayName,
            eventInfo=eventPostBody_dict["eventInfo"],
            invitee=eventPostBody_dict["invitee"],
            thumbnail=eventPostBody_dict["thumbnail"]
        )
        db_session.add(newEvent)
        db_session.commit()
        newPushMessage = orm.PushMessage_db(
            messageType="Event",
            entityId=newEvent.id,
            senderId=learner.id,
            senderDisplayName=initiatorDisplayName,
            recipients=eventPostBody_dict["invitee"],
            rsvp={"accept": [], "decline": [], "tentative": []},
            sentDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            modifiedDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            expireDateTime=util.EWSDateTimeToDateTime(EWSDateTime.from_string(eventPostBody_dict["eventInfo"]["expireDateTime"])),
            content=eventPostBody_dict["content"]
        )
        db_session.add(newPushMessage)
        db_session.commit()
        newEvent.pushMessageId = newPushMessage.id
        db_session.commit()
        # TODO: 这里应当添加Microsoft Graph API为initiator添加appointment并发送至recipients
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400
    response = {"pushMessage_id": newPushMessage.id, "event_id": newEvent.id}
    db_session.remove()
    return response, 201


def miniprogram_event_patch(eventId):
    # 修改活动接口，包括报名的部分
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    eventPatchBody_dict = connexion.request.get_json()
    sessionKey = connexion.request.headers['token']
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    if not learner:
        db_session.remove()
        return {"message": "learner not found"}, 401
    event = db_session.query(orm.Event_db).filter(orm.Event_db.id == eventId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == event.pushMessageId).one_or_none()
    try:
        if event.initiatorId != learner.id:
            try:
                newRsvp = json.loads(pushMessage.rsvp) if pushMessage.rsvp else {'accept': [], 'decline': [], 'tentative': []}
                if eventPatchBody_dict["rsvp"] == "参加":
                    newRsvp["accept"].append(learner.id)
                    newRsvp["accept"] = list(set(newRsvp["accept"]))
                    for responseType in ["decline", "tentative"]:
                        if learner.id in newRsvp[responseType]:
                            newRsvp[responseType].remove(learner.id)
                if eventPatchBody_dict["rsvp"] == "拒绝":
                    newRsvp["decline"].append(learner.id)
                    newRsvp = list(set(newRsvp))
                    for responseType in ["accept", "tentative"]:
                        if learner.id in newRsvp[responseType]:
                            newRsvp[responseType].remove(learner.id)
                if eventPatchBody_dict["rsvp"] == "可能参加":
                    newRsvp["tentative"].append(learner.id)
                    newRsvp = list(set(newRsvp))
                    for responseType in ["decline", "accept"]:
                        if learner.id in newRsvp[responseType]:
                            newRsvp[responseType].remove(learner.id)
                setattr(pushMessage, "rsvp", json.dumps(newRsvp))
                db_session.commit()
            except Exception as e:
                db_session.remove()
                return {'error': str(e)}, 400
            db_session.remove()
            return {"message": "event rsvp updated"}, 200
        else:
            for itemKey in eventPatchBody_dict:
                if itemKey == "initiatorDisplayName":
                    event.initiatorDisplayName = eventPatchBody_dict[itemKey]
                if itemKey == "invitee":
                    event.invitee = eventPatchBody_dict[itemKey]
                if itemKey == "thumbnail":
                    event.thumbnail = eventPatchBody_dict[itemKey]
                if itemKey == "content":
                    pushMessage.content = eventPatchBody_dict[itemKey]
                if itemKey in ["title", "description", "fee", "location"]:
                    newEventInfo = event.eventInfo
                    newEventInfo[itemKey] = eventPatchBody_dict[itemKey]
                    event.eventInfo = newEventInfo
                if itemKey in ["expireDateTime", "endDateTime", "startDateTime"]:
                    newEventInfo = event.eventInfo
                    newEventInfo[itemKey] = eventPatchBody_dict[itemKey]
                    event.eventInfo = newEventInfo
                    newPatchDateTime = util.EWSDateTimeToDateTime(EWSDateTime.from_string(eventPatchBody_dict[itemKey])),
                    setattr(pushMessage, itemKey, newPatchDateTime)
            newModifiedDateTime = util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            pushMessage.modifiedDateTime = newModifiedDateTime
            db_session.commit()
            db_session.remove()
            return {"message": "event updated"}, 200
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400


def miniprogram_event_eventId_get(eventId):
    # 获取活动的详情以及相关的rsvp详情
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    sessionKey = connexion.request.headers['token']
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    if not learner:
        db_session.remove()
        return {"message": "learner not found"}, 401
    event = db_session.query(orm.Event_db).filter(orm.Event_db.id == eventId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == event.pushMessageId).one_or_none()
    try:
        response = {
            "id": event.id,
            "initiatorId": event.initiatorId,
            "initiatorDisplayName": event.initiatorDisplayName,
            "eventInfo": event.eventInfo,
            "invitee": event.invitee,
            "thumbnail": event.thumbnail,
            "rsvp": pushMessage.rsvp
        }
        db_session.remove()
        return response, 200
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400


def miniprogram_event_eventId_delete(eventId):
    # 根据eventId删除event和相关的pushMessage
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    sessionKey = connexion.request.headers['token']
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    if not learner:
        db_session.remove()
        return {"message": "learner not found"}, 401
    event = db_session.query(orm.Event_db).filter(orm.Event_db.id == eventId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == event.pushMessageId).one_or_none()
    try:
        if event.initiatorId == learner.id or learner.isAdmin:
            pushMessage.delete()
            event.delete()
        db_session.commit()
        db_session.remove()
        return {"message": "successfully deleted"}, 204
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400


def miniprogram_event_get():
    # 获取活动列表，目前暂时默认为返回全部条目
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    sessionKey = connexion.request.headers['token']
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    if not learner:
        db_session.remove()
        return {"message": "learner not found"}, 401
    try:
        eventList = db_session.query(orm.Event_db).all()
        response = []
        for event in eventList:
            response.append({
                "id": event.id,
                "initiatorId": event.initiatorId,
                "initiatorDisplayName": event.initiatorDisplayName,
                "eventInfo": event.eventInfo,
                "invitee": event.invitee
            })
        db_session.remove()
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400
    return response, 200
