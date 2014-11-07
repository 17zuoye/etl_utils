# -*- coding: utf-8 -*-

from .design_pattern import cached_property, singleton

_ = u""

class UnicodeConvert(object):
    """
    汉字处理的工具:
    copied from https://github.com/oldhu/micolog-oldhu/blob/master/app/gbtools.py
    判断unicode是否是汉字，数字，英文，或者其他字符。
    全角符号转半角符号。
    """

    def is_chinese(self, uchar):
        """判断一个unicode是否是汉字"""
        assert isinstance(uchar, unicode)
        return uchar >= u'\u4e00' and uchar <= u'\u9fa5'

    def is_number(self, uchar):
        """判断一个unicode是否是数字"""
        assert isinstance(uchar, unicode)
        return uchar >= u'\u0030' and uchar <= u'\u0039'

    def is_alphabet(self, uchar):
        """判断一个unicode是否是英文字母"""
        assert isinstance(uchar, unicode)
        return (uchar >= u'\u0041' and uchar <= u'\u005a') \
                or (uchar >= u'\u0061' and uchar <= u'\u007a')

    def is_other(self, uchar):
        """判断是否非汉字，数字和英文字符"""
        assert isinstance(uchar, unicode)
        return not (UnicodeUtils.is_chinese(uchar) or UnicodeUtils.is_number(uchar) \
                or UnicodeUtils.is_alphabet(uchar))

    def B2Q(self, uchar):
        """半角转全角"""
        assert isinstance(uchar, unicode)
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:      #不是半角字符就返回原来的字符
                return uchar
        if inside_code == 0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code = 0x3000
        else:
                inside_code += 0xfee0
        return unichr(inside_code)

    def is_Q(self, uchar):
        return uchar != Q2B(uchar)

    def Q2B(self, uchar):
        """全角转半角"""
        assert isinstance(uchar, unicode)
        inside_code = ord(uchar)
        if inside_code == 0x3000:
                inside_code = 0x0020
        else:
                inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:      #转完之后不是半角字符返回原来的字符
                return uchar
        return unichr(inside_code)

    def stringQ2B(self, ustring, convert_strs={}):
        """把字符串全角转半角"""
        default_Q2B_convert = {
                                  unicode("…", "UTF-8") : u"...",
                                  u"′"                  : u"'",
                              }
        convert_strs = convert_strs or default_Q2B_convert

        assert isinstance(ustring, unicode)
        result = [UnicodeUtils.Q2B(uchar) for uchar in ustring]
        result = [(((uchar in convert_strs) and convert_strs[uchar]) or uchar) for uchar in result]
        return _.join(result)

    def uniform(self, ustring):
        """格式化字符串，完成全角转半角，大写转小写的工作"""
        return UnicodeUtils.stringQ2B(ustring).lower()

    def string2List(self, ustring):
        """将ustring按照中文，字母，数字分开"""
        retList=[]
        utmp=[]
        for uchar in ustring:
                if UnicodeUtils.is_other(uchar):
                        if len(utmp)==0:
                                continue
                        else:
                                retList.append(_.join(utmp))
                                utmp=[]
                else:
                        utmp.append(uchar)
        if len(utmp)!=0:
                retList.append(_.join(utmp))
        return retList


class UnicodeWidth(object):
    """ 处理unicode在终端下的显示宽度 """

    def ljust(self, str1, width, fillchar=' '):
        return self.just_str(str1, 'ljust', width, fillchar)

    def rjust(self, str1, width, fillchar=' '):
        return self.just_str(str1, 'rjust', width, fillchar)

    ######### private functions
    @cached_property
    def just_str(self):
        """
        兼容中文和全角字符的对齐打印。Compact with chinese ajust.
        """
        # `pip install urwid`
        from urwid import is_wide_char
        def func(str1, method, width, fillchar):
            if isinstance(str1, str): str1 = unicode(str1, "UTF-8")
            assert isinstance(str1, unicode)

            two_width_count = len([s1 for s1 in str1 if is_wide_char(s1, 0)])
            return getattr(str1, method)(width - two_width_count, fillchar)
        return func

class UnicodeFile(object):
    def read(self, filename):
        return open(filename).read().decode("UTF-8")


@singleton()
class UnicodeClass(UnicodeConvert, UnicodeWidth, UnicodeFile):
    pass

UnicodeUtils = UnicodeClass()
Unicode = UnicodeUtils
