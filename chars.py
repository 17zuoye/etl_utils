# -*- coding: utf-8 -*-

import re

"""
`cat txt/duplicated_fullcontent_result_random500_20140507_1053.txt | grep -v 当前平均 | grep -v 字符串相 | grep -v 个题目 | grep -v self.time | grep text`.split("\n").map {|line| line.split(/text[12]:  /)[1] }.join().split(//).uniq.reject {|c1| c1.match(/[\u4E00-\u9FA5]+/) }.reject {|c1| c1.match(/[a-z]/i) }.reject {|c1| c1.match(/[0-9]/) }.join("|")
# "’|—|？|;|。|，|：|）|（|．|！|、|“|”|\"|=|‘|′|/|　|\\|＿|…|+|–|Ⅰ|Ⅱ|`| |@|－|；|｀|＇|•|∶|４|２|１|ɑ|→|&|￥|´|√|×|ə|ɜ|ː|<|>|①|②|③|④|¥||"
"""

re_special_chars = re.compile(
                       r"""
                        ^X√$|^FT$| # 选择题答案的hash特别处理
                        \ |,|\.|\?|\n|\'|!| # 正常字符
                        ’|—|？|;|。|，|：|）|（|．|！|、|“|”|\"|=|‘|′|\/|　|\\|＿|…|\+|\–|Ⅰ|Ⅱ|`| |@|－|；|｀|＇|•|∶ # 特殊字符
                        """,
                    re.VERBOSE)

object_id_regexp = re.compile("^[a-z0-9]{24}$")

if __name__ == "__main__":
    __answers_str = "WhoWhoseWho\xe2\x80\x99s"
    print "before :", __answers_str
    print "after  :", re_special_chars.sub("", __answers_str)
