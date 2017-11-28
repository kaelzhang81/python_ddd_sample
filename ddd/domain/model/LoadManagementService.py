class LoadManagementService(object):

    '''
    classdocs
    '''

    @staticmethod
    def _update_loadmanage_attrs(attrs, cellAlias):
        cell = CellRepository().find(cellAlias)
        if cell:
            MoAgent().update_mo(attrs, cell._enodeb.alias, 'LoadManagement', 1)

    @staticmethod
    def config_load_balance_switch(cellAlias, switch):
        return LoadManagementService._update_loadmanage_attrs({'lbSwch':
                                                              switch},
                                                              cellAlias)
