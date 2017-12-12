# coding=utf-8
"""the implement of value object"""


from abc import ABCMeta


class ValueObject(object):
    """VO abstract class
    """

    __metaclass__ = ABCMeta

    def __setattr__(self, name, value):
        raise AttributeError()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
