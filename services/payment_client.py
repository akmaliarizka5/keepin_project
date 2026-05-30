import requests

from config import PAYMENT_SERVICE_URL


def create_payment(payload):
    return requests.post(f"{PAYMENT_SERVICE_URL}/create", json=payload)


def get_payment_by_booking(booking_id):
    return requests.get(f"{PAYMENT_SERVICE_URL}/booking/{booking_id}")


def update_payment_status(payment_id, status):
    return requests.patch(f"{PAYMENT_SERVICE_URL}/{payment_id}/status", json={"status": status})
