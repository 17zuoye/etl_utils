# -*- coding: utf-8 -*-

from .design_pattern import singleton
from collections import defaultdict

@singleton()
class DictUtilsClass(object):
    def nested_read(self, dict1, keys, default_val=None):
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


    def add_default_value(self, dict1, default_value=None):
        if default_value is None:
            default_value = sum(dict1.values()) / float(len(dict1))
        return defaultdict(lambda : default_value, dict1)

DictUtils = DictUtilsClass()
