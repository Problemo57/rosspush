import requests
import json
from os import environ

serverToken = environ["SERVER_TOKEN"]


def notifiy(device_token, notification):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }

    body = {
        'notification': notification,
        'to': device_token,
        'priority': 'high',
    }

    return requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)).status_code


def notifiy_class(class_entry, notification):

    for device_token, device_settings in class_entry.items():
        notifiy(device_token, notification)


if __name__ == "__main__":
    notification = {
        'title': 'Sending push form python script',
        'body': 'New Message'
    }

    from database import *
    db = Database("user.db")
    class_names = db.read_entrys("BGIT21")
    db.close()

    print(notifiy_class(class_names, notification))
