# getDynamicReposts.py

import requests
import logging

logging.basicConfig(level=logging.INFO, filename='Doc/UPdater.log', format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_latest_updates(session):
    logging.info("Fetching latest updates")
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/portal'
    response = session.get(url)
    if response.status_code == 200:
        logging.info("Successfully fetched latest updates")
        return response.json()
    else:
        logging.error(f"Failed to fetch updates. Status Code: {response.status_code}")
        return None
