# coding=utf-8
"""the implement of domain event"""

import abc
import itertools
from utility.time import monotonic_utc_now

_now = object()

class DomainEvent:
    """domain event class
    """
        
    metaclass=abc.ABCMeta

    def __init__(self, timestamp=_now, **kwargs):
        self.__dict__['timestamp'] = monotonic_utc_now() if timestamp is _now else timestamp
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        """redefine __setattr__"""
        if hasattr(self, key):
            raise AttributeError("{} attributes can be added but not modified."
                                 "Attribute {!r} already exists with value {!r}".format(
                                 self.__class__.__name__, key, getattr(self, key)))
        self.__dict__[key] = value

    def __eq__(self, rhs):
        """redefine __eq__"""
        if type(self) is not type(rhs):
            return NotImplemented
        return self.__dict__ == rhs.__dict__

    def __ne__(self, rhs):
        """redefine __ne__"""
        return not (self == rhs)

    def __hash__(self):
        """redefine __hash__"""
        return hash(tuple(itertools.chain(self.__dict__.items(),
                                          [type(self)])))

    def __repr__(self):
        """redefine __repr__"""
        return self.__class__.__qualname__ + "(" + ', '.join(
            "{0}={1!r}".format(*item) for item in self.__dict__.items()) + ')'
