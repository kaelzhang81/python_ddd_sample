# coding=utf-8

from domain.model.provider import Provider


class StubCargoProvider(object):

    def __init__(self):
        self._cargo_id = 0
        self._after_days = 0

    def confirm(self, cargo):
        self._cargo_id = cargo.id
        self._after_days = cargo.after_days

    @property
    def cargo_id(self):
        return self._cargo_id

    @property
    def after_days(self):
        return self._after_days

Provider.register(Provider)

if __name__ == '__main__':
    print('Subclass:', issubclass(StubCargoProvider, Provider))
    print('Instance:', isinstance(StubCargoProvider(), Provider))
