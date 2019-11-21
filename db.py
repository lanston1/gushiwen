import redis
from config import *
import random

class AccountRedisClient(object):

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password = REDIS_PASSWORD, domain = 'account'):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.name = REDIS_NAME
        self.domain = domain
        if password:
            self._db = redis.StrictRedis(host=host, port=port, password=password)
        else:
            self._db = redis.StrictRedis(host=host, port=port)

    def key(self, key):
        """
        得到格式化的key
        :param key: 最后一个参数key
        :return:
        """
        return "{domain}:{name}:{key}".format(domain=self.domain, name=self.name, key=key)

    def set(self, key, value):
        """
        设置键值对
        :param key:
        :param value:
        :return:
        """
        return self._db.set(self.key(key), value)

    def get(self, key):
        """
        根据键名获取键值
        :param key:
        :return:
        """
        return self._db.get(self.key(key)).decode("utf-8")

    def delete(self,key):
        """
        根据键名删除键值
        :param key:
        :return:
        """
        return self._db.delete(self.key(key))

    def keys(self):
        """
        得到所有的键名
        :return:
        """
        return self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name))

    def flush(self):
        """
        清空数据库, 慎用
        :return:
        """
        self._db.flushall()

    def random(self):
        """
        随机得到一account
        :return:
        """
        return self._db.get(random.choice(self.keys()))

    def all(self):
        """
        获取所有账户, 以字典形式返回
        :return:
        """
        for key in self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name)):
            group = key.decode('utf-8').split(':')
            if len(group) == 3:
                username = group[2]
                yield {
                    'username': username,
                    'password': self.get(username)
                }

    def count(self):
        """
        获取当前Account数目
        :return: 数目
        """
        return len(self.keys())



class CookiesRedisClient(object):

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password = REDIS_PASSWORD, domain = 'cookies'):
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.name = REDIS_NAME
        self.domain = domain
        if password:
            self._db = redis.StrictRedis(host=host, port=port, password=password)
        else:
            self._db = redis.StrictRedis(host=host, port=port)

    def key(self, key):
        """
        得到格式化的key
        :param key: 最后一个参数key
        :return:
        """
        return "{domain}:{name}:{key}".format(domain=self.domain, name=self.name, key=key)

    def set(self, key, value):
        """
        设置键值对
        :param key:
        :param value:
        :return:
        """
        return self._db.set(self.key(key), value)

    def get(self, key):
        """
        根据键名获取键值
        :param key:
        :return:
        """
        return self._db.get(self.key(key)).decode("utf-8")

    def delete(self,key):
        """
        根据键名删除键值
        :param key:
        :return:
        """
        return self._db.delete(self.key(key))

    def keys(self):
        """
        得到所有的键名
        :return:
        """
        return self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name))

    def flush(self):
        """
        清空数据库, 慎用
        :return:
        """
        self._db.flushall()

    def random(self):
        """
        随机得到一cookies
        :return:
        """
        return self._db.get(random.choice(self.keys()))

    def all(self):
        """
        获取所有账户, 以字典形式返回
        :return:
        """
        for key in self._db.keys('{domain}:{name}:*'.format(domain=self.domain, name=self.name)):
            group = key.decode('utf-8').split(':')
            if len(group) == 3:
                username = group[2]
                yield {
                    'username': username,
                    'cookies': self.get(username)
                }

    def count(self):
        """
        获取当前Cookies数目
        :return: 数目
        """
        return len(self.keys())