# encoding: utf-8
# author: QCL
# datetime:2019/4/2 13:56
# software: PyCharm Professional Edition 2018.2.8
import time
from ip_pool.api import app
from ip_pool.tester import Tester
from ip_pool.getter import Getter
from ip_pool.settings import API_HOST, API_PORT
from ip_pool.settings import TESTER_CYCLE, GETTER_CYCLE
from ip_pool.settings import TESTER_ENABLED, GETTER_ENABLED, API_ENABLED
from multiprocessing import Process


class Scheduler(object):
    @staticmethod
    def scheduler_tester(cycle=TESTER_CYCLE):
        """
        定时测试代理模块
        :param cycle:定时器测试周期
        :return:None
        """
        tester = Tester()
        while True:
            print("测试器开始运行...")
            tester.run()
            time.sleep(cycle)

    @staticmethod
    def scheduler_getter(cycle=GETTER_CYCLE):
        """
        定时抓取模块
        :param cycle:抓取器时间周期
        :return: None
        """
        getter = Getter()
        while True:
            print("抓取器开始运行...")
            getter.run()
            time.sleep(cycle)

    @staticmethod
    def scheduler_api():
        """开启web api 接口"""
        app.run(API_HOST, API_PORT)

    def run(self):
        """启动调度器"""
        print("代理池开始运行...")

        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

