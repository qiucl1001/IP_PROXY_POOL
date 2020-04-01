# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import requests
from requests.exceptions import ConnectionError

base_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/73.0.3683.86 Safari/537.36",
    "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br"
}


def get_page(url, options={}):
    """抓取代理"""
    headers = dict(base_headers, **options)
    try:
        response = requests.get(url=url, headers=headers)
        url = response.url
        status_code = response.status_code
        print({"info": "抓取成功...", "url": url, "status_code": status_code})
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print("抓取失败...")
        return None
