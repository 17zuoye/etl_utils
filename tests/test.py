# -*- coding: utf-8 -*-

import os, sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

import unittest

from etl_utils import *

# 1. test opts
inspect = False

# 2. test class
@slots_with_pickle('attr_a', 'attr_b', 'attr_c')
class Slots(object):
    def __init__(self):
        attr_a = 'a'
        attr_b = 'b'
        attr_c = 'c'

# 3. test cases
class TestPhrasalRecognizer(unittest.TestCase):
    def test_Unicode(self):
        self.assertTrue(UnicodeUtils.is_chinese(u"你"))
        self.assertFalse(UnicodeUtils.is_chinese(u"h"))

        self.assertTrue(UnicodeUtils.is_number(u"3"))
        self.assertFalse(UnicodeUtils.is_number(u"a"))

        self.assertTrue(UnicodeUtils.is_alphabet(u"h"))
        self.assertFalse(UnicodeUtils.is_alphabet(u"3"))

        self.assertTrue(UnicodeUtils.is_other(u"。"))
        self.assertFalse(UnicodeUtils.is_other(u"a"))

        #test Q2B and B2Q
        for i in range(0x0020,0x007F):
            if inspect:
                print Q2B(B2Q(unichr(i))),B2Q(unichr(i))

        #test uniform
        ustring=u'中国 人名ａ高频Ａ'
        ustring=UnicodeUtils.uniform(ustring)
        ret=UnicodeUtils.string2List(ustring)
        self.assertEqual(ret, [u"中国", u"人名a高频a"])

        self.assertEqual(u"@",    UnicodeUtils.stringQ2B(u"＠"))
        self.assertEqual(u"Z",    UnicodeUtils.Q2B(u"Ｚ"))
        self.assertEqual(u"...",  UnicodeUtils.stringQ2B(unicode("…", "UTF-8")))
        self.assertEqual(u"'",    UnicodeUtils.stringQ2B(u"′"))

        self.assertEqual(jieba_parse("精确模式"), [u"精确", u"模式"])

        # Fix wired error
        # UnicodeDecodeError: 'utf8' codec can't decode byte 0xf3 in position 1: invalid continuation byte
        print "[__file__]", __file__

        current_file = UnicodeUtils.read(os.path.join(root_dir, "tests/test.py"))
        self.assertTrue(isinstance(current_file, unicode))

    def test_dict_utils(self):
        d1 = {"a" : {"b" : "c"} }
        self.assertEqual(DictUtils.nested_read(d1, ["a", "b"]), "c")

        d2 = {"a" : 1, "b" : 2 }
        d2_1 = DictUtils.add_default_value(d2)
        self.assertEqual(d2_1["not_exist"], 1.5)

    def test_ItemsGroupAndIndexes(self):
        igi = ItemsGroupAndIndexes()
        igi.add([1,2,3])
        igi.add([4,5,6])
        igi.add([7,8,9])
        igi.add([10,11])
        self.assertEqual(igi.result_json(), [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11]])
        self.assertEqual(igi.find(7), [7,8,9])
        self.assertTrue(igi.exists(3))
        self.assertFalse(igi.exists(13))
        self.assertTrue(igi.exists_between(10, 11))
        self.assertEqual(igi.groups_len(), 4)
        self.assertEqual(igi.items_len(), 11)

    def test_re_special_chars(self):
        __answers_str = "WhoWhoseWho\xe2\x80\x99s"
        self.assertEqual(regexp.special_chars.sub("", __answers_str), "WhoWhoseWhos")

    def test_string_utils(self):
        def func(a, b):
            pure_english_len = UnicodeUtils.rjust(a, 20).count(' ')
            with_chinese_len = UnicodeUtils.rjust(b, 20).count(' ')
            self.assertEqual(pure_english_len, with_chinese_len)

        func(u"ｂ", u"你")
        func(u"在", u"、")
        func(u"Ruby vs Python", u"中文 、 Python")

        self.assertEqual(StringUtils.frequence_chars_info("hello world"), {'uniq_chars__len': 8, 'sorted_freq_chars': 'lo '})
        self.assertEqual(StringUtils.frequence_chars_info("ccbbaaa"), {'uniq_chars__len': 3, 'sorted_freq_chars': 'abc'})

    def test_calculate_entropy(self):
        data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        self.assertTrue(calculate_entropy(data) > 1)

    def test_lazy_data(self):
        self.assertEqual(ld.lemmatize("having"), "have")
        self.assertTrue(ld.two_length_words)
        self.assertTrue(ld.regular_words)

    def test_cpickle_cache(self):
        data1 = ["cpickle_cache"]
        file1 = root_dir + '/tests/test_cpickle_cache.cPickle'

        cpickle_cache(file1, lambda : data1)
        self.assertEqual(data1, cpickle_cache(file1, lambda : None))
        os.remove(file1)

    def test_hash_utils(self):
        self.assertEqual( \
                HashUtils.hashvalue_with_sorted("hello"), \
                HashUtils.hashvalue_with_sorted("elloh"))

    def test_itertools_utils(self):
        self.assertEqual(ItertoolsUtils.split_seqs_by_size([1,2,3,4], 2), \
                [[[1], [2, 3, 4]], [[1, 2], [3, 4]], [[1, 2, 3], [4]]])

        self.assertEqual(ItertoolsUtils.split_seqs_by_size([1,2,3,4], 3), \
                [[[1], [2], [3, 4]], [[1], [2, 3], [4]], [[1, 2], [3], [4]]])

        self.assertEqual(ItertoolsUtils.split_seqs_by_size([1,2,3,4,5], 3), \
                [[[1], [2], [3, 4, 5]], [[1], [2, 3], [4, 5]], [[1], [2, 3, 4], \
                [5]], [[1, 2], [3], [4, 5]], [[1, 2], [3, 4], [5]], [[1, 2, 3], [4], [5]]])

    def test_process_notifier(self):
        import time

        for line1 in process_notifier(file(__file__), msg=u"[test iter] FILE"):
            time.sleep(0.01)

        for i1 in process_notifier(range(365), msg=u"[测试 iter] range"):
            time.sleep(0.005)

        import mongomock
        scope = mongomock.Connection().db.TestModel # has no items
        process_notifier(scope, msg=u"MONGODB")

        for item1 in process_notifier(iter(range(1000)), msg=u"[test endless] go "):
            time.sleep(0.005)


    def test_design_pattern(self):
        o1 = object()

        class Foo():

            @classproperty
            def bar(cls):
                return o1

        self.assertEqual(Foo.bar, o1)

    def test_set_default_value(self):
        scope = range(100)

        v1 = set_default_value(
                [lambda : scope.iteritems(), lambda : scope.iterator(), \
                 lambda: iter(scope), lambda : None], \
                 unicode(scope) + u" should be iteratable!")
        self.assertEqual(type(v1).__name__, 'listiterator')

    def test_console_utils(self):
        d1 = {"a": u"你", "b": u"好"}
        self.assertTrue(uprint(d1, d1) in [u"{'a': u'\u4f60', 'b': u'\u597d'}, {'a': u'\u4f60', 'b': u'\u597d'}", u"{'b': u'\u597d', 'a': u'\u4f60'}, {'b': u'\u597d', 'a': u'\u4f60'}"])

    def test_slots_with_pickle(self):
        slots = [Slots() for idx1 in xrange(1000)]

        # mimic pickle and upickle
        file1 = root_dir + '/tests/test_slots_with_pickle.cPickle'
        cpickle_cache(file1, lambda : slots)
        self.assertEqual(len(slots), len(cpickle_cache(file1, lambda : not_exists)))
        os.remove(file1)

    def test_json_utils(self):
        import json
        class Foobar(object): # add __dict__ attr
            def __init__(self):
                self.unicode_value = json.loads('{"你好" : ["世界"]}')
        self.assertEqual(JsonUtils.unicode_dump(Foobar()), u'{"unicode_value": {"\u4f60\u597d": ["\u4e16\u754c"]}}')

        specify_chars = [u"\\\"", u"你好"]
        self.assertEqual(json.loads(JsonUtils.unicode_dump(specify_chars)), specify_chars)

        nested_unorder_dict_str = u"""{"z":1, "b":1, "h":1, "": {"z":1, "b":1, "h":1}}"""
        nested_order_dict_str   = u"""{"": {"b": 1, "h": 1, "z": 1}, "b": 1, "h": 1, "z": 1}"""
        self.assertEqual(JsonUtils.unicode_dump(json.loads(nested_unorder_dict_str)), nested_order_dict_str)


if __name__ == '__main__': unittest.main()
