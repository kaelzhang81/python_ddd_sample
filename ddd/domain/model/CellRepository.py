# coding=utf-8
import Singleton

class cell(object):
    def __init__(self, id):
        self.id = id

    def get_cell_state(self):
        return 'available'

class ObjectRepository(object):
    def __init__(self):
        self._objDict = {}

    def add(self, id, obj):
        self._objDict[id] = obj


@Singleton
class CellRepository(ObjectRepository):
    def __init__(self):
        ObjectRepository.__init__(self)

    def find_all_available_cells(self):
        return filter(lambda x: x.get_cell_state() == 'available', self._objDict.values())


if __name__ == '__main__':
    repo = CellRepository()
    repo.add(1, cell(1))

    print(repo.find_all_available_cells())
