# coding=utf-8
from testlib.domain.model.cell import ECellEquipmentFunction


class Cp(object):

    def __init__(self, enodeb, bbBoard, cpId, rruInfoList, freqDl, freqInd):
        self._cpId = None
        self.freqBandInd = None
        self._feqDl = freqDl
        self._freqInd = freqInd
        self._mocObject = ECellEquipmentFunction.create_mocobject(
            enodeb, bbBoard, cpId, rruInfoList, 
        )

    def __getattr__(self, name):
        return getattr(self._mocObject, name)

    def get_attrs(self):
        _attrs = self._mocObject._create_attrs()
        return _attrs
 
    @property
    def cpid(self):
        return self._cpId

    def get_freqDl(self):
        return self._feqDl

    def query_rru_freqband_Ind(self, freqDl, cellBand):
        return self._freqInd
