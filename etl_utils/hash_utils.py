# -*- coding: utf-8 -*-

import hashlib

from .regexp_utils import regexp
from .design_pattern import singleton

@singleton()
class HashUtilsClass(object):

    def hashvalue_with_sorted(self, str1):
        # sub unicode str
        str1 = regexp.special_chars.sub("", str1)

        # turn into `str` type
        if isinstance(str1, unicode): str1 = str1.encode("UTF-8")

        # sorted in ASNII
        str1 = ''.join(sorted(list(str1)))

        return hashlib.md5(str1).hexdigest()

HashUtils = HashUtilsClass()
