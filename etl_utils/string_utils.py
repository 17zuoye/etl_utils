# -*- coding: utf-8 -*-

import collections, re
from .regexp_utils import regexp
import math

class StringUtils(object):

    @classmethod
    def merge(self, *strs):
        """ 拼接 包含各种类型对象 的列表里的字符串 """
        result = list()
        for str1 in strs:
            if isinstance(str1, str):
                str1 = str1.decode("utf-8")
            elif isinstance(str1, unicode):
                str1
            else:
                str1 = str(str1)
            result.append(str1)
        return u' '.join(result)


    @classmethod
    def calculate_text_similarity(self, text1, text2, inspect=False, similar_rate_baseline=0.0, skip_special_chars=False):
        """
        目前简单计算 公共字符串比例即可，因为前几步已经算了答案数量和内容都是一样的。

        示例:
        print String.calculate_text_similarity("It\'s ten o\'clock! Let\'s go to bed. Good ______.", "Good ______. ")

        TODO
        误判:
        1. 51e2710da310cdedfd3167d0和51dec4e8a310cdedfd192487 的内容是d[i]ver和dr[i]ve 不同。
        解决，可以判断是仅仅一个单词长度就认为不一样，如果是填字母入单词的话。
        """

        # 如果只是hash就不必计算了，比如 51e9eb90a31047fb0c697413
        if not text1 or not text2 or \
                regexp.object_id.match(text1): # 只要一个match其实就不用比较了
            return {"similarity_rate": 0.0, "info": ""}

        if skip_special_chars:
            text1 = regexp.special_chars.sub("", text1)
            text2 = regexp.special_chars.sub("", text2)

        # 不兼容处理中文等非英文转化为list
        text1_list        = list(text1.strip())
        text2_list        = list(text2.strip())

        original_count    = len(text1_list) + len(text2_list)

        if original_count == 0.0:
            return {"similarity_rate": 0.0, "info": ""}

        # 两两字符串计算重复度用长度较小的那个来做外循环
        t1, t2 = (len(text1_list) > len(text2_list)) and (text2_list, text1_list) or (text1_list, text2_list)
        for char1 in t1[:]: # 使用copy去修复"for循环依赖索引"，感谢罗鑫
            if char1 in t2:
                text1_list.remove(char1)
                text2_list.remove(char1)

        remain_count    = len(text1_list) + len(text2_list)
        similarity_rate = float(original_count - remain_count) / original_count

        if inspect and (similarity_rate > similar_rate_baseline):
            lines = [
                        u"",
                        u"计算相似度详细log",
                        u"-"*40,
                        u"text1: %s" % text1,
                        u"text2: %s" % text2,
                        u"similarity_rate: %f" % similarity_rate,
                        u"-"*40,
                    ]
            info = "\n".join(lines)
        else:
            info = ""

        return {"similarity_rate": similarity_rate, "info": info}


    @classmethod
    def frequence_chars_info(self, str1, length_lambda=lambda len1 : len1):
        # 兼容unicode split
        if isinstance(str1, str): str1 = unicode(str1, "UTF-8")
        str_unicode_len = len(str1)
        default_length  = int(round(length_lambda(math.sqrt(str_unicode_len))))
        result1 = collections.Counter((str1 or "").lower())

        result2 = [t1[1] for t1 in sorted([(-t2, t1) for t1, t2 in result1.most_common()])]

        return {
                "sorted_freq_chars" : ''.join(result2)[0:default_length],
                "uniq_chars__len" : len(result2) }


String = StringUtils
