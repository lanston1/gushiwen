import requests
from db import CookiesRedisClient
from config import *
import json
from lxml import etree

class ValidTester(object):
    '''
    验证redis数据库中的cookie是否有效
    '''
    def __init__(self):
        self.logined_url = LOGINED_URL
        self.cookies_db = CookiesRedisClient()

    def test(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        cookies = self.cookies_db.all()
        cookies = list(cookies)
        for cookie in cookies:
            print("Testing the cookies of", cookie.get('username'))
            jar = requests.cookies.RequestsCookieJar()
            for key, value in json.loads(cookie.get("cookies")).items():
                jar.set(key, value)
            response = requests.get(url=self.logined_url, headers=headers, cookies=jar)
            html = etree.HTML(response.text)
            if "我的收藏" in html.xpath('//div[@class="mainshoucang"]/span[1]/text()'):
                print("Valid cookies of ", cookie.get('username'))
            else:
                print("Invalid cookies of ", cookie.get('username'))
                self.cookies_db.delete(cookie.get('username'))
                print('Deleted cookies of ', cookie.get('username'))

if __name__ == "__main__":
    tester = ValidTester()
    tester.test()