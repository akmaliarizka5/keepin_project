import requests

from config import BOOKING_SERVICE_URL


def create_booking(payload):
    return requests.post(f"{BOOKING_SERVICE_URL}/create", json=payload)


def get_user_bookings(id_user):
    return requests.get(f"{BOOKING_SERVICE_URL}/user/{id_user}")
