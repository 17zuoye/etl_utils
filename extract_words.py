# -*- coding: utf-8 -*-

import re
import nltk
import marisa_trie
from .regexp import word_regexp

regular_words = marisa_trie.Trie([unicode(w1) for w1 in nltk.corpus.abc.words() if word_regexp.match(w1)])

def is_nltk_word(str1):
    if not isinstance(str1, unicode):
        try:
            str1 = unicode(str1, "UTF-8")
        except:
            return False # invalid chars
    return (str1 == u'a') or (str1 == u'I') or ((len(str1) >= 2) and (str1 in regular_words))


def extract_words(sentence):
    if isinstance(sentence, list): sentence = ' '.join(sentence)

    sentence = re.compile("[^a-z]+", re.IGNORECASE).sub(" ", sentence)
    these_words = [i1.strip() for i1 in sentence.split(" ")]
    words = [i1 for i1 in these_words if is_nltk_word(i1)]
    return words
