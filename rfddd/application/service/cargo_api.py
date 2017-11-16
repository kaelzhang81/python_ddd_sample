# coding=utf-8

class CargoApi(object):
    
    def __init__(self, cargo_service):
        self._cargo_service = cargo_service

    def create_cargo(self, msg):
        self._cargo_service.Create(msg.id, msg.after_days)

    def delay(self, cargo_id, days):
        self._cargo_service.delay(cargoId, days)
