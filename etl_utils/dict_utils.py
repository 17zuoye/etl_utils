# -*- coding: utf-8 -*-

from .design_pattern import singleton
from collections import defaultdict

@singleton()
class DictUtilsClass(object):
    def dict_nested_read(self, dict1, keys, default_val=None):
        if not isinstance(keys, list): keys = [keys]

        current_dict = dict1
        current_val  = default_val
        for k1 in keys:
            if not isinstance(current_dict, dict): break

            if isinstance(current_dict, dict):
                if current_dict.has_key(k1):
                    current_dict = current_dict[k1]
                    current_val  = current_dict
                else:
                    break

            if isinstance(current_dict, list):
                if len(current_dict) > k1:
                    current_dict = current_dict[k1]
                    current_val  = current_dict
                else:
                    break

        return current_val


    def add_default_value(self, d1, default_value=None):
        if default_value is None:
            default_value = sum(d1.values()) / float(len(d1))
        return defaultdict(lambda : default_value, d1)

DictUtils = DictUtilsClass()
