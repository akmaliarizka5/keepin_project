import requests

from config import LOKER_SERVICE_URL


def get_lockers(lokasi=None, search=None, sort_by="jarak", ukuran=None):
    params = {
        "lokasi": lokasi,
        "search": search,
        "sort_by": sort_by,
        "ukuran": ukuran,
    }
    params = {key: value for key, value in params.items() if value}
    return requests.get(LOKER_SERVICE_URL, params=params)


def get_lockers_by_location(lokasi):
    return get_lockers(lokasi=lokasi)
