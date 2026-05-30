import requests

from config import LOKER_SERVICE_URL


def get_lockers_by_location(lokasi):
    return requests.get(LOKER_SERVICE_URL, params={"lokasi": lokasi})
