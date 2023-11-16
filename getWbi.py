import requests
import time
import hashlib
import urllib.parse
from functools import reduce

# Wbi签名映射表
mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]

# 获取MixinKey
def getMixinKey(orig):
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

# 执行Wbi签名
def encWbi(params, img_key, sub_key):
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time
    params = dict(sorted(params.items()))
    params = {k: ''.join(filter(lambda chr: chr not in "!'()*", str(v))) for k, v in params.items()}
    query = urllib.parse.urlencode(params)
    wbi_sign = hashlib.md5((query + mixin_key).encode()).hexdigest()
    params['w_rid'] = wbi_sign
    return params

# 获取img_key和sub_key
def getWbiKeys():
    response = requests.get('https://api.bilibili.com/x/web-interface/nav')
    response.raise_for_status()
    json_content = response.json()
    img_url = json_content['data']['wbi_img']['img_url']
    sub_url = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key
