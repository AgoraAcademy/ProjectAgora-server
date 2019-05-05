import connexion
import six
import os
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
    try:
        for roomList in roomLists:
            roomsEWS = GetRooms(protocol=account.protocol).call(
                roomlist=RoomList(
                    email_address=roomList['email'])
            )
            rooms = []
            for room in roomsEWS:
                rooms.append({
                    'name': room.name,
                    'email': room.email_address
                })
            entry = {
                'listname': roomList['name'],
                'rooms': rooms
            }
            response.append(entry)
    except Exception as e:
        return e
    """返回所有Course

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[Course]
    """
    return 'do some magic!'


def booking_roomCode_get(roomCode):  # noqa: E501
    # 按房间信息和月份（query中）获取所有的预约信息
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    """返回所有Course

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[Course]
    """
    return 'do some magic!'


def booking_roomCode_post():  # noqa: E501
    # 添加预约信息
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    """返回所有Course

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[Course]
    """
    return 'do some magic!'


def booking_roomCode_delete(uid):  # noqa: E501
    # 按照月份、uid、房间号删除预约信息
    validation_result = wxLogin.validateUser()
    if not validation_result["result"]:
        return {"error": "Failed to validate access token"}, 401
    """返回所有Course

    # noqa: E501

    :param learnerId:
    :type learnerId: int

    :rtype: List[Course]
    """
    return 'do some magic!'

