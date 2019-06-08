from DB import redisclient
from Logger import logger
from Check_Proxy import Check_Proxy
from Get_Proxy import Get_Proxy

def get_redis_client():
    # 获取redis检查对象
    return redisclient.redisclient()

def get_ip_proxy():
    # 获取ip获取类对象
    return Get_Proxy.Get_Proxy()

def get_logger(name):
    # 获取日志对象
    return logger.logger(name).logger

def get_check_proxy():
    # 获取ip测试对象
    return Check_Proxy.Check_Proxy()
