# -*- coding: utf-8 -*-

class ItemsGroupAndIndexes(object):
    """
    用于判断 一个元素 在 一个集合中 是否已经和其中某些元素 被group过。
    """

    def __init__(self):
        # 存储 排重结果，类似 [[oi1, oi2], [oi8, oi9, oi10], ...]
        self.result                           = list()
        # 存储 单个题目ID到 [oi1, oi2] 的索引
        self.object_id_to_same_ids_index_dict = dict()

    def exists_between(self, item_id1, item_id2):
        if not self.object_id_to_same_ids_index_dict.has_key(item_id1): return False
        if not self.object_id_to_same_ids_index_dict.has_key(item_id2): return False

        return self.object_id_to_same_ids_index_dict[item_id1] == self.object_id_to_same_ids_index_dict[item_id2]

    def exists(self, item_id):
        return item_id in self.object_id_to_same_ids_index_dict

    def add(self, same_ids):
        for same_id1 in same_ids:
            if self.exists(same_id1):
                continue
            else:
                # 存储数据
                self.result.append(same_ids)
                idx = len(self.result) - 1
                # 存储索引
                for same_id1 in same_ids:
                    self.object_id_to_same_ids_index_dict[same_id1] = idx

    def find(self, item_id):
        idx = self.object_id_to_same_ids_index_dict[item_id]
        return self.result[idx]

    def update(self, item_ids):
        pass

    def groups_len(self) : return len(self.result)
    def items_len(self)  : return len(self.object_id_to_same_ids_index_dict)

    def result_inspect(self):
        for l1 in self.result:
            print ', '.join([str(i1) for i1 in l1])
        print "groups_len", self.groups_len()
        print "items_len", self.items_len()

    def result_json(self):
        return [
                [(((type(i1) in [int, float]) and i1) or str(i1) ) for i1 in r1]
            for r1 in self.result]
