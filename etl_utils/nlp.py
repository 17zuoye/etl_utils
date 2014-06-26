# -*- coding: utf-8 -*-

import re

from .lazy_data import ld

def is_regular_word(str1):
    """
    werid example.
    >>> en_us_dict.check(u"跑")
    True
    """

    if isinstance(str1, unicode): str1 = str1.encode("UTF-8")
    str1 = str(str1)

    return (str1 == 'a') or (str1 == 'I') or ((len(str1) >= 2) and ld.en_us_dict.check(str1))
