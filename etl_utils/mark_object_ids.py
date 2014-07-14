# -*- coding: utf-8 -*-

from .item_increment_id_dict import ItemIncrementIdDict

class MarkObjectIds(object):
    """
    标记 之前这两个ObjectId是否已经被处理过
    """
    def __init__(self):
        self.mark_object_ids_dict = dict()

    def write(self, oids, value):
        self.mark_object_ids_dict[self.generate_key(oids)] = value

    def read(self, oids):
        k1 = self.generate_key(oids)
        return self.mark_object_ids_dict.has_key(k1) and self.mark_object_ids_dict[k1] or None

    def generate_key(self, oids):
        return ','.join(sorted([str(ItemIncrementIdDict.fetch(oid1)) for oid1 in oids]))
