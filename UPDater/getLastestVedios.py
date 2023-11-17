# getLatestVideos.py

import requests
import time
import logging
from getWbi import encWbi, getWbiKeys

logging.basicConfig(level=logging.INFO, filename='Doc/UPdater.log', format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_videos(mid, session):
    logging.info(f"Getting latest videos for MID: {mid}")
    img_key, sub_key = getWbiKeys()

    # 准备请求参数
    params = {'mid': mid, 'pn': '1', 'ps': '1', 'index': '1'}
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Bilibili API Client/1.0)'}

    # 进行Wbi签名
    signed_params = encWbi(params, img_key, sub_key)

    # 发送请求
    url = 'https://api.bilibili.com/x/space/wbi/arc/search'
    response = session.get(url, params=signed_params, headers=headers)

    # print(f"Request URL: {url}")
    # print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        logging.info("Successfully fetched latest videos")
        data = response.json()
        # print(f"API response: {data}")
        if data['code'] == 0 and data['data']['list']['vlist']:
            return data['data']['list']['vlist'][0]
    else:
        logging.error(f"Failed to fetch videos. Status Code: {response.status_code}")
    return None

