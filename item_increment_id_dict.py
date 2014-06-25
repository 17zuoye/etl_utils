# -*- coding: utf-8 -*-

class ItemIncrementIdDict(object):
    """ Assign an auto increment integer to item, e.g. an object_id.

    Usage:

    ItemIncrementIdDict.fetch(obj1) # => 1
    ItemIncrementIdDict.fetch(obj1) # => 1
    ItemIncrementIdDict.fetch(obj2) # => 2
    ItemIncrementIdDict.fetch(obj5) # => 3
    ItemIncrementIdDict.fetch(obj2) # => 2
    """

    count = 0
    object_id_to_increment_dict = dict()

    @classmethod
    def fetch(cls, object_id1):
        if cls.object_id_to_increment_dict.has_key(object_id1):
            return cls.object_id_to_increment_dict[object_id1]
        else:
            cls.count += 1
            cls.object_id_to_increment_dict[object_id1] = cls.count
            return cls.count
