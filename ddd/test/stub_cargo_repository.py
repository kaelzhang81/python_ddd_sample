# coding=utf-8

from domain.model.repository import Repository


class StubCargoRepository:
    def __init__(self):
        self._repo = {}

    def add(self, id, obj):
        if self._has_key(id):
            return False
        self._repo[id] = obj
        return True

    def save(self, id, obj):
        if not self._has_key(id):
            return False
        self._repo[id] = obj
        return True

    def delete(self, id):
        if self._has_key(self, id):
            del self._repo[id]

    def find_by_id(self, id):
        return self._repo.get(id)

    def _has_key(self, id):
        return self._repo.has_key(id)

Repository.register(StubCargoRepository)

if __name__ == '__main__':
    print('Subclass:', issubclass(StubCargoRepository, Repository))
    print('Instance:', isinstance(StubCargoRepository(), Repository))
