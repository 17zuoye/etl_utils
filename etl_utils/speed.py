# -*- coding: utf-8 -*-

from datetime import datetime

class Speed():
    def __init__(self):
        self.born_clock = datetime.now()
        self.last_clock = datetime.now()

        self.item_count    = 0

    def tick(self):
        self.last_clock = datetime.now()
        self.item_count += 1
        return self

    def inspect(self):
        if self.item_count == 0:
            print "当前还没有计数"
        else:
            c1 = self.item_count / (self.last_clock - self.born_clock).total_seconds()
            print "当前平均速度为1秒处理", c1, "个"
        return self
