# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8


class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)
        # super(PoolEmptyError, self).__init__()

    def __str__(self):
        return repr("代理池没有代理了......")

