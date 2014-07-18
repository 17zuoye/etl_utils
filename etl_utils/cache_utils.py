# -*- coding: utf-8 -*-

import os, sys, time, cPickle
from termcolor import cprint

from werkzeug.utils import cached_property

def cpickle_cache(filename, func1):
    """
    Usage:

    questions = cpickle_cache(pickle_filename, load_questions_func)
    """
    return cPickleCache(filename, func1).process()


class cPickleCache(object):
    def __init__(self, filename, func1):
        self.filename = filename
        self.func     = func1

    def process(self):
        tb = time.time()
        cprint(u"[%s] " % self.filename, end='')

        if os.path.isfile(self.filename):
            cprint(u"cache is already exists!", end='')
            result = cPickle.load(open(self.filename, 'rb'))
        else:
            cprint(u"generating cache ...", end='')
            result = self.func()
            cPickle.dump(result, open(self.filename, 'wb'))
        cprint(" load in %2.2f sec" % (time.time()-tb))
        return result
