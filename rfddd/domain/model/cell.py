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


class Cell(object):

    def __init__(self, enodeb, PCI, cpList, cellBandWidth, freq, cellAlias, cellId=None):
        self._mocObject = EUtranCell.create_mocobject(
            enodeb, PCI, cpList, cellBandWidth, freq, cellAlias, cellId)
        self._enodeb = enodeb
        self.dm = self._enodeb.ommbDevice.dm
        self._signalRegulator = SignalRegulator(self)
        self._kpiTask = None
        self.functionPolicyDict = {}
        self.switchPolicyDict = {}
        self._alias = cellAlias
        self._historyKpiTask = None
        self._operathd = None
        self._bandwidthRestrain = BandwidthRestrain(self)

    def __getattr__(self, name):
        return getattr(self._mocObject, name)

    def role(self, className):
        return Role.convert(self, className)

    @property
    def enodeb(self):
        return self._enodeb

    @property
    def cellMocObject(self):
        return self._mocObject

    @property
    def alias(self):
        return self._alias

    def setAlias(self, alias):
        self._alias = alias

    def check_cell_state_normal_without_checking_cp(self, query_times=18):
        self.check_state_normal(query_times)

    def check_state_fail(self, query_times=18):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        radioMode = self._enodeb.radioMode
        subDict = {'_iSubNetwork_': subNetId,
                   '_iMEID_': meId, '_iEutrancellid_': self.cellId}
        cmd = self._cmdParser.parse(
            cmdDict=DM_CMD, mainKey='QueryCell', otherKey=radioMode, subDict=subDict)
        for i in range(query_times):
            cmd_result = self.dm.query(cmd, 'Fault')
            if cmd_result.result:
                time.sleep(5)
                cmd_result = self.dm.query(cmd, 'Fault')
                if cmd_result.result:
                    logging.info(
                        "cell status is fault in {0} times".format(i + 1))
                    break
                else:
                    pass
            time.sleep(5)
        else:
            raise Exception("cell status is not fault ")

    def check_state_normal(self, query_times=18):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        radioMode = self._enodeb.radioMode
        subDict = {'_iSubNetwork_': subNetId,
                   '_iMEID_': meId, '_iEutrancellid_': self.cellId}
        cmd = self._cmdParser.parse(
            cmdDict=DM_CMD, mainKey='QueryCell', otherKey=radioMode, subDict=subDict)
        for i in range(query_times):
            cmd_result = self.dm.query(cmd, 'Normal')
            if cmd_result.result:
                if not self._is_sim_env():
                    time.sleep(5)
                cmd_result = self.dm.query(cmd, 'Normal')
                if cmd_result.result:
                    logging.info(
                        "cell status is ok in {0} times".format(i + 1))
                    break
                else:
                    pass
            time.sleep(5)
        else:
            raise Exception("cell status is not ok ")

    def check_state_fault(self, query_times=18):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        radioMode = self._enodeb.radioMode
        subDict = {'_iSubNetwork_': subNetId,
                   '_iMEID_': meId, '_iEutrancellid_': self.cellId}
        cmd = self._cmdParser.parse(
            cmdDict=DM_CMD, mainKey='QueryCell', otherKey=radioMode, subDict=subDict)
        for i in range(query_times):
            cmd_result = self.dm.query(cmd, 'Outage')
            logging.warn("111cmd_result:%s,%s" %
                         (cmd_result, cmd_result.result))
            if cmd_result.result:
                time.sleep(5)
                cmd_result = self.dm.query(cmd, 'Outage')
                logging.warn("222cmd_result:%s,%s" %
                             (cmd_result, cmd_result.result))
                if cmd_result.result:
                    logging.info(
                        "cell status is outage in {0} times".format(i + 1))
                    break
                else:
                    pass
            time.sleep(5)
        else:
            raise Exception("cell status is not Outage ")

    def shut_down_cell_immediate(self):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        radioMode = self._enodeb.radioMode
        subDict = {'_iSubNetwork_': subNetId,
                   '_iMEID_': meId, '_iEutrancellid_': self.cellId}
        cmd = self._cmdParser.parse(cmdDict=DM_CMD, mainKey='ShutdownCellImmediate', otherKey=radioMode,
                                    subDict=subDict)
        for i in range(0, 3):
            cmd_result = self.dm.query(cmd, 'SUCCESS')
            if cmd_result.result:
                logging.info(
                    "shutdown cell immediate is ok in {0} times".format(i + 1))
                break
            else:
                time.sleep(10)
        else:
            raise Exception("shut down cell immediate is not ok ")
    
    def start_up_cell(self, query_times=18):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        radioMode = self._enodeb.radioMode
        subDict = {'_iSubNetwork_': subNetId,
                   '_iMEID_': meId, '_iEutrancellid_': self.cellId}
        cmd = self._cmdParser.parse(
            cmdDict=DM_CMD, mainKey='StartupCell', otherKey=radioMode, subDict=subDict)
        cmd_result = self.dm.query(cmd, u'SUCCESS|成功')
        if cmd_result.result:
            logging.info("start up cell is ok ")
        else:
            raise Exception("start up cell is not ok ")

    def _get_phychannel_attrs(self, bandWidthId):
        # 閺屻儳婀匬rach鐞涖劋鑵戦惃鍒緍achConfigIndex閸欏倹锟�?闂囷拷顪呴懢宄板絿srsBWCfg)
        queryInfo = MoAgent().query_mo(
            ['prachConfigIndex'], self.alias, 'Prach', 1)
        prachConfigIndex = queryInfo['prachConfigIndex'][0]

        prachConfigIndexMin = PRACHCONFIG_SRSBCFG_INDEX['min']
        prachConfigIndexMax = PRACHCONFIG_SRSBCFG_INDEX['max']
        if prachConfigIndexMin < prachConfigIndex < prachConfigIndexMax:
            prachConfigIndexFalg = 1
        else:
            prachConfigIndexFalg = 0
        attr = ['puschhoppingOffset', 'srsEnable']
        queryInfo = MoAgent().query_mo(attr, self.alias, 'PhyChannel', 1)
        queryPuschhoppingOffset = queryInfo['puschhoppingOffset'][0]
        querySrsEnable = queryInfo['srsEnable'][0]
        if (querySrsEnable == '1'):
            srsbcfgIndexDict = CmdParser().parse(SRSBCFG_INDEX, mainKey=self._enodeb.radioMode, version=self._enodeb.version)
            updateSrsBWCfg = srsbcfgIndexDict['%s%s%s' % (querySrsEnable, prachConfigIndexFalg, bandWidthId)]
        else:
            updateSrsBWCfg = 0
        puschhoppingOffset = PUSCHHOPOFFSET_BANDWIDTHID_INDEX[
            self._enodeb.radioMode][bandWidthId]
        isModPuschhopOff = False
        if queryPuschhoppingOffset > puschhoppingOffset:
            isModPuschhopOff = True

        # 娣囶喗鏁糚hyChannel鐞涖劋鑵憇rsBWCfg閸欏倹鏆熼敓锟�?
        attrs = {
            'srsBWCfg': updateSrsBWCfg,
        }
        if isModPuschhopOff:
            attrs.update({
                'puschhoppingOffset': puschhoppingOffset
            })

        return attrs

    def update_bandwidth(self, bandWidth):
        if self._is_sim_env():
            return
        bandWidthId = LTE_BANDWIDTHIND[bandWidth]
        # 娣囶喗鏁肩敮锕�顔旂痪锔芥将,闁氨鐓＄敮锕�顔旈惄绋垮彠閻ㄥ嫯顬佺�电喕锟�?濡拷鐓￠崥鍕殰閺勵垰鎯佹潻婵嗗冀缁撅拷
        self._bandwidthRestrain.setBandwidth(bandWidthId)

        maxUeRbNumDl, maxUeRbNumUl = BANDWIDTHID_MAP[bandWidthId][0:2]
        if self._enodeb.radioMode == 'FDD':
            attrs = {
                'maxUeRbNumUl': maxUeRbNumUl, 'maxUeRbNumDl': maxUeRbNumDl,
                'bandWidthUl': bandWidthId, 'bandWidthDl': bandWidthId
            }
        else:
            attrs = {
                'maxUeRbNumUl': maxUeRbNumUl, 'maxUeRbNumDl': maxUeRbNumDl,
                'bandWidth': bandWidthId
            }
        MoAgent().update_mo(attrs, self.alias)
        self.cellMocObject._cellBandWidth = bandWidth
        return True

    def get_cm(self):
        ommb = self._enodeb.ommbDevice
        return ommb.cm

    def tdd_subframe_config(self, sf_assignment):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        radioMode = self._enodeb.radioMode

        if radioMode != 'TDD':
            logging.info("tdd_cell_subframe_config : radiomode should be TDD ")
            return
        moc = self._cmdParser.parse(
            cmdDict=CM_MOC, mainKey='EUtranCell', otherKey=radioMode)
        subDict = {'_iSubNetId_': subNetId, '_iMEId_': meId,
                   '_iENBFuncId_': meId, '_iEUtranCell_': self.cellId}
        moi = self._cmdParser.parse(
            cmdDict=CM_MOI, mainKey='EUtranCell', otherKey=radioMode, subDict=subDict)
        attr = 'sfAssignment={0}'.format(sf_assignment)
        cm = self.get_cm()
        if not cm.update(moc, moi, attr).result:
            raise Exception('Update Baseband Resource Error!')

    def equal(self, idList):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        selfIdList = [subNetId, meId, self.cellId]

        for i in range(len(selfIdList)):
            if str(selfIdList[i]) != str(idList[i]):
                return False

        return True

    def update_config(self, attrs):
        MoAgent().update_mo(attrs, self.alias)

    def update_power_control_ul_params(self, attrs):
        MoAgent().update_mo(attrs, self.alias, 'PowerControlUL', 1)

    def get_bandwidth(self):
        if self._enodeb.radioMode == 'FDD':
            attrs = ['bandWidthDl', 'bandWidthUl']
            queryResult = MoAgent().query_mo_all(attrs, self._alias)
            bandWidthUl = queryResult['bandWidthUl'][0]
            bandWidthDl = queryResult['bandWidthDl'][0]
        else:
            attr = ['bandWidth']
            bandWidth = MoAgent().query_mo(attr, self.alias)
            bandWidthUl = bandWidth['bandWidth'][0]
            bandWidthDl = bandWidth['bandWidth'][0]
        bandWidthDict = {0: '1.4m', 1: '3m', 2: '5m',
                         3: '10m', 4: '15m', 5: '20m'}
        queryBandWidth = {'bandWidthDl': bandWidthDict[int(bandWidthDl)],
                          'bandWidthUl': bandWidthDict[int(bandWidthUl)]}
        return queryBandWidth

    def get_sf_assignment(self):
        if self._enodeb.radioMode == 'TDD':
            attr = ['sfAssignment']
            sfAssignment = MoAgent().query_mo(
                attr, self.alias)['sfAssignment'][0]
            return sfAssignment
        else:
            logging.warn("FDD mode not exist subframe assignmen")
            return None

    def get_special_sf_patterns(self):
        if self._enodeb.radioMode == 'TDD':
            attr = ['specialSfPatterns']
            specialSFPatterns = MoAgent().query_mo(
                attr, self.alias)['specialSfPatterns'][0]
            return specialSFPatterns
        else:
            logging.warn("FDD mode not exist special subframe patterns")
            return None

    def get_trans_mode(self):
        attr = ['flagSwiMode']
        transMode = MoAgent().query_mo(attr, self.alias)['flagSwiMode'][0]
        return transMode

    def get_cfi(self):
        attr = ['cFI']
        cfi = MoAgent().query_mo(attr, self.alias)['cFI'][0]
        return cfi

    def get_sample_rate_cfg(self):
        attr = ['sampleRateCfg']
        sampleRateCfg = MoAgent().query_mo(attr, self.alias)['sampleRateCfg'][0]
        return sampleRateCfg

    def get_pci(self):
        attr = ['pci']
        pci = MoAgent().query_mo(attr, self.alias)['pci'][0]
        if pci is not None:
            self._mocObject._PCI = pci
        return pci

    def get_cell_id(self):
        attr = ['cellLocalId']
        cellId = MoAgent().query_mo(attr, self.alias)['cellLocalId'][0]
        return cellId

    def get_gid_list(self):
        eNodeB_device_obj = self.enodeb.enodebInfrastructure
        return eNodeB_device_obj.get_gid_list(self.localId)

    def get_gid_by_crnti(self, crnti):
        eNodeB_device_obj = self.enodeb.enodebInfrastructure
        return eNodeB_device_obj.get_gid_by_crnti(crnti)

    def get_downlink_frequency(self):
        radioMode = self.enodeb.radioMode
        if radioMode == 'FDD':
            attr = ['earfcnDl']
            frequency = MoAgent().query_mo(attr, self.alias)['earfcnDl'][0]
        else:
            attr = ['earfcn']
            frequency = MoAgent().query_mo(attr, self.alias)['earfcn'][0]
        return frequency

    def get_earcfn(self):
        radioMode = self.enodeb.radioMode
        if radioMode == 'FDD':
            freqAttr = 'earfcnDl'
            bandIndex = 'freqBandInd'
            freqIndex = FDD_FREQ_INDEX
        else:
            freqAttr = 'earfcn'
            bandIndex = 'bandIndicator'
            freqIndex = TDD_FREQ_INDEX
        attrList = [freqAttr, bandIndex]
        attrValueDict = MoAgent().query_mo(attrList, self.alias)
        frequency = attrValueDict[freqAttr][0]
        freqBandInd = attrValueDict[bandIndex][0]
        logging.info("cell working frequency is {0}, freqBandInd is {1}".format(
            frequency, freqBandInd))
        minFreq = freqIndex[int(freqBandInd)][0]
        offset = freqIndex[int(freqBandInd)][2]
        earcfn = int(10 * (float(frequency) - float(minFreq)) + float(offset))
        logging.info("cell earcfn is {0}".format(earcfn))
        return earcfn

    def set_downlink_frequency(self, earcfn):
        radioMode = self.enodeb.radioMode
        if radioMode == 'FDD':
            freqAttr = 'earfcnDl'
        else:
            freqAttr = 'earfcn'
        MoAgent().update_mo({freqAttr: str(earcfn)},
                            self.alias)

    def update_cellLocalId(self, cellID):
        attrs = {'cellLocalId': cellID}
        self._mocObject._cellLocalId = cellID
        self.update_config(attrs)

    def update_pci(self, pci):
        attrs = {'pci': pci}
        self.update_config(attrs)
        self._mocObject._PCI = pci

    def update_cell_sf(self, subframe):
        attrs = {'sfAssignment': subframe}
        if self._enodeb.radioMode == 'FDD':
            logging.error("update_cell_sf: Not Support For FDD!")
            return
        self.update_config(attrs)

    def update_cell_ssf(self, specialSubframe):
        attrs = {'specialSfPatterns': specialSubframe}
        if self._enodeb.radioMode == 'FDD':
            logging.error("update_cell_ssf: Not Support For FDD!")
            return
        self.update_config(attrs)

    def update_cell_params_by_tablename(self, tablename, attrs):
        MoAgent().update_mo(attrs, self.alias, tablename, '1')

    def check_cell_state(self):
        queryCellStateCmd = self._assemble_query_cmd('QueryCell')
        cmd_result = self.dm.query(queryCellStateCmd, 'Normal')
        return cmd_result.result

    def get_cell_state_multi_times(self, status='Normal', times=5, timeout=60):
        times, timeout = int(times), int(timeout)
        for i in range(times):
            queryCellStateCmd = self._assemble_query_cmd('QueryCell')
            cmd_result = self.dm.query(queryCellStateCmd, status, timeout)
            logging.info(
                'cmd_result.result:{0},{1}'.format('QueryCell:', cmd_result.result))
            if cmd_result.result:
                return True
            else:
                continue
        return False

    def check_state_invariant(self, state, costTimeSecs=60):
        if self._is_sim_env():
            return

        queryCellStateCmd = self._assemble_query_cmd('QueryCell')
        endTimeSecs = int(time.time()) + costTimeSecs
        for _ in range(1, 10000):
            if int(time.time()) - endTimeSecs >= 0:
                break
            cmdResult = self.dm.query(queryCellStateCmd, 'Rows')
            lowTempState = string.lower(state)
            lowTempCmdReturn = string.lower(cmdResult.return_string)
            if re.search(lowTempState, lowTempCmdReturn) is None:
                raise Exception("cell state change process wrong")
            time.sleep(5)

    def check_state_change_process(self, stateList):
        if self._is_sim_env():
            return
        queryCellStateCmd = self._assemble_query_cmd('QueryCell')
        costTimeSecs = 300
        endTimeSecs = int(time.time()) + costTimeSecs
        for _ in range(1, 10000):
            cmdResult = self.dm.query(queryCellStateCmd, 'Rows')
            lowTempState = string.lower(stateList[0])
            lowTempCmdReturn = string.lower(cmdResult.return_string)
            if re.search(lowTempState, lowTempCmdReturn):
                stateList.remove(stateList[0])
            if int(time.time()) - endTimeSecs >= 0 or 0 == len(stateList):
                break
            time.sleep(5)

        if len(stateList) > 0:
            raise Exception("cell state change process wrong")

    def _assemble_query_cmd(self, queryType):
        subNetId = self._enodeb.subNetId
        meId = self._enodeb.neId
        radioMode = self._enodeb.radioMode
        subDict = {'_iSubNetwork_': subNetId, '_iMEID_': meId,
                   '_iEutrancellid_': self.cellId}
        cmd = self._cmdParser.parse(cmdDict=DM_CMD, mainKey=queryType,
                                    otherKey=radioMode, subDict=subDict)
        return cmd

    def get_rru_alias(self):
        cp = self.cpList[0]
        return cp.rru.boardName

    def update_operator(self, operator_list):
        plmn_list = [{'Plmn': 1, 'Operator': operator._operatroId}
                     for operator in operator_list]
        attrs = {'refPlmn': plmn_list}
        MoAgent().update_mo(attrs, self.alias)

    def update_mbms_svc_area_id_list(self, ids):
        if isinstance(ids, list):
            id_str_list = []
            for item in ids:
                id_str_list.append(item)
            ids = ';'.join(id_str_list)
        attrs = {'mbmsSvcAreaIDList': ids}
        MoAgent().update_mo(attrs, self.alias)

    def get_cp_trans_pwr_related_args(self, bandwidthId):
        bandWidthRb = BANDWIDTHID_MAP[bandwidthId][0]
        queryCellAttrs = MoAgent().query_mo(['cellRSPortNum', 'pb'], self.alias)
        cellRSPortNumIndex = queryCellAttrs['cellRSPortNum'][0]
        cellRSPortNum = CELLRSPORTNUM_MAP[cellRSPortNumIndex]
        pb = queryCellAttrs['pb'][0]
        pb_pa = CmdParser().parse(CPTRANSPWRCALFORMULA_PB_PA, mainKey=pb, otherKey=cellRSPortNum, version=self._enodeb.version)
        queryPaForDTCH = MoAgent().query_mo(['paForDTCH'], self.alias, 'PowerControlDL', 1)['paForDTCH'][0]
        pa = CmdParser().parse(PAFORDTCH_VAL, mainKey=queryPaForDTCH, version=self._enodeb.version)
        return cellRSPortNum, bandWidthRb, pa, pb_pa

    def _is_sim_env(self):
        return '127.0.0.1' == self.enodeb.ommbDevice._ip

if __name__ == "__main__":
    print string.lower('THasDF')
