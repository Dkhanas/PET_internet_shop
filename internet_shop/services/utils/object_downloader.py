import requests


def get_raw_object(url):
    try:
        response = requests.get(url, stream=True)
        return response.raw
    except requests.exceptions.RequestException:
        return None
