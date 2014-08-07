# -*- coding: utf-8 -*-

def set_default_value(lambdas, msg=u""):
    val = None
    for lambda1 in lambdas:
        if val is None:
            try:
                val = lambda1()
            except:
                continue
    assert val is not None, msg
    return val
