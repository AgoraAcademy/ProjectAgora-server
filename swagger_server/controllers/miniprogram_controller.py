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


def miniprogram_login_get(js_code):
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    MINIPROGRAM_APPID: str = os.environ['MINIPROGRAM_APPID']
    MINIPROGRAM_APPSECRET: str = os.environ['MINIPROGRAM_APPSECRET']
    try:
        result = requests.get("https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (MINIPROGRAM_APPID, MINIPROGRAM_APPSECRET, js_code))
        resultjson = result.json()
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openidWeApp == resultjson['openid']).one_or_none()
    try:
        learner.sessionKey = resultjson['session_key']
        db_session.commit()
    except Exception:
        db_session.remove()
    response = {'token': resultjson['session_key'], 'unionid': learner.unionid if learner else '', 'learnerFullName': learner.familyName + learner.givenName if learner else '', "isAdmin": learner.isAdmin if learner else '', "learnerId": learner.id if learner else ''}
    db_session.remove()
    return response, 200


def miniprogram_login_post(loginPostBody):
    # 处理授权用于获取unionid，openid，sessionKey并记入数据库内
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    MINIPROGRAM_APPID: str = os.environ['MINIPROGRAM_APPID']
    loginPostBody_dict = connexion.request.get_json()
    sessionKey = connexion.request.headers['token']
    try:
        decrypter = weapp.WXBizDataCrypt(MINIPROGRAM_APPID, sessionKey)
        decryptedData = decrypter.decrypt(loginPostBody_dict['encryptedData'], loginPostBody_dict['iv'])
        unionid = decryptedData['unionId']
    except Exception as e:
        print(e)
        db_session.remove()
        return {"error": str(e)}, 403
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.unionid == unionid).one_or_none()
    if not learner:
        db_session.remove()
        return {"message": "unionid not found"}, 401
    try:
        learner.openidWeApp = decryptedData['openId']
        learner.sessionKey = sessionKey
    except Exception as e:
        print(e)
        db_session.remove()
        return {"error": str(e)}, 403
    db_session.commit()
    response = {"unionid": unionid, "learnerFullName": learner.familyName + learner.givenName, "isAdmin": learner.isAdmin}
    db_session.remove()
    return response, 200


def miniprogram_learner_post(learnerPostBody):
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    MINIPROGRAM_APPID: str = os.environ['MINIPROGRAM_APPID']
    learnerPostBody_dict = connexion.request.get_json()
    sessionKey = connexion.request.headers['token']
    try:
        decrypter = weapp.WXBizDataCrypt(MINIPROGRAM_APPID, sessionKey)
        decryptedData = decrypter.decrypt(learnerPostBody_dict['encryptedData'], learnerPostBody_dict['iv'])
        unionid = decryptedData['unionId']
    except Exception as e:
        print(e)
        db_session.remove()
        return {"error": str(e)}, 403
    try:
        learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.unionid == unionid).one_or_none()
        if learner:
            db_session.remove()
            return {"error": "用户已存在注册记录"}, 403
    except Exception as e:
        print(e)
        db_session.remove()
        return {"error": str(e)}, 403
    try:
        db_session.add(orm.Learner_db(
            validated=False,
            branch=learnerPostBody_dict['branch'],
            openid="",
            unionid=unionid,
            sessionKey=sessionKey,
            openidWeApp=decryptedData['openId'],
            isAdmin=False,
            status="",
            role=learnerPostBody_dict['role'],
            isMentor=learnerPostBody_dict['isMentor'],
            givenName=learnerPostBody_dict['givenName'],
            familyName=learnerPostBody_dict['familyName'],
            gender="",
            ethnicity="",
            birthday=learnerPostBody_dict['birthday'],
            mainPersonalIdType="",
            mainPersonalId="",
            dateOfRegistration="",
            reasonOfRegistration="",
            previousStatus="",
            emergentContact="[]",
            contactInfo="[]",
            medicalInfo="[]",
        ))
        db_session.commit()
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 401
    response = {"unionid": unionid}
    db_session.remove()
    return response, 201


