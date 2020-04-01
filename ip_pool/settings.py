# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8


# ------ redis相关参数配置 ------

# 1. redis数据库服务器地址
REDIS_HOST = "127.0.0.1"

# 2. redis数据库端口使用默认的端口6379
REDIS_PORT = 6379

# 3. redis数据库登入密码，没有设置密码则为None，有密码则更改此处即可。
REDIS_PASSWORD = None

# 4. redis有序集合键名
REDIS_KEY = "proxies"

# 5. 代理池最大容量
POOL_UPPER_THRESHOLD = 9999


# ------ 代理分数设置 ------
# 1.最大值
MAX_SCORE = 100

# 2. 最小值
MIN_SCORE = 0

# 3. 获取代理的初始值
INITIAL_SCORE = 10


# -----------抓取模块设置---------
# 1. 免费代理抓取开关， 默认为True 开启
CRAWLER_FREE_ENABLED = False

# 2. 付费代理提取开关，默认为False 禁用，若购买了付费代理， 则可设置为True
CRAWLER_MONEY_ENABLED = True


# ------ 检测模块相关参数设置 ------
# 1. 响应状态码
VALID_STATUS_CODES = [200, 302]

# 2.测试url
# TEST_URL = "http://www.baidu.com/"
# TEST_URL = "http://app.mi.com/"  # 小米应用商店
# TEST_URL = "https://www.doutula.com/"  # 斗图啦
TEST_URL = "https://www.dytt8.net/"  # 电影天堂8
# 3.批量测试数
BATCH_TEST_SIZE = 20


# ------ api相关参数设置 ------
# 1. api服务器地址
API_HOST = "0.0.0.0"

# 2. api端口
API_PORT = 5000


# ------ 调度模块相关参数配置 ------
# 1. 测试模块开关
TESTER_ENABLED = False

# 2.获取模块开关
GETTER_ENABLED = True

# 3.api接口开关
API_ENABLED = True

# 4. 检测周期20秒
TESTER_CYCLE = 20

# 5. 获取周期5分钟
GETTER_CYCLE = 10




