# -*- coding: utf-8 -*-

def dict_nested_read(dict1, keys, default_val=None):
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
