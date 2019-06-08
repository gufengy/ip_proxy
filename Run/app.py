import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from Manager import Manager
import time
from multiprocessing import Process
from Config import Control


app = Flask(__name__)  # 输入的是类名,或者包名, Flask会根据你传入的名字进行
m = Manager.Manager()
SLEEP_TIME = 2  # 当检测一次休眠的时间分钟
log = Control.get_logger(__name__)

deamon_pro_object = []

@app.route('/')  # 路由部分 当访问 /时会返回这个函数
def main():
    if len(deamon_pro_object) > 0:
        return "代理正在执行中"
    p = Process(target=run_daemon, name="守护进程")
    p.daemon = True   # 设置进程为守护进程, 但是如果设置了成了守护进程那么将无法开启子进程, 也就无法进行多进程的检测代理可用性
    p.start()
    deamon_pro_object.append(p)
    return "线程开始执行"

def run_daemon():
    while True:
        log.info("开始检查代理可用性")
        m.check_proxy()
        log.info('程序开始休眠    10    秒')
        time.sleep(10)
        m.check_db()  # 检查数据库
        log.info("程序开始休眠    %s    分钟" % str(SLEEP_TIME))
        time.sleep(SLEEP_TIME*60)

'''
获取一个 可用的代理
'''
@app.route('/get')
def get():
    return str(m.get_proxy_info())

# '''
# 获取可用的数据量
# '''
# @app.route('/count')
# def count():
#     return str(m.get_proxy_keyong())

if __name__ == '__main__':
    app.run(port=8080)