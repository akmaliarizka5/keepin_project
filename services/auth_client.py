import requests

from config import AUTH_LOGIN_URL, AUTH_REGISTER_URL


def parse_response(response):
    content_type = response.headers.get("content-type", "")

    try:
        data = response.json() if "application/json" in content_type else None
    except requests.exceptions.JSONDecodeError:
        data = None

    if data and isinstance(data, dict):
        message = data.get("detail") or data.get("message") or "Terjadi kesalahan"
    else:
        message = response.text.strip() or "Server tidak mengembalikan response JSON"

    return data, message


def login(payload):
    return requests.post(AUTH_LOGIN_URL, json=payload)


def register(payload):
    return requests.post(AUTH_REGISTER_URL, json=payload)
