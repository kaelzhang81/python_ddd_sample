# coding=utf-8

from domain.model.base.provider import Provider


class CargoProvider(object):

    def confirm(self, cargo):
        pass

Provider.register(CargoProvider)

if __name__ == '__main__':
    provider = CargoProvider()
    print('Subclass:', issubclass(CargoProvider, Provider))
    print('Instance:', isinstance(provider, Provider))
    provider.confirm(None)
