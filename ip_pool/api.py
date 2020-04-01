# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
from flask import Flask, g
from ip_pool.db import RedisClient


__all__ = ["app"]
app = Flask(__name__)


def get_conn():
    """
    获取redis对象
    :return: 返回redis对象
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
        return g.redis


@app.route("/")
def index_page():
    """web api接口首页"""
    return "<h2>Welcome To Proxy Pool System</h2>"


@app.route("/random")
def get_proxy():
    """
    从redis数据库存储模块中获取随机的可用代理
    :return: 随机可用代理
    """
    conn = get_conn()
    return conn.random()


@app.route("/count")
def get_counts():
    """
    获取代理池的总代理数量
    :return: 代理池总数量
    """
    conn = get_conn()
    return str(conn.count())


@app.route("/all")
def get_all():
    """
    获取所有代理
    :return: 返回所有代理为一个列表
    """
    conn = get_conn()
    return str(conn.all())


if __name__ == '__main__':
    app.run()
