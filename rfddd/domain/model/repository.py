# coding=utf-8
"""the implement of repository"""

from abc import ABCMeta, abstractmethod

class Repository(object):
    """Repository abstract class
    """


    metaclass = ABCMeta

    @abstractmethod
    def add(self, eid, obj):
        """add entity"""
        raise NotImplementedError

    @abstractmethod
    def save(self, eid, obj):
        """save entity"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, eid):
        """delete entity"""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, eid):
        """find entity by id"""
        raise NotImplementedError
