# -*- coding: utf-8 -*-

from .buffer_logger import BufferLogger
from .cache_utils import cpickle_cache, cached_property
from .list import most_common_inspect, uniq_seqs
from .process_notifier import process_notifier
from .speed import Speed
from .string_utils import String
from .items_group_and_indexes import ItemsGroupAndIndexes
from .item_increment_id_dict import ItemIncrementIdDict
from .math_utils import MathUtils
from .xml import TextArrayXMLParser
from .dict_utils import dict_nested_read
from .extract_words import is_nltk_word, extract_words
from .regexp_utils import regexp
from .nlp import is_regular_word, jieba_parse
from .lazy_data import ld
from .unicode_utils import Unicode
from .entropy import calculate_entropy
from singleton import singleton
