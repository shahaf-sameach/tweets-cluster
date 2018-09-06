import collections


def dnamedtuple(typename, field_names):
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    return T

