# -*- coding: utf-8 -*-

from werkzeug.utils import cached_property, environ_property
from singleton import singleton

class ClassPropertyDescriptor(object):

    def __init__(self, func, name=None, doc=None):
        self.func               = func.__func__
        self.__name__           = name or self.func.__name__
        self.__module__         = self.func.__module__
        self.__doc__            = doc or self.func.__doc__

        # 改用self.is_cached替换ClassPropertyDescriptor, 后者在类上使用装饰器时会失效
        self.is_cached          = False

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)

        if self.is_cached:
            return klass.__dict__.get(self.__name__)
        else:
            value = self.func(klass)
            setattr(klass, self.__name__, value)
            self.is_cached = True
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
