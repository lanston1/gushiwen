from db import AccountRedisClient, CookiesRedisClient
from flask import Flask, g
from config import *

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>Welcome to Gushiwen Cookie Pool System</h2>'


def get_conn():
    """
    获取
    :return:
    """
    name = REDIS_NAME
    if not hasattr(g, name):
        setattr(g, name + '_cookies', eval('CookiesRedisClient' + '()'))
        setattr(g, name + '_account', eval('AccountRedisClient' + '()'))
    return g


@app.route('/<name>/random')
def random(name):
    """
    获取随机的Cookie, 访问地址如 /gushiwen/random
    :return: 随机Cookie
    """
    g = get_conn()
    cookies = getattr(g, name + '_cookies').random()
    return cookies

@app.route('/<name>/add/<username>/<password>')
def add(name, username, password):
    """
    添加用户, 访问地址如 /gushiwen/add/user/password
    """
    g = get_conn()
    result = getattr(g, name + '_account').set(username, password)
    return result


@app.route('/<name>/count')
def count(name):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, name + '_cookies').count()
    return str(count) if isinstance(count, int) else count


if __name__ == '__main__':
    app.run(host='0.0.0.0')