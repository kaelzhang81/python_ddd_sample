# coding=utf-8

import entity
import delivery

class CargoProvider(object):
    def __init__(self, id, delivery):
        self._id = id
        self._instance_id = next(Entity._instance_id_generator)
        slef._delivery = delivery

    def delay(self, days):
        after = self._delivery.AfterDays
        self._delivery = Delivery(after + days)

    def after_days(self):
        return self._delivery.AfterDays

Provider.register(CargoProvider)

if __name__ == '__main__':
    print 'Subclass:', issubclass(CargoProvider, Provider)
    print 'Instance:', isinstance(CargoProvider, Provider)
    
