# -*- coding: utf-8 -*-

from werkzeug.utils import cached_property, environ_property
from singleton import singleton

class ClassPropertyDescriptor(object):

    def __init__(self, func, name=None, doc=None):
        original_func = func.__func__

        self.__name__ = name or original_func.__name__
        self.__module__ = original_func.__module__
        self.__doc__ = doc or original_func.__doc__
        self.func = original_func

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        value = klass.__dict__.get(self.__name__)
        if isinstance(value, ClassPropertyDescriptor):
            value = self.func(klass)
            setattr(klass, self.__name__, value)
        return value


def classproperty(func):
    """
    Mimic werkzeug.utils's cached_property.

    A decorator that converts a function into a lazy class property.
    The function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

        class Foo(object):

            @classproperty
            def bar(cls):
                # calculate something important here
                return 42
        Foo.bar # => 42

    The class has to have a `__dict__` in order for this property to
    work.
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)
