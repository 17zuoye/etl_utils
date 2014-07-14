# -*- coding: utf-8 -*-

import logging
from .string_utils import String

class BufferLogger(object):
    """日志缓存管理

    使用说明:
    append, inspect, clear

    临时打印:
    p
    """

    def __init__(self, logger_file_name):
        self.__init_logger__(logger_file_name)
        self.buffer1 = list()

    def append(self, *strs):
        self.buffer1.append(String.merge(*strs))
    info = append

    def inspect(self):
        buffer_copy = self.buffer1[:]
        self.buffer1 = list()
        for b1 in buffer_copy:
            self.logger.info(b1)

    def clear(self):
        self.buffer1 = list()

    def p(self, *strs):
        print String.merge(*strs)

    def __init_logger__(self, logger_file_name):
        # copied from http://kenby.iteye.com/blog/1162698
        # 创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logger_file_name)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
