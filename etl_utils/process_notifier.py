# -*- coding: utf-8 -*-

import os, re
import progressbar as pb


class ProcessNotifier(object):
    """
    Usage:

    for b1 in ProcessNotifier(Book).generator():
        # do b1
    """

    def __init__(self, scope, per1):
        """ TypeError: __init__() should return None, not 'generator' """
        if hasattr(scope, 'count') or isinstance(scope, list) or hasattr(scope, 'itervalues') or hasattr(scope, 'iterator'):
            self.scope = scope
        else:
            raise Exception(u"%s should be iteratable", str(scope))
        self.current_pid = os.getpid()
        self.per = per1

        # 兼容 list, dict, mongomock
        # 判断这个对象的属性方法来觉得用len还是count，不能覆盖所有情况，所以这里直接暴力解决。
        self.scope_count = None
        for lambda1 in [ lambda : len(scope), lambda : scope.count()]:
            if self.scope_count is None:
                try:
                    self.scope_count = lambda1()
                except:
                    pass
        assert self.scope_count is not None


    def iterator(self):
        if 'iterator' in dir(self.scope)        : return self.scope.iterator()
        if 'itervalues' in dir(self.scope)      : return self.scope.itervalues()
        return self.scope

    def generator(self):
        """ Use a Generator to print the inner status when iterate a scope."""
        base_str = "[pid %i] To loading %i records " % (self.current_pid, self.scope_count)

        process_count = 0

        widgets = ['  ', base_str, pb.Percentage(), ' ', pb.Bar(),
                   ' ', ItemProcessSpeed()]

        if self.scope_count:
            self.pbar = pb.ProgressBar(widgets=widgets, maxval=self.scope_count).start()

        for record in self.iterator():
            process_count += 1
            # Fix grow up when iterator
            if process_count > self.scope_count: process_count = self.scope_count
            if self.scope_count: self.pbar.update(process_count)
            yield record
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


def process_notifier(scope, per1=1000):
    return ProcessNotifier(scope, per1).generator()