def miniprogram_ping():
    return {'message': 'pinged!'}, 200


def miniprogram_booking_get():
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    if not weapp.getLearner():
        db_session.remove()
        return {"message": "unionid not found"}, 401
    response = []
    roomLists = db_session.query(orm.Config_db).filter(orm.Config_db.name == 'roomLists').one_or_none().value
    roomDescriptions = db_session.query(orm.Config_db).filter(orm.Config_db.name == 'roomDescriptions').one_or_none().value
    try:
        for roomList in roomLists:
            roomsEWS = GetRooms(protocol=account.protocol).call(
                roomlist=RoomList(
                    email_address=roomList['email'])
            )
            rooms = []
            for room in roomsEWS:
                roomCode = room.email_address.split("@")[0]
                rooms.append({
                    'name': room.name,
                    'roomCode': roomCode,
                    'email': room.email_address,
                    'description': roomDescriptions.get(roomCode, "")
                })
            entry = {
                'listname': roomList['name'],
                'rooms': rooms
            }
            response.append(entry)
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 400
    db_session.remove()
    return response, 200


def miniprogram_booking_roomCode_get(roomCode, monthToLoad):  # noqa: E501
    # 按房间信息和月份（query中）获取所有的预约信息
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    responseList = []
    if not weapp.getLearner():
        db_session.remove()
        return {"message": "unionid not found"}, 401
    try:
        room_account = Account(
            primary_smtp_address=('%s@agoraacademy.cn' % roomCode),
            credentials=credentials,
            config=config
        )
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 400
    monthToLoad_year = int(monthToLoad.split("-")[0])
    monthToLoad_month = int(monthToLoad.split("-")[1])
    if monthToLoad_month == 1:
        start = room_account.default_timezone.localize(EWSDateTime(monthToLoad_year - 1, 12, 1))
    else:
        start = room_account.default_timezone.localize(EWSDateTime(monthToLoad_year, monthToLoad_month - 1, 1))
    if monthToLoad_month == 11:
        end = room_account.default_timezone.localize(EWSDateTime(monthToLoad_year + 1, 1, 1))
    elif monthToLoad_month == 12:
        end = room_account.default_timezone.localize(EWSDateTime(monthToLoad_year + 1, 2, 1))
    else:
        end = room_account.default_timezone.localize(EWSDateTime(monthToLoad_year, monthToLoad_month + 2, 1))
    try:
        for item in room_account.calendar.view(start=start, end=end).all().order_by('start'):
            notes = db_session.query(orm.BookingNotes_db).filter(orm.BookingNotes_db.changekey == item.changekey).one_or_none()
            localizedStart = item.start.astimezone(get_localzone())
            localizedEnd = item.end.astimezone(get_localzone())
            bookedByID = getattr(notes, "bookedByID", 0)
            bookedByName = getattr(notes, "bookedByName", "")
            responseList.append({
                'startDate': ("%d-%0*d-%0*d" % (localizedStart.year, 2, localizedStart.month, 2, localizedStart.day)),
                'endDate': ("%d-%0*d-%0*d" % (localizedEnd.year, 2, localizedEnd.month, 2, localizedEnd.day)),
                'startTime': ("%0*d:%0*d" % (2, localizedStart.hour, 2, localizedStart.minute)),
                'endTime': ("%0*d:%0*d" % (2, localizedEnd.hour, 2, localizedEnd.minute)),
                'subject': item.subject,
                'changekey': item.changekey,
                'bookedByID': bookedByID,
                'bookedByName': bookedByName,
                'description': '' if not getattr(item, 'text_body') else getattr(item, 'text_body'),
                'type': 'appointment'
            })
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400
    db_session.remove()
    return responseList, 200


