# -*- coding: utf-8 -*-

from collections import Counter

def most_common_inspect(list1):
    new_list = []
    for s1 in list1:
        if not isinstance(s1, unicode):
            s1 = str(s1).decode("UTF-8")
        new_list.append(s1)

    cc = Counter(new_list).most_common()

    if len(cc) > 0:
        max_len = len(max([c1[0] for c1 in cc], key=lambda x1: len(x1))) + 5

        for c1 in cc:
            print c1[0].ljust(max_len, ' '), ' : ', c1[1]

    return cc


def uniq_seqs(seqs, uniq_lambda=None):
    if uniq_lambda is None: return list(set(seqs))

    __uniq = set([])
    __remove_idxes = []

    for idx1, seq1 in enumerate(seqs[:]):
       __id = uniq_lambda(seq1)
       if __id in __uniq:
           __remove_idxes.append(idx1)
       else:
           __uniq.add(__id)

    new_seqs = []
    for idx1, seq1 in enumerate(seqs[:]):
        if idx1 not in __remove_idxes:
            new_seqs.append(seq1)

    seqs = new_seqs

    return seqs
