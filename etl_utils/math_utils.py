# -*- coding: utf-8 -*-

class MathUtils(object):

    @classmethod
    def plus(cls, int_list):
        if len(int_list):
            return reduce(lambda x, y: x + y, int_list)
        else:
            return 0