def miniprogram_booking_roomCode_post(roomCode, appointment):  # noqa: E501
    # 添加预约信息
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    if not weapp.getLearner():
        db_session.remove()
        return {"message": "unionid not found"}, 401
    sessionKey = connexion.request.headers['token']
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    if not learner.validated:
        db_session.remove()
        return {"error": "Learner not validated"}, 401
    room_account = Account(
        primary_smtp_address=('%s@agoraacademy.cn' % roomCode),
        credentials=credentials,
        config=config
    )
    startDateTime = room_account.default_timezone.localize(EWSDateTime(
        appointment['startYear'],
        appointment['startMonth'],
        appointment['startDay'],
        appointment['startHour'],
        appointment['startMinute']
    ))
    endDateTime = room_account.default_timezone.localize(EWSDateTime(
        appointment['endYear'],
        appointment['endMonth'],
        appointment['endDay'],
        appointment['endHour'],
        appointment['endMinute']
    ))
    try:
        item = CalendarItem(
            account=room_account,
            folder=room_account.calendar,
            start=startDateTime,
            end=endDateTime,
            subject=appointment['subject'],
            body=appointment['description'],
        )
        item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)
        db_session.add(orm.BookingNotes_db(
            changekey=item.changekey,
            bookedByID=learner.id,
            bookedByName=learner.familyName + learner.givenName
        ))
        db_session.commit()
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400
    db_session.remove()
    return {'message': 'success'}, 201


def miniprogram_booking_roomCode_delete(roomCode, monthToLoad, deleteInfo):  # noqa: E501
    # 按照月份、changekey、房间号删除预约信息
    db_session = None
    if "DEVMODE" in os.environ:
        if os.environ["DEVMODE"] == "True":
            db_session = orm.init_db(os.environ["DEV_DATABASEURI"])
        else:
            db_session = orm.init_db(os.environ["DATABASEURI"])
    else:
        db_session = orm.init_db(os.environ["DATABASEURI"])
    if not weapp.getLearner():
        db_session.remove()
        return {"message": "unionid not found"}, 401
    changekey = deleteInfo['changekey']
    sessionKey = connexion.request.headers['token']
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.sessionKey == sessionKey).one_or_none()
    try:
        room_account = Account(
            primary_smtp_address=('%s@agoraacademy.cn' % roomCode),
            credentials=credentials,
            config=config
        )
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400
    start_year = int(monthToLoad.split("-")[0])
    start_month = int(monthToLoad.split("-")[1])
    start = room_account.default_timezone.localize(EWSDateTime(start_year, start_month, 1))
    if start_month == 12:
        end = room_account.default_timezone.localize(EWSDateTime(start_year + 1, 1, 1))
    else:
        end = room_account.default_timezone.localize(EWSDateTime(start_year, start_month + 1, 1))
    try:
        for item in room_account.calendar.filter(start__range=(start, end)).all().order_by('start'):
            if item.changekey == changekey:
                notes = db_session.query(orm.BookingNotes_db).filter(orm.BookingNotes_db.changekey == item.changekey).one_or_none()
                if notes.bookedByID == learner.id:
                    db_session.delete(notes)
    except Exception as e:
        db_session.remove()
        return {'error': str(e)}, 400
    db_session.remove()
    return {'message': 'success'}, 201


def miniprogram_pushMessage_get():
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
        return {"message": "unionid not found"}, 401
    response = []
    pushMessageList = db_session.query(orm.PushMessage_db).all()
    for pushMessage in pushMessageList:
        if util.isRecipient(learner, pushMessage.recipients):
            response.append({
                "id": pushMessage.id,
                "messageType": pushMessage.messageType,
                "entityId": pushMessage.entityId,
                "senderId": pushMessage.senderId,
                "recipients": json.dumps(pushMessage.recipients),
                "rsvp": json.dumps(pushMessage.rsvp),
                "sentDateTime": EWSDateTime.from_datetime(pushMessage.sentDateTime).ewsformat(),
                "modifiedDateTime": EWSDateTime.from_datetime(pushMessage.modifiedDateTime).ewsformat(),
                "expireDateTime": EWSDateTime.from_datetime(pushMessage.expireDateTime).ewsformat(),
                "content": json.dumps(pushMessage.content)
            })
    db_session.remove()
    return response, 200
