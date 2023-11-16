# qrLogin.py

import requests
import qrcode
import time

def qr_login():
    # 申请二维码
    response = requests.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate")
    data = response.json()['data']
    qr_url = data['url']
    qrcode_key = data['qrcode_key']

    # 生成二维码图片
    img = qrcode.make(qr_url)
    img.show()

    # 初始化session
    session = requests.Session()

    # 循环检查登录状态，每次检查间隔一定时间
    while True:
        time.sleep(10)  # 增加等待时间，例如10秒
        response = session.get("https://passport.bilibili.com/x/passport-login/web/qrcode/poll", params={'qrcode_key': qrcode_key})
        result = response.json()
        code = result['data']['code']
        if code == 0:  # 登录成功
            print("登录成功")
            return session
        elif code in [86038, 86101]:  # 二维码失效或未扫描
            print("继续等待扫描...")
            continue  # 如果是未扫描状态，继续循环等待
        else:
            print("出现未知错误，状态码:", code)
            return None
