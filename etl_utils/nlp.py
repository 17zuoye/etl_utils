# -*- coding: utf-8 -*-

import re
from .lazy_data import ld

def is_regular_word(str1):
    if isinstance(str1, unicode): str1 = str1.encode("UTF-8")
    str1 = str(str1)

    return (str1 == 'a') or (str1 == 'I') or ((len(str1) >= 2) and ld.en_us_dict.check(str1))

def jieba_parse(str1):
    """ 精确模式 """
    return list(ld.jieba.cut(str1, cut_all=False))
