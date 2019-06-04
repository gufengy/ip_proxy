import logging
from logging.handlers import HTTPHandler

file_path = 'output.log'
format = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
date_fmt = '%Y/%m/%d %H:%M:%S'

'''
这是一个日志打印的类, 负责日志的打印和控制
'''
class logger(object):


    def __init__(self):
        logging.basicConfig(format=format, level=logging.INFO, datefmt=date_fmt)
        # logging.basicConfig(format=format, level=logging.INFO, filename=file_path, datefmt=date_fmt)
        # self.logger = logging.getLogger(__name__)
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter(format, date_fmt)
        # # chlr = logging.StreamHandler()  # 输出到控制台的handler
        # # chlr.setFormatter(formatter)
        # # chlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
        fhlr = logging.FileHandler(file_path, encoding="utf-8")  # 输出到文件的handler
        fhlr.setFormatter(formatter)
        # 设置 输出到http服务器, 服务器需要进行处理才行
        # python -m http.server 8080   打开一个http服务
        # http_handler = HTTPHandler(host='localhost:8001', url='log', method='POST')   #
        # self.logger.addHandler(http_handler)
        # # self.logger.addHandler(chlr)
        self.logger.addHandler(fhlr)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)