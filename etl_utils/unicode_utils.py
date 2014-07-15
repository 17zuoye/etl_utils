# -*- coding: utf-8 -*-

from urwid import is_wide_char

class Unicode(object):

    @classmethod
    def ljust(self, str1, width, fillchar=' '):
        return just_str(str1, 'ljust', width, fillchar)

    @classmethod
    def rjust(self, str1, width, fillchar=' '):
        return just_str(str1, 'rjust', width, fillchar)

def just_str(str1, method, width, fillchar):
    """
    兼容中文和全角字符的对齐打印。Compact with chinese ajust.
    """
    if isinstance(str1, str): str1 = unicode(str1, "UTF-8")
    assert isinstance(str1, unicode)

    two_width_count = len([s1 for s1 in str1 if is_wide_char(s1, 0)])
    return getattr(str1, method)(width - two_width_count, fillchar)
