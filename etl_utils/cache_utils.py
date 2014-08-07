# -*- coding: utf-8 -*-

import os, sys, time, cPickle
from termcolor import cprint

def cpickle_cache(filename, func1, quiet=False):
    """
    Usage:

    questions = cpickle_cache(pickle_filename, load_questions_func)
    """
    return cPickleCache(filename, func1, quiet).process()


class cPickleCache(object):
    def __init__(self, filename, func1, quiet=False):
        self.filename = filename
        self.func     = func1
        self.quiet    = quiet

    def blue(self, msg, is_ender=False):
        if not self.quiet:
            e1 = "\n" if is_ender else ""
            cprint(msg, 'blue', end=e1)

    def process(self):
        tb = time.time()
        self.blue(u"[%s] " % self.filename)

        if os.path.isfile(self.filename):
            self.blue(u"cache is already exists!")
            result = cPickle.load(open(self.filename, 'rb'))
        else:
            self.blue(u"generating cache ...")
            result = self.func()
            cPickle.dump(result, open(self.filename, 'wb'))
        self.blue(" load in %2.2f sec" % (time.time()-tb), True)
        return result
