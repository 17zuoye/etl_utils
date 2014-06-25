# -*- coding: utf-8 -*-

from __future__ import print_function
import os, sys, time, cPickle

class cPickleCache(object):
    """
    Usage:

    questions = cPickleCache(pickle_filename, load_questions_func).process()
    """

    def __init__(self, filename, func1):
        self.filename = filename
        self.func     = func1

    def process(self):
        tb = time.time()
        if os.path.isfile(self.filename):
            print (u"[%s] cache is already exists!" % self.filename)
            result = cPickle.load(open(self.filename, 'rb'))
        else:
            print (u"[%s] generating cache ..." % self.filename)
            result = self.func()
            cPickle.dump(result, open(self.filename, 'wb'))
        print ("load in %2.2f sec" % (time.time()-tb))
        return result
