# coding=utf-8
"""the sample of domain event"""

import domain_event

class CargoDelayedEvent(object):
    """cargo delayed domain event class
    """
        
    def __init__(self, cargo_id):
        self._cargo_id = cargo_id

DomainEvent.register(CargoDelayedEvent)

if __name__ == '__main__':
    print 'Subclass:', issubclass(CargoDelayedEvent, DomainEvent)
    print 'Instance:', isinstance(CargoDelayedEvent, DomainEvent)
