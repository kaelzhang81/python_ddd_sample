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
from .base.aggregate_root import AggregateRoot


class Cell(object):

    def __init__(self, cell_alias, cp_list, band_width, freq):
        self._signalRegulator = SignalRegulator(self)
        self._kpiTask = None
        self.functionPolicyDict = {}
        self.switchPolicyDict = {}
        self._id = cell_alias
        self._bandwidthRestrain = BandwidthRestrain(self)
        self._cp_list = cp_list
        self._band_width = band_width
        self._freq = freq


    def role(self, className):
        return Role.convert(self, className)

    def shut_down(self):
        params = {'_iSubNetwork_': self._subNetId, '_iMEID_': self._meId, '_iEutrancellid_': self._id}
        cmd_result = self.dm.query_cmd( params, 'SUCCESS')
        if not cmd_result.result:
            raise Exception("failed to shut down cell")
    
    def start_up(self, query_times=18):
        params = {'_iSubNetwork_': self._subNetId, '_iMEID_': self._meId, '_iEutrancellid_': self._id}
        cmd_result = self.dm.query(params, u'SUCCESS')
        if not cmd_result.result:
            raise Exception("failed to start up cell ")


    def get_rru_alias(self):
        cp = self.cpList[0]
        return cp.rru.boardName

AggregateRoot.register(Cell)

if __name__ == '__main__':
    print('Subclass:', issubclass(Cell, AggregateRoot))
    print('Instance:', isinstance(Cell(1, None), AggregateRoot))
