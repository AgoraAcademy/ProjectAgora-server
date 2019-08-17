import connexion
import six
import os
import requests
import json
import pytz
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
tzinfo = pytz.timezone('Asia/Shanghai')


def miniprogram_announcement_post(announcementPostBody):
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    announcementPostBody_dict = connexion.request.get_json()
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    # 自定义鉴权
    if not learner.isAdmin:
        db_session.remove()
        return {'code': -1007, 'message': '需要管理员权限', "detail": "只有管理员有权限发送通知"}, 200
    try:
        newAnnouncement = orm.Announcement_db(
            initiatorId=learner.id,
            initiatorDisplayName=announcementPostBody_dict['initiatorDisplayName'],
            recipients=json.dumps(announcementPostBody_dict['recipients']),
            sentDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            modifiedDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            expireDateTime=util.EWSDateTimeToDateTime(EWSDateTime.from_string(announcementPostBody_dict["expireDateTime"])),
            thumbnail=json.dumps(announcementPostBody_dict['thumbnail']),
            title=announcementPostBody_dict['title'],
            description=announcementPostBody_dict['description'],
            body=json.dumps(announcementPostBody_dict['body']),
            attachment=json.dumps(announcementPostBody_dict['attachment']),
        )
        db_session.add(newAnnouncement)
        db_session.commit()
        newPushMessage = orm.PushMessage_db(
            messageType="Announcement",
            entityId=newAnnouncement.id,
            senderId=learner.id,
            senderDisplayName=announcementPostBody_dict['initiatorDisplayName'],
            recipients=json.dumps(announcementPostBody_dict['recipients']),
            sentDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            modifiedDateTime=util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
            expireDateTime=util.EWSDateTimeToDateTime(EWSDateTime.from_string(announcementPostBody_dict["expireDateTime"])),
            content=json.dumps(announcementPostBody_dict["content"])
        )
        db_session.add(newPushMessage)
        db_session.commit()
        newAnnouncement.pushMessageId = newPushMessage.id
        db_session.commit()
    except Exception as e:
        db_session.remove()
        return {'code': -5001, 'message': '创建通知失败', 'log': str(e)}, 200
    response = {'pushMessage_id': newPushMessage.id, 'announcment_id': newAnnouncement.id}
    return {'code': 0, 'data': response, 'message': '成功'}, 200


def miniprogram_announcement_get():
    # 获取通知列表，目前暂时默认为返回全部条目
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
        announcementList = db_session.query(orm.Announcement_db).all()
        response = []
        for announcement in announcementList:
            response.append({
                "id": announcement.id,
                "pushMessageId": announcement.pushMessageId,
                "initiatorId": announcement.initiatorId,
                "initiatorDisplayName": announcement.initiatorDisplayName,
                "recipients": json.loads(announcement.recipients),
                "sentDateTime": EWSDateTime.from_datetime(tzinfo.localize(announcement.sentDateTime)).ewsformat(),
                "modifiedDateTime": EWSDateTime.from_datetime(tzinfo.localize(announcement.modifiedDateTime)).ewsformat(),
                "expireDateTime": EWSDateTime.from_datetime(tzinfo.localize(announcement.expireDateTime)).ewsformat(),
                "thumbnail": json.loads(announcement.thumbnail),
                "title": announcement.title,
                "description": announcement.description,
                "body": json.loads(announcement.body),
                "attachment": json.loads(announcement.attachment)
            })
        db_session.remove()
    except Exception as e:
        db_session.remove()
        return {'code': -3006, 'message': '获取通知列表失败', 'log': str(e)}, 200
    return {'code': 0, 'data': response, 'message': '成功'}, 200


