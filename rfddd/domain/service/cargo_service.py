# coding=utf-8
"""the implement of entity"""


from domain.model import cargo_factory

class CargoService(object):
    """cargo service class
    """
        
    def __init__(self, cargo_repo, cargo_provider):
        self._cargo_repo = cargo_repo
        self._cargo_provider = cargo_provider

    def create(self, cargo_id, days):
        """create cargo"""
        cargo = CargoFactory(cargo_id, days)
        self._cargo_repo.save(cargo);
        self._cargo_provider.confirm(cargo);

    def delay(self, id, days):
        """cargo delay"""
        cargo = self._cargo_repo.find_by_id(id);
        if cargo is not None:
            cargo.Delay(days);
            self._cargo_repo.save(cargo);
            self._cargo_provider.confirm(cargo);
