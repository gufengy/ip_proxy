import logging
from logging.handlers import RotatingFileHandler

format = '%(filename)s - line:%(lineno)d - %(asctime)s - %(levelname)s: %(message)s'
# 日志打印的文件的大小  <M>
file_size = 1
# 日志打印的最大副本数
backup_Count = 10
# 日志文件输出的位置
file_path = "../output"

'''
这是一个日志打印的类, 负责日志的打印和控制
'''


class logger(object):

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=logging.INFO)
        handler = RotatingFileHandler(file_path + "/log.txt", maxBytes=file_size * 1024 * 1024, encoding="utf-8",
                                      backupCount=backup_Count)
        handler_e = RotatingFileHandler(file_path + "/error.txt", maxBytes=file_size * 1024 * 1024, encoding="utf-8",
                                        backupCount=backup_Count)
        handler_w = RotatingFileHandler(file_path + "/warning.txt", maxBytes=file_size * 1024 * 1024, encoding="utf-8",
                                        backupCount=backup_Count)
        handler_d = RotatingFileHandler(file_path + "/debug.txt", maxBytes=file_size * 1024 * 1024, encoding="utf-8",
                                        backupCount=backup_Count)

        handler.setLevel(logging.INFO)
        handler_e.setLevel(logging.ERROR)
        handler_w.setLevel(logging.WARNING)
        handler_d.setLevel(logging.DEBUG)

        formatter = logging.Formatter(format)

        handler.setFormatter(formatter)
        handler_e.setFormatter(formatter)
        handler_w.setFormatter(formatter)
        handler_d.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(handler_e)
        self.logger.addHandler(handler_d)
        self.logger.addHandler(handler_w)
        self.logger.addHandler(console)
