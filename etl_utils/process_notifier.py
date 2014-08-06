# -*- coding: utf-8 -*-

import os
import progressbar as pb


class ProcessNotifier(object):
    """
    Usage:

    for b1 in ProcessNotifier(Book).generator():
        # do b1
    """

    def __init__(self, scope, per, msg):
        """ TypeError: __init__() should return None, not 'generator' """
        def set_default_value(name, lambdas, msg):
            setattr(self, name, None)
            for lambda1 in lambdas:
                if getattr(self, name) is None:
                    try:
                        setattr(self, name, lambda1())
                    except:
                        pass
            assert getattr(self, name) is not None, (unicode(scope) + u" " + msg)

        set_default_value('iterator', \
                          [lambda: iter(scope), lambda : scope.iteritems(), lambda : scope.iterator()], \
                          u"should be iteratable!")

        self.current_pid = os.getpid()
        self.per = per
        self.msg = msg

        # 兼容 list, dict, mongomock
        # 判断这个对象的属性方法来觉得用len还是count，不能覆盖所有情况，所以这里直接暴力解决。
        set_default_value('total_count', \
                          [ lambda : len(scope), lambda : scope.count()], \
                          u"should be counted!")


    def generator(self):
        """ Use a Generator to print the inner status when iterate a scope."""
        base_str = u"[pid %i] %s processing %i records " % (self.current_pid, self.msg, self.total_count)

        process_count = 0

        widgets = ['  ', base_str.encode("UTF-8"), pb.Percentage(), ' ', pb.Bar(),
                   ' ', ItemProcessSpeed()]

        if self.total_count:
            self.pbar = pb.ProgressBar(widgets=widgets, maxval=self.total_count).start()

        for record in self.iterator:
            process_count += 1
            # Fix grow up when iterator
            if process_count > self.total_count: process_count = self.total_count
            if self.total_count: self.pbar.update(process_count)
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


def process_notifier(scope, per=1000, msg=u"",):
    assert isinstance(msg, unicode)
    return ProcessNotifier(scope, per, msg).generator()
