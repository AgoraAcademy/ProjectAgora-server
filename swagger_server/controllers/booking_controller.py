import connexion
import six
import os
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
        return e
    return response, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def booking_roomCode_get(roomCode, monthToLoad):  # noqa: E501
    # 按房间信息和月份（query中）获取所有的预约信息
    responseList = []
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    try:
        room_account = Account(
            primary_smtp_address=('%s@agoraacademy.cn' % roomCode),
            credentials=credentials,
            config=config
        )
    except Exception as e:
        return e
    start_year = int(monthToLoad.split("-")[0])
    start_month = int(monthToLoad.split("-")[1])
    start = room_account.default_timezone.localize(EWSDateTime(start_year, start_month, 1))
    if start_month == 12:
        end = room_account.default_timezone.localize(EWSDateTime(start_year + 1, 1, 1))
    else:
        end = room_account.default_timezone.localize(EWSDateTime(start_year, start_month + 1, 1))
    try:
        for item in room_account.calendar.filter(start__range=(start, end)).all().order_by('start'):
            notes = db_session.query(orm.BookingNotes_db).filter(orm.BookingNotes_db.changekey == item.changekey).one_or_none()
            bookedByID = getattr(notes, "bookedByID", 0)
            bookedByName = getattr(notes, "bookedByName", "")
            responseList.append({
                'startDate': ("%d-%0*d-%0*d" % (item.start.year, 2, item.start.month, 2, item.start.day)),
                'endDate': ("%d-%0*d-%0*d" % (item.end.year, 2, item.end.month, 2, item.end.day)),
                'startTime': ("%0*d:%0*d" % (2, item.start.hour, 2, item.start.minute)),
                'endTime': ("%0*d:%0*d" % (2, item.end.hour, 2, item.end.minute)),
                'subject': item.subject,
                'changekey': item.changekey,
                'bookedByID': bookedByID,
                'bookedByName': bookedByName,
                'description': '' if not getattr(item, 'text_body') else getattr(item, 'text_body'),
                'type': 'appointment'
            })
    except Exception as e:
        print(e)
    return responseList, 200, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def booking_roomCode_post(roomCode, appointment):  # noqa: E501
    # 添加预约信息
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
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
    startDateTime = EWSDateTime(
        appointment['startYear'],
        appointment['startMonth'],
        appointment['startDay'],
        appointment['startHour'],
        appointment['startMinute']
    )
    endDateTime = EWSDateTime(
        appointment['endYear'],
        appointment['endMonth'],
        appointment['endDay'],
        appointment['endHour'],
        appointment['endMinute']
    )
    try:
        item = CalendarItem(
            account=room_account,
            folder=room_account.calendar,
            start=room_account.default_timezone.localize(startDateTime),
            end=room_account.default_timezone.localize(endDateTime),
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
        db_session.remove()
    except Exception as e:
        db_session.remove()
        return e
    return {'message': 'success'}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}


def booking_roomCode_delete(roomCode, monthToLoad, deleteInfo):  # noqa: E501
    # 按照月份、changekey、房间号删除预约信息
    changekey = deleteInfo['changekey']
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    learner = db_session.query(orm.Learner_db).filter(orm.Learner_db.openid == validation_result["openid"]).one_or_none()
    try:
        room_account = Account(
            primary_smtp_address=('%s@agoraacademy.cn' % roomCode),
            credentials=credentials,
            config=config
        )
    except Exception as e:
        return e
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
        db_session.remove()
    except Exception as e:
        db_session.remove()
        print(e)
    return {'message': 'success'}, 201, {"Authorization": validation_result["access_token"], "refresh_token": validation_result["refresh_token"]}
