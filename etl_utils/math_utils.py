# -*- coding: utf-8 -*-

class MathUtils(object):
    @classmethod
    def plus(cls, obj1):
        if len(obj1):
            return reduce(lambda x, y: x + y, obj1)
        else:
            return 0
