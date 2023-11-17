# get_bvid_cid.py

import requests
import re
import logging

logging.basicConfig(level=logging.INFO, filename='Doc/UPdater.log', format='%(asctime)s - %(levelname)s - %(message)s')

# Extract BVID from URL
def get_bvid_from_url(url):
    logging.info(f"Extracting BVID from URL: {url}")
    match = re.search(r'BV[a-zA-Z0-9]+', url)
    return match.group(0) if match else None

# Fetch CID using BVID
def get_cid(bvid):
    logging.info(f"Fetching CID for BVID: {bvid}")
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Successfully fetched CID")
        return response.json()['data']['cid']
    else:
        logging.error(f"Failed to fetch CID. Status Code: {response.status_code}")
    return None
