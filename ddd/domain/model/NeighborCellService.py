

class NeighborCellService(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAl'

    @staticmethod
    def check_neighbor_relation(self, serve_cell_alias, neighbor_cell_alias_list):
        serve_cell = CellRepository().find(serve_cell_alias)
        neighbour_cell_ids = [CellRepository().find(cell_alias).id for cell_alias in neighbor_cell_alias_list]

        enb_id = serve_cell.get_enodeb_id()
        enb = EnodebRepository().find(enb_id)
        cell_ids = enb.query_neightbor_cellId_list()
        if set(neighbour_cell_ids) ^ set(cell_ids) != set():
            return False
        return True



class DV:
    pass

class CellRepository:
    def find(self, id):
        return id

class EnodebRepository:
    def find(self, id):
        return id
