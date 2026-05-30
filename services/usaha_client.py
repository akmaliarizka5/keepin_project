import requests

from config import USAHA_SERVICE_URL


def create_usaha(payload):
    return requests.post(f"{USAHA_SERVICE_URL}/create", json=payload)


def get_usaha_by_owner(id_owner):
    return requests.get(f"{USAHA_SERVICE_URL}/owner/{id_owner}")


def get_usaha_summary(id_owner):
    return requests.get(f"{USAHA_SERVICE_URL}/owner/{id_owner}/summary")
