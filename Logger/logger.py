import logging
from logging.handlers import RotatingFileHandler

file_path = 'output.log'
format = '%(asctime)s - %(levelname)s: %(message)s'
date_fmt = '%Y/%m/%d %H:%M:%S'

'''
这是一个日志打印的类, 负责日志的打印和控制
'''
class logger(object):


    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=logging.INFO)
        handler = RotatingFileHandler("../output/log.txt", maxBytes=1*1024*1024, encoding="utf-8", backupCount=10)

        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)