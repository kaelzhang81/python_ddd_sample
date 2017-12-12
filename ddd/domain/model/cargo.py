# coding=utf-8
"""the implement of cargo"""

import abc
from .base.entity import Entity
from .delivery import Delivery

class Cargo(object):
    """the cargo class
    """
    
    def __init__(self, id, delivery):
        self._id = id
        self._instance_id = next(Entity._instance_id_generator)
        self._delivery = delivery

    def delay(self, days):
        """delay logic"""
        after = self._delivery.after_days
        self._delivery = Delivery(after + days)

    @property
    def after_days(self):
        """get after days of delivery"""
        return self._delivery.after_days

    @property
    def id(self):
        return self._id

    @property
    def delivery(self):
        """get after days of delivery"""
        return self._delivery

import Cp

Entity.register(Cp)

if __name__ == '__main__':
    print('Subclass:', issubclass(Cp, Entity))
    print('Instance:', isinstance(Cp(1, 100, 25, 10), Entity))


