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
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    # 自定义鉴权
    if not learner.isAdmin:
        if "initiatorDisplayName" in eventPostBody:
            db_session.remove()
            return {'code': -1007, 'message': '需要管理员权限', "detail": "非管理员不可自定义发起者名称"}, 200
        initiatorDisplayName = learner.familyName + learner.givenName
    else:
        initiatorDisplayName = eventPostBody_dict["initiatorDisplayName"] if "initiatorDisplayName" in eventPostBody_dict else learner.familyName + learner.givenName
    try:
        newEvent = orm.Event_db(
            initiatorId=learner.id,
            initiatorDisplayName=initiatorDisplayName,
            eventInfo=json.dumps(eventPostBody_dict["eventInfo"]),
            invitee=json.dumps(eventPostBody_dict["invitee"]),
            thumbnail=json.dumps(eventPostBody_dict["thumbnail"])
        )
        db_session.add(newEvent)
        db_session.commit()
        newPushMessage = orm.PushMessage_db(
            messageType="Event",
            entityId=newEvent.id,
            senderId=learner.id,
            senderDisplayName=initiatorDisplayName,
            recipients=json.dumps(eventPostBody_dict["invitee"]),
            rsvp=json.dumps({"accept": [], "decline": [], "tentative": []}),
            sentDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            modifiedDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            expireDateTime=util.EWSDateTimeToDateTime(EWSDateTime.from_string(eventPostBody_dict["eventInfo"]["expireDateTime"])),
            content=json.dumps(eventPostBody_dict["content"])
        )
        db_session.add(newPushMessage)
        db_session.commit()
        newEvent.pushMessageId = newPushMessage.id
        db_session.commit()
        # TODO: 这里应当添加Microsoft Graph API为initiator添加appointment并发送至recipients
    except Exception as e:
        db_session.remove()
        return {'code': -3001, 'message': '活动创建失败', 'log': str(e)}, 200
    response = {"pushMessageId": newPushMessage.id, "id": newEvent.id}
    db_session.remove()
    return {'code': 0, 'data': response, 'message': '成功'}, 201


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
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    event = db_session.query(orm.Event_db).filter(orm.Event_db.id == eventId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == event.pushMessageId).one_or_none()
    if event.initiatorId != learner.id:
        try:
            newRsvp = json.loads(pushMessage.rsvp) if pushMessage.rsvp else {'accept': [], 'decline': [], 'tentative': []}
            newEntry = {'id': learner.id, 'fullname': learner.familyName + learner.givenName}
            if eventPatchBody_dict["rsvp"] == "参加":
                if newEntry not in newRsvp['accept']:
                    newRsvp["accept"].append(newEntry)
                for responseType in ["decline", "tentative"]:
                    if newEntry in newRsvp[responseType]:
                        newRsvp[responseType].remove(newEntry)
            if eventPatchBody_dict["rsvp"] == "拒绝":
                if newEntry not in newRsvp['decline']:
                    newRsvp["decline"].append(newEntry)
                for responseType in ["accept", "tentative"]:
                    if newEntry in newRsvp[responseType]:
                        newRsvp[responseType].remove(newEntry)
            if eventPatchBody_dict["rsvp"] == "可能参加":
                if newEntry not in newRsvp['tentative']:
                    newRsvp["tentative"].append(newEntry)
                for responseType in ["decline", "accept"]:
                    if newEntry in newRsvp[responseType]:
                        newRsvp[responseType].remove(newEntry)
            setattr(pushMessage, "rsvp", json.dumps(newRsvp))
            db_session.commit()
        except Exception as e:
            db_session.remove()
            return {'code': -3002, 'message': '更新rsvp信息失败', 'log': str(e)}, 200
        db_session.remove()
        return {'code': 0, 'message': '成功更新rsvp信息'}, 200
    else:
        try:
            for itemKey in eventPatchBody_dict:
                if itemKey == "initiatorDisplayName":
                    event.initiatorDisplayName = eventPatchBody_dict[itemKey]
                if itemKey == "invitee":
                    event.invitee = json.dumps(eventPatchBody_dict[itemKey])
                if itemKey == "thumbnail":
                    event.thumbnail = json.dumps(eventPatchBody_dict[itemKey])
                if itemKey == "content":
                    pushMessage.content = json.dumps(eventPatchBody_dict[itemKey])
                if itemKey in ["title", "description", "fee", "location"]:
                    newEventInfo = json.loads(event.eventInfo)
                    newEventInfo[itemKey] = eventPatchBody_dict[itemKey]
                    event.eventInfo = json.dumps(newEventInfo)
                if itemKey in ["expireDateTime", "endDateTime", "startDateTime"]:
                    newEventInfo = json.loads(event.eventInfo)
                    newEventInfo[itemKey] = eventPatchBody_dict[itemKey]
                    event.eventInfo = json.dumps(newEventInfo)
                    newPatchDateTime = util.EWSDateTimeToDateTime(EWSDateTime.from_string(eventPatchBody_dict[itemKey])),
                    setattr(pushMessage, itemKey, newPatchDateTime)
            newModifiedDateTime = util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            pushMessage.modifiedDateTime = newModifiedDateTime
            db_session.commit()
            db_session.remove()
            return {'code': 0, 'message': '成功'}, 200
        except Exception as e:
            db_session.remove()
            return {'code': -3003, 'message': '更新活动失败', 'log': str(e)}, 200


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
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    event = db_session.query(orm.Event_db).filter(orm.Event_db.id == eventId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == event.pushMessageId).one_or_none()
    try:
        response = {
            "id": event.id,
            "initiatorId": event.initiatorId,
            "initiatorDisplayName": event.initiatorDisplayName,
            "eventInfo": json.loads(event.eventInfo),
            "invitee": json.loads(event.invitee),
            "thumbnail": json.loads(event.thumbnail),
            "rsvp": json.loads(pushMessage.rsvp)
        }
        db_session.remove()
        return {'code': 0, 'data': response, 'message': '成功'}, 200
    except Exception as e:
        db_session.remove()
        return {'code': -3004, 'message': '获取活动详情失败', 'log': str(e)}, 200


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
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    event = db_session.query(orm.Event_db).filter(orm.Event_db.id == eventId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == event.pushMessageId).one_or_none()
    try:
        if event.initiatorId == learner.id or learner.isAdmin:
            db_session.delete(event)
            db_session.commit()
            if pushMessage:
                db_session.delete(pushMessage)
        else:
            return {'code': -1007, 'message': '需要管理员权限', 'detail': '只有管理员或该活动创建人可以删除该活动'}, 200
        db_session.commit()
        db_session.remove()
        return {'code': 0, 'message': '成功'}, 200
    except Exception as e:
        db_session.remove()
        return {'code': -3005, 'message': '删除活动失败', 'log': str(e)}, 200


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
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    try:
        eventList = db_session.query(orm.Event_db).all()
        response = []
        for event in eventList:
            response.append({
                "id": event.id,
                "pushMessageId": event.pushMessageId,
                "initiatorId": event.initiatorId,
                "initiatorDisplayName": event.initiatorDisplayName,
                "eventInfo": json.loads(event.eventInfo),
                "invitee": json.loads(event.invitee),
                "thumbnail": json.loads(event.thumbnail)
            })
        db_session.remove()
    except Exception as e:
        db_session.remove()
        return {'code': -3006, 'message': '获取活动列表失败', 'log': str(e)}, 200
    return {'code': 0, 'data': response, 'message': '成功'}, 200
