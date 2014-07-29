# -*- coding: utf-8 -*-

import os
import re
from .cache_utils import cpickle_cache, cached_property
current_dir = os.path.dirname(os.path.realpath(__file__))

from singleton import singleton

@singleton()
class LazyData(object):

    @cached_property
    def en_us_dict(self):
        """
        werid example.
        >>> en_us_dict.check(u"跑")
        True
        """
        import enchant
        return enchant.Dict("en_US")

    @cached_property
    def two_length_words(self):
        """
        检查 2个字符 的字符组 是否是正常单词 或 词组
        e.g. `"At" in two_length_words`
        """
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


        return cpickle_cache(current_dir + "/two_length_words.cPickle", load__two_length_words__func)

    @cached_property
    def regular_words(self):
        import nltk
        import marisa_trie
        from .regexp import word_regexp
        return marisa_trie.Trie([unicode(w1) for w1 in nltk.corpus.abc.words() if word_regexp.match(w1)])

    @cached_property
    def lemmatize(self):
        """
        return lemmatize method.

        必须得注明 词形 才行
        >>> lmtzr.lemmatize("having")
        'having'
        >>> lmtzr.lemmatize("having", 'v')
        'have'

        http://stackoverflow.com/questions/771918/how-do-i-do-word-stemming-or-lemmatization
        """
        from nltk.stem.wordnet import WordNetLemmatizer
        lmtzr = WordNetLemmatizer()

        def func(word1, tag1=None):
            if tag1 is None:
                word1 = lmtzr.lemmatize(word1, 'v')
                tag1 = 'n'
            return lmtzr.lemmatize(word1, tag1)
        return func

    @cached_property
    def tagged_words__dict(self):
        import nltk
        return {w1:t1.upper() for w1, t1 in nltk.corpus.brown.tagged_words()}



ld = LazyData()
