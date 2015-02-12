# -*- coding: utf-8 -*-

__all__ = ['JsonUtils']

import json
from .design_pattern import singleton

# copied from https://github.com/mikexstudios/python-firebase/pull/5/files
import datetime #for parse datetime object to string
import decimal #for parse decimal to string

class JSONEncoder(json.JSONEncoder):
    """ 支持 Decode datetime, decimal等类型 """
    def default(self, obj): # ignore
        if isinstance(obj, datetime.datetime):
            # '2014-10-13T17:51:09.692857'[0:19] => '2014-10-13T17:51:09'
            return obj.isoformat()[0:19]
        elif isinstance(obj, datetime.timedelta):
            return total_seconds(obj)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)
# TODO default_dict

@singleton()
class JsonUtilsClass(object):


    def unicode_dump(self, item1, **opts1):
        default_opt2 = {"cls":JSONEncoder, "ensure_ascii":False, "sort_keys":True}
        default_opt2.update(opts1)

        o1 = None # init
        if isinstance(item1, (dict, list, int, bool, float, unicode)):
            o1 = item1
        else:
            if '__dict__' in dir(item1):
                o1 = item1.__dict__
            else:
                raise Exception("%s can't be dumped" % item1)

        # decode("unicode-escape") 无法兼容  " \ 等转义，而是转不回来了
        return json.dumps(o1, **default_opt2)

JsonUtils = JsonUtilsClass()
