import requests

# 目标网址
url = 'https://www.bilibili.com'

# 发送请求
response = requests.get(url)

# 获取 cookie
cookies = response.cookies

# 打印所有 cookie
for cookie in cookies:
    print(cookie.name, cookie.value)