# -*- coding: utf-8 -*-

def uprint(*objs):
    """ mimic default print with unicode support """
    text = ', '.join([repr(o1).decode("unicode-escape") for o1 in objs])
    print text
    return text
