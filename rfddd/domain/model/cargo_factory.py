# coding=utf-8
"""the implement of factory"""

import abc
from factory import Factory
from delivery import Delivery
from cargo import Cargo


class CargoFactory(object):
    """Cargo factory class
    """

    def create(self, cargo_id, days):
        delivery = Delivery(days);
        return Cargo(delivery, cargo_id);

Factory.register(CargoFactory)

if __name__ == '__main__':
    from entity import Entity
    print 'Subclass:', issubclass(CargoFactory, Factory)
    print 'Instance:', isinstance(CargoFactory(), Factory)

    cargo = CargoFactory().create(1, 5)

    print 'Instance:', isinstance(cargo, Entity)
