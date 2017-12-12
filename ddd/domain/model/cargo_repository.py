# coding=utf-8

from domain.model.base.repository import Repository


class CargoRepository(object):
    def __init__(self):
        pass

    def add(self, id, obj):
        pass

    def save(self, id, obj):
        pass

    def delete(self, id):
        pass

    def find_by_id(self, id):
        pass

    def _has_key(self, id):
        pass

Repository.register(CargoRepository)

if __name__ == '__main__':

    print('Subclass:', issubclass(CargoRepository, Repository))
    print('Instance:', isinstance(CargoRepository(), Repository))
