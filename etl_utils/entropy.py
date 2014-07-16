# -*- coding: utf-8 -*-

import math

def calculate_entropy(feature_with_count_dict):
    assert hasattr(feature_with_count_dict, 'iteritems')
    assert isinstance(feature_with_count_dict.iteritems().next()[1], int)

    feature_count_sum = float(sum(feature_with_count_dict.values()))

    entropy = 0.0
    for f1, c1 in feature_with_count_dict.iteritems():
        p_ij = c1 / feature_count_sum
        entropy += p_ij * math.log(p_ij)
    return - entropy
