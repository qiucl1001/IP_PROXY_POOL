# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
from ip_pool.scheduler import Scheduler
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")  # 改变标准输出的默认编码


def main():
    try:
        s = Scheduler()
        s.run()
    except Exception as e:
        print(e.args)
        main()


if __name__ == '__main__':
    main()
