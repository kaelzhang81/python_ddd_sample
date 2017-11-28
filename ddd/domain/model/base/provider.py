# coding=utf-8
"""the interface of provider"""

from abc import ABCMeta, abstractmethod


class Provider(object):
    """Provider abstract class
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def confirm(self, *args):
        """the create method of factory"""
        raise NotImplementedError
