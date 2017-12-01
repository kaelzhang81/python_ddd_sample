import Role
import MocObject
import CellRepository


class LoadManagement(Role):
    def __init__(self, pci, cp_list, band_width, freq):
        self._moc_object = MocObject.Create(pci, cp_list, band_width, freq)

    def config_load_balance_switch(self, switch):
        moc_object = MocObject('LoadManagement', '1', self._moc_object)
        moc_object.set_attrs({'lbSwch': switch})
        return moc_object.update_mo()


class LoadBalanceService(object):
    @staticmethod
    def config_load_balance_switch(cell_alias, switch):
        cell = CellRepository().find(cell_alias)
        return cell.config_load_balance_switch(switch)

class LoadBalanceService(object):
    def __init__(self, cell_alias):
        self._cell = CellRepository().find(cell_alias)
        self._load_management = LoadManagement(self._cell)
        self._cell.role(self._load_management)

    def __del__(self):
        self._cell.unrole(self._load_management)

    def config_load_balance_switch(self, switch):
        return self._cell.config_load_balance_switch(switch)
