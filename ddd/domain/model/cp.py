# coding=utf-8

from .base.entity import Entity

class hocRepository:
    def find(self, id):
        return Hoc()

class Hoc:
    def get_port_value(self, i):
        return 1


class Cp(object):

    def __init__(self, cp_id, freq_band_ind, freq_dl, freq_ind):
        self._cp_id = cp_id
        self._freq_band_ind = freq_band_ind
        self._freq_dl = freq_dl
        self._freq_ind = freq_ind

    def get_freq_dl(self):
        return self._freq_dl

    def query_freq_ind(self):
        return self._freq_ind

    def _change_hoc_value_max(self):
        pass

    def _change_hoc_value(self, l, v):
        pass

    def get_hoc_port_value(self):
        hoc_info_list = self._get_cp_link_ue_hoc()

        for hocInfo in hoc_info_list:
            hoc_alias = hocInfo[0]
            hoc_channel = hocInfo[1]
            hoc = hocRepository().find(hoc_alias)
            return hoc.get_port_value(hoc_channel)

    def move_to(self, signal_value):
        self._change_hoc_value_max()
        hoc_info_list = self._get_cp_link_ue_hoc()
        self._change_hoc_value(hoc_info_list, signal_value)

    def _get_cp_link_ue_hoc(self):
        return []



Entity.register(Cp)

if __name__ == '__main__':
    print('Subclass:', issubclass(Cp, Entity))
    print('Instance:', isinstance(Cp(1, None), Entity))
