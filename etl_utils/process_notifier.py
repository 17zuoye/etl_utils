# -*- coding: utf-8 -*-

import os
import sys
import progressbar as pb
import humanize


class ProcessNotifier(object):

    def __init__(self, scope, msg=u""):
        """ TypeError: __init__() should return None, not 'generator' """
        from .object_utils import set_default_value

        scope_repr = unicode(repr(type(scope)))
        self.orig_scope = scope
        self.current_pid = os.getpid()
        self.msg = msg

        # set_default_value 兼容抛出其他异常, 比如数据库没权限
        # NOTE: iter(generator) # => still genrator
        self.iterator = set_default_value(
            [lambda: scope.iteritems(), lambda: scope.iterator(), lambda: iter(scope), ],
            scope_repr + u" should be iteratable!")

        iter_types = ["endless", "file", "listdict"]
        self.iter_type = None
        if isinstance(scope, file):
            self.iter_type = "file"
        if (self.iter_type not in ["file"]) and ("next" in dir(scope)):
            self.iter_type = "endless"
        self.iter_type = self.iter_type or "listdict"
        assert self.iter_type in iter_types

        # 兼容 list, dict, mongomock, file
        # 判断这个对象的属性方法来觉得用len还是count，不能覆盖所有情况，所以这里直接暴力解决。
        if self.iter_type == "endless":
            self.total_size = 0
        else:
            self.total_size = set_default_value(
                [lambda: len(scope), lambda: scope.count(), lambda: os.path.getsize(scope.name)],
                scope_repr + u" should be counted!")

        # process status
        self.counter = 0
        self.pre_counter = 0
        self.default_chunk_size = 200
        self.chunk_size = self.total_size / self.default_chunk_size  # update rate should between 100 and 200 .

        # bind a generator
        """ Use a Generator to print the inner status when iterate a scope."""
        self.generator = getattr(self, self.iter_type + "_generator")

    def __pbar(self, status_str, widget_cls):
        weights = [' ', status_str.encode("UTF-8"), pb.Percentage(), ' ', pb.Bar(),
                   ' ', widget_cls()]
        return pb.ProgressBar(widgets=weights, maxval=self.total_size).start()

    def __update_status_by_item(self, update_counter_lambda=lambda self: self, calculate_item_size_lambda=lambda item1: 1):
        for item1 in self.iterator:
            self.counter += calculate_item_size_lambda(item1)
            if (self.counter > self.total_size) and (self.iter_type != "endless"):
                self.counter = self.total_size  # Fix grow up when iterator
            if self.counter - self.pre_counter > self.chunk_size:
                update_counter_lambda(self)
                self.pre_counter = self.counter
            yield item1
        update_counter_lambda(self)  # finish it.
        print

    def endless_generator(self):
        import time
        begin_time = time.time()
        self.chunk_size = self.chunk_size or self.default_chunk_size

        def print_current_progress_status(self):
            current_time = time.time()
            self.speed_str = self.counter / (current_time - begin_time)
            # "\r" means to clear current line
            sys.stdout.write((u"\r  %s {pid: %i, processed: %s items, speed: %.2f items/s . }" %
                              (self.msg, self.current_pid, self.counter, self.speed_str)).encode("UTF-8"))
            sys.stdout.flush()
        return self.__update_status_by_item(print_current_progress_status)

    def file_generator(self):
        if self.total_size == 0:
            return iter([])
        status_str = u"""%s {pid: %i, file: "%s", size: %s}""" % (
            self.msg,
            self.current_pid,
            self.orig_scope.name,
            humanize.naturalsize(self.total_size))
        self.pbar = self.__pbar(status_str, FileProcessSpeed)
        return self.__update_status_by_item(lambda self: self.pbar.update(self.counter),
                                            lambda item1: len(item1) + 1)

    def listdict_generator(self):
        if self.total_size == 0:
            return iter([])
        status_str = u"%s {pid:%i, records:%i}" % (self.msg, self.current_pid, self.total_size)
        self.pbar = self.__pbar(status_str, ItemProcessSpeed)
        return self.__update_status_by_item(lambda self: self.pbar.update(self.counter))


class ItemProcessSpeed(pb.ProgressBarWidget):

    def __init__(self):
        self.fmt = '%6.2f items/s'

    def update(self, pbar):
        if pbar.seconds_elapsed < 2e-6:  # == 0:
            bps = 0.0
        else:
            bps = float(pbar.currval) / pbar.seconds_elapsed
        return self.fmt % bps


class FileProcessSpeed(pb.ProgressBarWidget):

    def __init__(self):
        self.fmt = '%s/s'

    def update(self, pbar):
        if pbar.seconds_elapsed < 2e-6:  # == 0:
            bps = 0.0
        else:
            bps = float(pbar.currval) / pbar.seconds_elapsed
        return self.fmt % humanize.naturalsize(bps)


def process_notifier(scope, msg=u"",):
    """
    Usage:

    for b1 in process_notifier(a_list):
        # do b1
    """

    assert isinstance(msg, unicode), msg
    return ProcessNotifier(scope, msg).generator()
