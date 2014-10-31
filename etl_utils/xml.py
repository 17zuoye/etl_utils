# -*- coding: utf-8 -*-

# 引入XML解析库
# xml.etree.ElementTree解析XML遇到 fontFamily="\u5b8b\u4f53" 这种属性时会无效
# 详情见 http://lxml.de/parsing.html#python-unicode-strings 描述

from itertools import chain
from .design_pattern import singleton, cached_property

@singleton()
class TextArrayXMLParserClass(object):
    """
    XML题目内容parse，见fullcontent.question.choice里的参考数据说明

    XPATH结构是 TextFlow{} -> p{} -> span{}.text
    """

    def parse(self, xml1):
        str_list = [[span1.text for span1 in p1.getchildren() if span1.text]
            # '\x1f' cause xml parser error
            for p1 in self.etree.XML(xml1.encode("UTF-8").replace('\x1f', '')).getchildren()]
        str_list = list(chain.from_iterable(str_list))

        return ' '.join(str_list)

    @cached_property
    def etree(self):
        # 'lxml >= 3.3.5',
        from lxml import etree
        return etree

TextArrayXMLParser = TextArrayXMLParserClass()
