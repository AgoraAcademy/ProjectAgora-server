import connexion
import six
import os
from tzlocal import get_localzone
from dateutil.relativedelta import relativedelta
from exchangelib import Credentials, Account, Configuration, DELEGATE, RoomList, CalendarItem, EWSDateTime
from exchangelib.services import GetRooms
from exchangelib.items import MeetingRequest, MeetingCancellation, SEND_TO_ALL_AND_SAVE_COPY
from swagger_server import util, wxLogin, orm

db_session = None
db_session = orm.init_db(os.environ["DATABASEURI"])

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


def booking_get():  # noqa: E501
    # 获取所有的房间信息
    db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
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
        return {"error": str(e)}, 400, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    db_session.remove()
    return response, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def booking_roomCode_get(roomCode, monthToLoad):  # noqa: E501
    # 按房间信息和月份（query中）获取所有的预约信息
    db_session = orm.init_db(os.environ["DATABASEURI"])
    responseList = []
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
    try:
        room_account = Account(
            primary_smtp_address=('%s@agoraacademy.cn' % roomCode),
            credentials=credentials,
            config=config
        )
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 400, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
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
        return {"error": str(e)}, 400, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    db_session.remove()
    return responseList, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def booking_roomCode_post(roomCode, appointment):  # noqa: E501
    # 添加预约信息
    db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
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
        return {"error": str(e)}, 400, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    db_session.remove()
    return {'message': 'success'}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def booking_roomCode_delete(roomCode, monthToLoad, deleteInfo):  # noqa: E501
    # 按照月份、changekey、房间号删除预约信息
    db_session = orm.init_db(os.environ["DATABASEURI"])
    validation_result = wxLogin.validateUser()
    changekey = deleteInfo['changekey']
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        db_session.remove()
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    try:
        room_account = Account(
            primary_smtp_address=('%s@agoraacademy.cn' % roomCode),
            credentials=credentials,
            config=config
        )
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 400, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
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
                    item.delete()
    except Exception as e:
        db_session.remove()
        return {"error": str(e)}, 400, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
    db_session.remove()
    return {'message': 'success'}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