def miniprogram_announcement_announcementId_patch(announcementId, announcementPatchBody):
    # 修改通知接口
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    announcementPatchBody_dict = connexion.request.get_json()
    learner = weapp.getLearner()
    if not learner:
        db_session.remove()
        return {'code': -1001, 'message': '没有找到对应的Learner'}, 200
    announcement = db_session.query(orm.Announcement_db).filter(orm.Announcement_db.id == announcementId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == announcement.pushMessageId).one_or_none()
    try:
        for itemKey in announcementPatchBody_dict:
            if itemKey == "initiatorDisplayName":
                announcement.initiatorDisplayName = announcementPatchBody_dict[itemKey]
            if itemKey == "recipients":
                announcement.recipients = json.dumps(announcementPatchBody_dict[itemKey])
            if itemKey == "thumbnail":
                announcement.thumbnail = json.dumps(announcementPatchBody_dict[itemKey])
            if itemKey == "content":
                pushMessage.content = json.dumps(announcementPatchBody_dict[itemKey])
            if itemKey == "body":
                announcement.body = json.dumps(announcementPatchBody_dict[itemKey])
            if itemKey == "attachment":
                announcement.attachment = json.dumps(announcementPatchBody_dict[itemKey])
            if itemKey == "title":
                announcement.title = announcementPatchBody_dict[itemKey]
            if itemKey == "description":
                announcement.description = announcementPatchBody_dict[itemKey]
            if itemKey == "expireDateTime":
                newExpireDateTime = util.EWSDateTimeToDateTime(EWSDateTime.from_string(announcementPatchBody_dict[itemKey])),
                setattr(pushMessage, itemKey, newExpireDateTime)
        newModifiedDateTime = util.EWSDateTimeToDateTime(account.default_timezone.localize(EWSDateTime.now())),
        pushMessage.modifiedDateTime = newModifiedDateTime
        db_session.commit()
        db_session.remove()
        return {'code': 0, 'message': '成功'}, 200
    except Exception as e:
        db_session.remove()
        return {'code': -5002, 'message': '更新通知失败', 'log': str(e)}, 200


def miniprogram_announcement_announcementId_get(announcementId):
    # 获取通知的详情
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
    announcement = db_session.query(orm.Announcement_db).filter(orm.Announcement_db.id == announcementId).one_or_none()
    try:
        response = {
            "id": announcement.id,
            "initiatorId": announcement.initiatorId,
            "initiatorDisplayName": announcement.initiatorDisplayName,
            "recipients": json.loads(announcement.recipients),
            "sentDateTime": EWSDateTime.from_datetime(tzinfo.localize(announcement.sentDateTime)).ewsformat(),
            "modifiedDateTime": EWSDateTime.from_datetime(tzinfo.localize(announcement.modifiedDateTime)).ewsformat(),
            "thumbnail": json.loads(announcement.thumbnail),
            "title": announcement.title,
            "description": announcement.description,
            "body": json.loads(announcement.body),
            "attachment": json.loads(announcement.attachment),
        }
        db_session.remove()
        return {'code': 0, 'data': response, 'message': '成功'}, 200
    except Exception as e:
        db_session.remove()
        return {'code': -5003, 'message': '获取通知详情失败', 'log': str(e)}, 200


def miniprogram_announcement_announcementId_delete(announcementId):
    # 根据announcementId删除announcement和相关的pushMessage
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
    announcement = db_session.query(orm.Announcement_db).filter(orm.Announcement_db.id == announcementId).one_or_none()
    pushMessage = db_session.query(orm.PushMessage_db).filter(orm.PushMessage_db.id == announcement.pushMessageId).one_or_none()
    try:
        if announcement.initiatorId == learner.id or learner.isAdmin:
            db_session.delete(announcement)
            if pushMessage:
                db_session.delete(pushMessage)
        else:
            return {'code': -1007, 'message': '需要管理员权限', 'detail': '只有管理员或该活动创建人可以删除该活动'}, 200
        db_session.commit()
        db_session.remove()
        return {'code': 0, 'message': '成功'}, 200
    except Exception as e:
        db_session.remove()
        return {'code': -3005, 'message': '删除通知失败', 'log': str(e)}, 200
