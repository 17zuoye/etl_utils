# -*- coding: utf-8 -*-

import functools
__all__ = ['slots_with_pickle']


# dont inherit from object, so no __init__ method
class SlotPickleMixin:
    """This mixin makes it possible to pickle/unpickle objects with __slots__ defined.

    In many programs, one or a few classes have a very large number of instances.
    Adding __slots__ to these classes can dramatically reduce the memory footprint
    and improve execution speed by eliminating the instance dictionary. Unfortunately,
    the resulting objects cannot be pickled. This mixin makes such classes pickleable
    again and even maintains compatibility with pickle files created before adding
    __slots__.

    Recipe taken from:
    http://code.activestate.com/recipes/578433-mixin-for-pickling-objects-with-__slots__/
    """
    def __getstate__(self):
        return dict(
            (slot, getattr(self, slot))
            for slot in self.__slots__
            if hasattr(self, slot)
        )

    def __setstate__(self, state):
        for slot, value in state.items():
            setattr(self, slot, value)


def slots_with_pickle(*slots):
    def func(decorated_class):
        # set slots related
        setattr(decorated_class, '__slots__', slots)
        class _class(SlotPickleMixin, decorated_class): pass

        # set orig class attrs
        _class.__name__    = decorated_class.__name__
        _class.__module__  = decorated_class.__module__
        decorated_class    = _class

        decorated_class = _class
        return decorated_class
    return func
