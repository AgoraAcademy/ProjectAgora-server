import requests


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