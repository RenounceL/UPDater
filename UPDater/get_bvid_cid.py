# get_bvid_cid.py

import requests
import re

# Extract BVID from URL
def get_bvid_from_url(url):
    match = re.search(r'BV[a-zA-Z0-9]+', url)
    return match.group(0) if match else None

# Fetch CID using BVID
def get_cid(bvid):
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']['cid']
    return None
