# -*- coding: utf-8 -*-

import os, re
from .cache_utils import cpickle_cache
from ._current_dir import current_dir
from .design_pattern import singleton ,cached_property

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
        return self.nltk_abc_data[0]

    @cached_property
    def regular_words(self): return self.nltk_abc_data[1]

    @cached_property
    def nltk_abc_data(self):
        nltk = self.nltk_download('abc')
        def load__nltk_abc_data__func():
            import marisa_trie
            from .regexp_utils import regexp
            words = nltk.corpus.abc.words()

            two_length_words_data = marisa_trie.Trie( \
                        sorted( \
                        list( \
                        set(\
                            [w1 for w1 in words \
                                if (len(w1) == 2) and \
                                    re.compile("[a-z]", re.IGNORECASE).match(w1[0]) \
                            ] \
                        ))))

            regular_words_data = marisa_trie.Trie([ \
                    unicode(w1) for w1 in words if regexp.word.match(w1)])

            return [two_length_words_data, regular_words_data]

        return cpickle_cache(current_dir + "/nltk_abc.cPickle", \
                load__nltk_abc_data__func, True)


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
        nltk = self.nltk_download('wordnet')
        lmtzr = nltk.stem.wordnet.WordNetLemmatizer()

        def func(word1, tag1=None):
            if tag1 is None:
                word1 = lmtzr.lemmatize(word1, 'v')
                tag1 = 'n'
            return lmtzr.lemmatize(word1, tag1)
        return func

    @cached_property
    def tagged_words__dict(self):
        nltk = self.nltk_download('brown')
        return {w1:t1.upper() for w1, t1 in nltk.corpus.brown.tagged_words()}

    def nltk_download(self, package):
        import nltk
        if nltk.data.path[0] != current_dir:
            nltk.data.path.insert(0, current_dir)

        if not os.path.isdir(os.path.join(current_dir, 'corpora', package)):
            nltk.download(info_or_id=package, download_dir=current_dir)
        return nltk



ld = LazyData()
