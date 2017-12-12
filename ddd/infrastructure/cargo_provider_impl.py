# coding=utf-8

from domain.model.cargo_provider import CargoProvider


class CargoProviderImpl(CargoProvider):

    def confirm(self, cargo):
        print('confirm cargo')


if __name__ == '__main__':
    from domain.model.base.provider import Provider
    provider = CargoProviderImpl()
    print('Subclass:', issubclass(CargoProviderImpl, Provider))
    print('Instance:', isinstance(provider, Provider))
    provider.confirm(None)
