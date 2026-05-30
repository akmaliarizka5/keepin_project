import requests

from config import AUTH_LOGIN_URL, AUTH_REGISTER_URL


def login(payload):
    return requests.post(AUTH_LOGIN_URL, json=payload)


def register(payload):
    return requests.post(AUTH_REGISTER_URL, json=payload)
