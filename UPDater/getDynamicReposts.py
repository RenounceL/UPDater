# getDynamicReposts.py

import requests


def fetch_latest_updates(session):
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/portal'
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
