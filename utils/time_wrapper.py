from time import time
import logging


def timewrapper(func):
    """ decorator function to get running time"""
    def new_func(*args, **kwargs):
        t0 = time()
        a = func(*args, **kwargs)
        t1 = time()
        logging.debug("running time of %s -> %s sec" % (func.__name__, t1 - t0))
        return a

    return new_func
