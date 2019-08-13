import requests
import os
import json
import datetime
from exchangelib import Credentials, Account, Configuration, DELEGATE, RoomList, CalendarItem, EWSDateTime
from swagger_server import orm, weapp

credentials = Credentials(
    os.environ["EWS_admin_email"],
    os.environ["EWS_admin_password"])

config = Configuration(server='outlook.office365.com', credentials=credentials)

admin_account = Account(
    primary_smtp_address='admin@agoraacademy.cn',
    credentials=credentials,
    autodiscover=False,
    config=config,
    access_type=DELEGATE
)


def getValidMicrosoftToken(learner, db_session):
    MICROSOFT_CLIENT_ID: str = os.environ['MICROSOFT_CLIENT_ID']
    MICROSOFT_CLIENT_SECRET: str = os.environ['MICROSOFT_CLIENT_SECRET']
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % learner.microsoftAccessToken,
    }
    meResponse = requests.get("https://graph.microsoft.com/v1.0/me/", headers=headers)
    if meResponse.status_code == 200:
        return learner.microsoftAccessToken
    if meResponse.status_code == 401:
        refreshPostBody = {
            "client_id": MICROSOFT_CLIENT_ID,
            "scope": "offline_access openid profile https://graph.microsoft.com/calendars.readwrite https://graph.microsoft.com/user.readwrite",
            "refresh_token": learner.microsoftRefreshToken,
            "grant_type": "refresh_token",
            "client_secret": MICROSOFT_CLIENT_SECRET
        }
        refreshResponse = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=refreshPostBody)
    if refreshResponse.status_code == 200:
        try:
            learner.microsoftAccessToken = refreshResponse.json()["access_token"]
            learner.microsoftRefreshToken = refreshResponse.json()["refresh_token"]
            db_session.commit()
        except Exception as e:
            print(str(e))
            db_session.remove()
            return ""
        return learner.microsoftAccessToken
    else:
        return ""


def getMe(microsoftAccessToken):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % microsoftAccessToken,
    }
    try:
        meResponse = requests.get("https://graph.microsoft.com/v1.0/me/", headers=headers)
    except Exception as e:
        print(str(e))
        return
    return meResponse.json()


def getSchedule(dateToLoad: str, nameList=[]):
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
        return {"message": "learner not found"}, 401
    nameList.append(learner.microsoftUserPrincipalName)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % getValidMicrosoftToken(learner, db_session),
        "Prefer": 'outlook.timezone="China Standard Time"'
    }
    dateToLoad_year = int(dateToLoad.split("-")[0])
    dateToLoad_month = int(dateToLoad.split("-")[1])
    dateToLoad_day = int(dateToLoad.split("-")[2])
    start = admin_account.default_timezone.localize(EWSDateTime(dateToLoad_year, dateToLoad_month, dateToLoad_day))
    end = start + datetime.timedelta(days=1)
    myScheduleBody = {
        "schedules": nameList,
        "startTime": {
            "dateTime": start.ewsformat()[:19],
            "timeZone": "China Standard Time"
        },
        "endTime": {
            "dateTime": end.ewsformat()[:19],
            "timeZone": "China Standard Time"
        },
        "availabilityViewInterval": "60"
    }
    myScheduleResponse = requests.post("https://graph.microsoft.com/v1.0/me/calendar/getSchedule ", headers=headers, data=json.dumps(myScheduleBody))
    return myScheduleResponse.json()


# def getUserSchedule(learnerId):
