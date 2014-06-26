# -*- coding: utf-8 -*-

import os
import re
from .cpickle_cache import cPickleCache
current_dir = os.path.dirname(os.path.realpath(__file__))

from werkzeug.utils import cached_property

class LazyData(object):

    @cached_property
    def en_us_dict(self):
        import enchant
        return enchant.Dict("en_US")

    @cached_property
    def two_length_words(self):
        """
        检查 2个字符 的字符组 是否是正常单词 或 词组
        e.g. `"At" in two_length_words`
        """
        return cPickleCache(current_dir + "/two_length_words.cPickle", load__two_length_words__func).process()

    @cached_property
    def regular_words(self):
        import nltk
        import marisa_trie
        from .regexp import word_regexp
        return marisa_trie.Trie([unicode(w1) for w1 in nltk.corpus.abc.words() if word_regexp.match(w1)])

ld = LazyData()


def load__two_length_words__func():
    import nltk
    import marisa_trie
    return marisa_trie.Trie( \
                sorted( \
                list( \
                set(\
                    [w1 for w1 in nltk.corpus.abc.words() \
                        if (len(w1) == 2) and \
                            re.compile("[a-z]", re.IGNORECASE).match(w1[0]) \
                    ] \
                ))))
