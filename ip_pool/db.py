# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import re
import redis
import random
from ip_pool.error import PoolEmptyError
from ip_pool.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from ip_pool.settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE


class RedisClient(object):
    """定义一个代理池的存储模块，使用redis的有序集合维护"""
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化redis对象相关属性
        :param host: redis地址
        :param port: redis端口
        :param password: redis登入密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数
        :param proxy: 获取模块获取到的代理
        :param score: 分数
        :return: 添加结果
        """
        if not re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print("此代理不符合规范，抛弃掉...", proxy)
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            # return self.db.zadd(REDIS_KEY, score, proxy)

            # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        获取随机代理，先尝试获取代理最高分，如果获取不到最高分，则按照排名来获取代理，否则为异常
        :return: 获取到的随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return random.choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        设置代理值减一分机制，如果代理分数小于最小值， 则移除此代理
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print("当前代理~~~<%s>~~~的当前分数~~~<%d>~~~减1..." % (proxy, score))
            # return self.db.zincrby(REDIS_KEY, proxy, -1)

            # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print("当前代理~~~<%s>~~~的当前分数为~~~<%d>~~~从数据库中移除..." % (proxy, score))
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: 代理是否存在
        """
        # return not self.db.zscore(REDIS_KEY, proxy) == None  # ?
        if not self.db.zscore(REDIS_KEY, proxy):
            return None
        else:
            return "代理存在", proxy

    def max(self, proxy):
        """
        将代理设置为最大值
        :param proxy: 代理
        :return: 设置代理后的结果
        """
        print("代理~~~<%s>~~~可用，设置为~~~<%d>~~~" % (proxy, MAX_SCORE))
        # return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

        # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取redis数据库中所有代理的数量
        :return: 代理数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取redis数据库中所有的代理
        :return: 全部代理为一个列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
