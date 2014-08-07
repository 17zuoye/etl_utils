# -*- coding: utf-8 -*-

import re
from .design_pattern import singleton, cached_property

@singleton()
class RegexpUtils(object):

    @cached_property
    def alphabet(self): return re.compile("[a-z]", re.IGNORECASE)

    @cached_property
    def word(self): return re.compile("^[a-z]+$", re.IGNORECASE)

    @cached_property
    def upper(self): return re.compile("[A-Z]")

    @cached_property
    def object_id(self): return re.compile("^[a-z0-9]{24}$")

    @cached_property
    def special_chars(self):
        return re.compile(
                           r"""
                            ^X√$|^FT$| # 选择题答案的hash特别处理
                            \ |,|\.|\?|\n|\'|!| # 正常字符
                            ’|—|？|;|。|，|：|）|（|．|！|、|“|”|\"|=|‘|′|\/|　|\\|＿|…|\+|\–|Ⅰ|Ⅱ|`| |@|－|；|｀|＇|•|∶ # 特殊字符
                            """,
                        re.VERBOSE)

"""
`cat txt/duplicated_fullcontent_result_random500_20140507_1053.txt | grep -v 当前平均 | grep -v 字符串相 | grep -v 个题目 | grep -v self.time | grep text`.split("\n").map {|line| line.split(/text[12]:  /)[1] }.join().split(//).uniq.reject {|c1| c1.match(/[\u4E00-\u9FA5]+/) }.reject {|c1| c1.match(/[a-z]/i) }.reject {|c1| c1.match(/[0-9]/) }.join("|")
# "’|—|？|;|。|，|：|）|（|．|！|、|“|”|\"|=|‘|′|/|　|\\|＿|…|+|–|Ⅰ|Ⅱ|`| |@|－|；|｀|＇|•|∶|４|２|１|ɑ|→|&|￥|´|√|×|ə|ɜ|ː|<|>|①|②|③|④|¥||"
"""

regexp = RegexpUtils()
