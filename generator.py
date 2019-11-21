from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from captcha import CracklmageCode
from selenium.webdriver.chrome.options import Options
from PIL import Image
from config import *
from db import AccountRedisClient, CookiesRedisClient
import json

class GushiwenCookieGenerator(object):

    def __init__(self, browser_type=DEFAULT_BROWSER):
        self.account_db = AccountRedisClient()
        self.cookies_db = CookiesRedisClient()
        self.captcha_path = CAPTCHA_PATH
        self.captcha_name = CAPTCHA_NAME
        self.captcha = CracklmageCode(self.captcha_path)
        self.login_url = LOGIN_URL
        self.logined_url = LOGINED_URL
        self.browser_type = browser_type


    def _init_browser(self, browser_type):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :param browser: 浏览器 Chrome_headless/ Chrome
        :return:
        """
        if browser_type == 'Chrome_headless':
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
        elif browser_type == 'Chrome':
            self.browser = webdriver.Chrome()


    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts = self.account_db.all()
        cookies = self.cookies_db.all()
        accounts = list(accounts)
        valid_accouns = [cookie.get('username') for cookie in cookies]
        print('Getting', len(accounts), 'accounts from Redis')
        if len(accounts):
            self._init_browser(browser_type=self.browser_type)
        for account in accounts:
            if not account.get('username') in valid_accouns:
                print('Getting Cookies of ', account.get('username'), account.get('password'))
                self.set_cookies(account)
            else:
                print('Generator Run Finished')


    def set_cookies(self, account):
        """
        根据账户设置新的Cookies
        :param account:
        :return:
        """
        while True:
            cookies = self.new_cookies(account.get('username'), account.get('password'))
            if cookies:
                print('Saving Cookies to Redis', account.get('username'), cookies)
                self.cookies_db.set(account.get('username'), cookies)
                break



    def new_cookies(self, usename, password):
        """
        selenium模拟登陆，根据账户密码返回cookies
        :param usename:
        :param password:
        :return: usename, cookies
        """
        print("Generating Cookies of", usename)
        self.browser.delete_all_cookies()
        self.browser.get(self.login_url)
        wait = WebDriverWait(self.browser, 20)

        try:
            email_input = wait.until(EC.presence_of_element_located((By.ID, 'email')))
            email_input.send_keys(usename)
            password_input = wait.until(EC.presence_of_element_located((By.ID, 'pwd')))
            password_input.send_keys(password)
            code_input = wait.until(EC.presence_of_element_located((By.ID, 'code')))
            denglu_button = wait.until(EC.presence_of_element_located((By.NAME, 'denglu')))
            code = self.verify_code()
            if code:
                code_input.send_keys(code)
                denglu_button.click()
                try:
                    alert = self.browser.switch_to.alert
                    self.browser.switch_to.alert.accept()
                    print("验证码错误，刷新页面，重新登陆")
                    new_cookies = self.new_cookies(usename, password)
                    return new_cookies
                except:
                    self.browser.get(self.logined_url)
                    if '我的收藏' in self.browser.title:
                        print("登陆成功")
                        cookies = {}
                        for cookie in self.browser.get_cookies():
                            cookies[cookie["name"]] = cookie["value"]
                        print('成功获取到Cookies:', cookies)
                        return json.dumps(cookies)
            else:
                print("验证码获取失败，刷新页面，重新登陆")
                new_cookies = self.new_cookies(usename, password)
                return new_cookies
        except Exception as e:
            print(e.args)


    def verify_code(self):
        """
        截图屏幕，再截取验证码，最后识别验证码
        :return:
        """
        self.browser.save_screenshot(self.captcha_name)
        im = Image.open(self.captcha_name)
        im = im.crop((205,310,290,350))
        im.save(self.captcha_name)
        code = self.captcha.run()
        return code

    def close(self):
        '''
        关闭浏览器
        :return:
        '''
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')



if __name__ == "__main__":
    generator = GushiwenCookieGenerator()
    generator.run()
    generator.close()
