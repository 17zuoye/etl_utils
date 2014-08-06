# -*- coding: utf-8 -*-

def set_default_value(obj, name, lambdas, msg=u""):
    setattr(obj, name, None)
    for lambda1 in lambdas:
        if getattr(obj, name) is None:
            try:
                setattr(obj, name, lambda1())
            except:
                pass
    assert getattr(obj, name) is not None, msg
