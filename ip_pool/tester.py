# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import time
import sys
import aiohttp
import asyncio
from ip_pool.db import RedisClient
from ip_pool.settings import VALID_STATUS_CODES, TEST_URL, BATCH_TEST_SIZE
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientHttpProcessingError


class Tester(object):
    """定义一个检测模块类"""
    def __init__(self):
        """初始化"""
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        检测单个代理
        :param proxy: 被检测单个代理
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = "http://" + proxy
                print("正在测试代理", proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print("代理可用", proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法 ', response.status, 'IP', proxy)
            except (ClientError, asyncio.TimeoutError, AttributeError, ConnectionError):
                self.redis.decrease(proxy)
                print("代理请求失败", proxy)

    def run(self):
        """
        测试主函数
        :return: None
        """
        print("测试器开始启动......")
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            # 采用批量测试避免一次性测试全部代理导致内存开销过大问题
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i: i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print("测试器出错了，%s" % e.args)
