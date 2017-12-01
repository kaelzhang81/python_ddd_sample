# coding=utf-8

import logging
import time
import re
import string
from testlib.domain.model.MmlCmd import *
from testlib.domain.model.cell import EUtranCell
from testlib.infrastructure.utility.CmdParser import CmdParser
from testlib.infrastructure.utility.Role import Role
from testlib.domain.model.cell.SignalRegulator import SignalRegulator
from testlib.infrastructure.utility.envpara.EnvPara import EnvPara
from testlib.infrastructure.utility.moctree.model.MoAgent import MoAgent
from testlib.domain.model.cell.BandwidthRestrain import BandwidthRestrain
import FunctionPolicy
import SwitchPolicy
import LoadManagement

from .base.aggregate_root import AggregateRoot


class Cell(object):

    def __init__(self, cell_alias, pci, cp_list, band_width, freq, dm):
        self._kpi_task = None
        self._id = cell_alias
        self._cp_list = cp_list
        self._pci = pci
        self._band_width = band_width
        self._freq = freq
        self._dm = dm
        self.switch_policy = SwitchPolicy()
        self.function_policy = FunctionPolicy()
        self._bandwidth_restrain = BandwidthRestrain(band_width)
        self._signal_regulator = SignalRegulator(cp_list)
        self._load_management = LoadManagement(pci, cp_list, band_width, freq)

    def role(self, className):
        return Role.convert(self, className)

    def shut_down(self):
        params = {'_iSubNetwork_': self._subNetId, '_iMEID_': self._meId, '_iEutrancellid_': self._id}
        cmd_result = self._dm.query_cmd( params, 'SUCCESS')
        if not cmd_result.result:
            raise Exception("failed to shut down cell")
    
    def start_up(self, query_times=18):
        params = {'_iSubNetwork_': self._subNetId, '_iMEID_': self._meId, '_iEutrancellid_': self._id}
        cmd_result = self._dm.query(params, u'SUCCESS')
        if not cmd_result.result:
            raise Exception("failed to start up cell ")

    def move_to_near_far(self, signal_value):
        cp = self._cp_list[0]
        return cp.move_to(signal_value)

AggregateRoot.register(Cell)

if __name__ == '__main__':
    print('Subclass:', issubclass(Cell, AggregateRoot))
    print('Instance:', isinstance(Cell(1, [], 0, 0, None), AggregateRoot))
