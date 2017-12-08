# coding=utf-8
"""the implement of entity"""

from abc import ABCMeta
from itertools import count

class Entity(object):
    """the entity meta class
    """
    __metaclass__ = ABCMeta
    _instance_id_generator = count()

    def __init__(self, eid):
        self._eid = eid
        self._instance_id = next(Entity._instance_id_generator)
 
    def __eq__(self, other):
        return self._id == other.id

    def __ne__(self, other):
        return not self == other
 
    @property
    def instance_id(self):
        """the instance id of entity"""
        return self._instance_id

    @property
    def eid(self):
        """the property of id"""
        return self._eid
