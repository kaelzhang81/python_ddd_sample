class EnodebService(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAl'

    def restore_dv(self, enodebAlias):
        enodeb = EnodebRepository().find(enodebAlias)
        dv = DV(enodeb.enodebInfrastructure, enodeb.radioMode, enodeb.isIpUnit)
        dv.restore_dv()
        logging.debug('restore dv success!')

    def upload_dv_xml(self, enodebAlias,remotePath=None):
        enodeb = EnodebRepository().find(enodebAlias)
        dv = DV(enodeb.enodebInfrastructure, enodeb.radioMode, enodeb.isIpUnit)
        if dv.upload_dv_xml(remotePath):
            logging.debug('upload_dv_xml dv success!')
            return True
        return False

    def open_enodeb_query_cmac_status(self, enodebAlias):
        enodeb = EnodebRepository().find(enodebAlias)
        enodeb.change_enodeb_query_cmac_status('1')

    def close_enodeb_query_cmac_status(self, enodebAlias):
        enodeb = EnodebRepository().find(enodebAlias)
        enodeb.change_enodeb_query_cmac_status('2')

    def check_cell_neighbor_relation_correct(self, serveCellAlias, *neighborCellAliasList):
        serveCell = CellRepository().find(serveCellAlias)
        neighbourCellIds = [int(CellRepository().find(cellAlias).cellId)
                            for cellAlias in neighborCellAliasList]

        enodeb = serveCell.enodeb
        cellIdList = enodeb.get_cell_neightbor_cellId_list(serveCell.cellId)
        if set(neighbourCellIds) ^ set(cellIdList) != set():
            logging.warn('Check Cell(%s) Neighbor Relation Error:\n'
                         '\tExpect Neighbor Cells are: %s\n'
                         '\tReal Neighbor Cells are: %s' %
                         (serveCell.cellId, neighbourCellIds, cellIdList))
            return False
        return True

    def check_neighbor_relation(self, serveCellAlias, *neighborCellAliasList):  # add by wulei
        serveCell = CellRepository().find(serveCellAlias)
        neighbourCellIds = [CellRepository().find(cellAlias).cellId
                            for cellAlias in neighborCellAliasList]

        enodeb = serveCell.enodeb
        enb_para = ['wNCId']
        cellIdList = enodeb.query_neightbor_cellId_list(enb_para)
        if set(neighbourCellIds) ^ set((cellIdList.return_info)[enb_para[0]]) != set():
            logging.warn('Check Cell(%s) Neighbor Relation Error:\n'
                         '\tExpect Neighbor Cells are: %s\n'
                         '\tReal Neighbor Cells are: %s' %
                         (serveCell.cellId, neighbourCellIds, cellIdList.return_info))
            return False
        return True

    def check_used_cell(self, enodebAlias, serveCellAlias):  # add by wulei
        serveCell = CellRepository().find(serveCellAlias)
        enodeb = EnodebRepository().find(enodebAlias)
        enb_para = ['wCId']
        cellIdList = enodeb.get_used_cellId_list(enb_para)
        if set((cellIdList.return_info)[enb_para[0]]) == set():
            return False
        if set(serveCell.cellId) ^ set((cellIdList.return_info)[enb_para[0]]) != set():
            return False
        return True

    def check_used_neighbor(self, enodebAlias, cellAlias):  # add by wulei
        cell = CellRepository().find(cellAlias)
        enodeb = EnodebRepository().find(enodebAlias)
        cellIdList = enodeb.get_cell_neightbor_cellId_list(cell.cellId)
        if set(cellIdList) == set():
            return False
        return True

    def check_mutli_cell_mutual_neighbor_relation_correct(self, *cellAliasList):
        for serveCellAlias in cellAliasList:
            neighborCellAliasList = [cellAlias for cellAlias in
                                     itertools.ifilterfalse(lambda alias: alias == serveCellAlias, cellAliasList)]
            if self.check_cell_neighbor_relation_correct(serveCellAlias, *neighborCellAliasList):
                pass
            else:
                return False
        return True
