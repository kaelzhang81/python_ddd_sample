# coding=utf-8
"""the implement of factory"""

from abc import ABCMeta, abstractmethod

class Factory(object):
    """Factory abstract class
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self):
        """the create method of factory"""
        raise NotImplementedError
