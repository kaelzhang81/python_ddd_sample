# coding=utf-8
"""the implement of factory"""

import factory
import delivery
import cargo

class CargoFactory(object):
    """Cargo factory class
    """

    def create(self, cargo_id, days):
        delivery = Delivery(days);
        return Cargo(delivery, cargo_id);

if __name__ == '__main__':
    print 'Subclass:', issubclass(CargoFactory, Factory)
    print 'Instance:', isinstance(CargoFactory, Factory)
