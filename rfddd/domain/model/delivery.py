# coding=utf-8
"""the sample of value object"""

import value_object

class Delivery(object):
    """delivery class
    """
    
    def __init__(self, after_days):
        self._after_days = after_days

    @property
    def after_days(self):
        """the property of after days"""
        return self._after_days


ValueObject.register(Delivery)

if __name__ == '__main__':
    print 'Subclass:', issubclass(Delivery, ValueObject)
    print 'Instance:', isinstance(Delivery, ValueObject)
