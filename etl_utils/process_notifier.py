# -*- coding: utf-8 -*-

import os
import progressbar as pb
import humanize


class ProcessNotifier(object):
    def __init__(self, scope, msg):
        """ TypeError: __init__() should return None, not 'generator' """
        from .object_utils import set_default_value

        scope_repr = unicode(repr(type(scope)))

        self.orig_scope = scope
        self.iterator = set_default_value(
              [lambda : scope.iteritems(), lambda : scope.iterator(), lambda: iter(scope), ], \
              scope_repr + u" should be iteratable!")

        self.current_pid = os.getpid()
        self.msg = msg

        # 兼容 list, dict, mongomock, file
        # 判断这个对象的属性方法来觉得用len还是count，不能覆盖所有情况，所以这里直接暴力解决。
        self.total_count = set_default_value( \
            [ lambda : len(scope), lambda : scope.count(), lambda : os.path.getsize(scope.name)], \
              scope_repr + u" should be counted!")
        self.is_file = isinstance(scope, file)


    def generator(self):
        """ Use a Generator to print the inner status when iterate a scope."""
        base_str = (u"%s {pid:%i, records:%i}" % (self.msg, self.current_pid, self.total_count)) \
                   if not self.is_file else \
                   (u"%s {pid:%i, file:%s, size:%s}" % (self.msg, self.current_pid, self.orig_scope.name, humanize.naturalsize(self.total_count)))

        widget_cls = FileProcessSpeed if self.is_file else ItemProcessSpeed
        widgets = [' ', base_str.encode("UTF-8"), pb.Percentage(), ' ', pb.Bar(),
                   ' ', widget_cls()]

        process_count = 0
        pre_process_count = 0
        one_percent = self.total_count / 200

        self.pbar = None
        if self.total_count:
            self.pbar = pb.ProgressBar(widgets=widgets, maxval=self.total_count).start()

        for record in self.iterator:
            process_count += ((len(record) + 1) if self.is_file else 1)
            # Fix grow up when iterator
            if process_count > self.total_count: process_count = self.total_count
            if self.total_count and (process_count - pre_process_count > one_percent):
                self.pbar.update(process_count)
                pre_process_count = process_count
            yield record

        if self.pbar:
            self.pbar.update(process_count) # finish it.
            print


class ItemProcessSpeed(pb.ProgressBarWidget):
    def __init__(self):
        self.fmt = '%6.2f items/s'
    def update(self, pbar):
        if pbar.seconds_elapsed < 2e-6:#== 0:
            bps = 0.0
        else:
            bps = float(pbar.currval) / pbar.seconds_elapsed
        return self.fmt % bps

class FileProcessSpeed(pb.ProgressBarWidget):
    def __init__(self):
        self.fmt = '%s/s'
    def update(self, pbar):
        if pbar.seconds_elapsed < 2e-6:#== 0:
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

    assert isinstance(msg, unicode)
    return ProcessNotifier(scope, msg).generator()
