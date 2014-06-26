# -*- coding: utf-8 -*-

import os

class ProcessNotifier(object):
    """
    Usage:

    for b1 in ProcessNotifier(Book).generator():
        # do b1
    """

    def __init__(self, scope, per1=1000):
        """ TypeError: __init__() should return None, not 'generator' """
        if hasattr(scope, 'count') or isinstance(scope, list) or hasattr(scope, 'itervalues') or hasattr(scope, 'iterator'):
            self.scope = scope
        else:
            raise Exception(u"%s should be iteratable", str(scope))
        self.current_pid = os.getpid()
        self.per = per1

    def iterator(self):
        if 'iterator' in dir(self.scope)        : return self.scope.iterator()
        if 'itervalues' in dir(self.scope)      : return self.scope.itervalues()
        return self.scope

    def generator(self):
        """ Use a Generator to print the inner status when iterate a scope."""
        process_count = 0

        # 兼容 list和dict
        scope_count = len(self.scope) if hasattr(self.scope, '__len__') else self.scope.count()

        print "[pid %i] To loading %i records..." % (self.current_pid, scope_count)
        for record in self.iterator():
            process_count += 1
            if (process_count > 0) and (process_count % self.per == 0):
                print "[pid %i][Processing records]" % self.current_pid, process_count, "."
            if process_count == scope_count:
                print "[pid %i][Processed records]" % self.current_pid, process_count, ", done!"
            yield record
        print
