# coding=utf-8
import unittest

from application.service.cargo_api import CargoApi
from domain.service.cargo_service import CargoService
from application.service.create_cargo_msg import CreateCargoMsg
from domain.model.base.exceptions import CannotBeChangeException
from stub_cargo_provider import StubCargoProvider
from stub_cargo_repository import StubCargoRepository


class CargoTestCase(unittest.TestCase):

    def setUp(self):
        self._cargo_id = 1
        self._after_days = 10
        self._provider = StubCargoProvider()

    @staticmethod
    def create_api(provider):
        repository = StubCargoRepository()
        service = CargoService(repository, provider)
        return CargoApi(service)

    def test_create_cargo(self):
        msg = CreateCargoMsg(1, 10)
        api = CargoTestCase.create_api(self._provider)
        api.create_cargo(msg)
        self.assertEqual(msg._cargo_id, self._provider.cargo_id)
        self.assertEqual(msg.after_days,  self._provider.after_days)

    def test_delay_cargo(self):
        msg = CreateCargoMsg(self._cargo_id, self._after_days)
        api = CargoTestCase.create_api(self._provider)
        api.create_cargo(msg)
        api.delay(self._cargo_id, 2)
        self.assertEqual(self._cargo_id, self._provider.cargo_id)
        self.assertEqual(12,  self._provider.after_days)

    def test_change_entity_id_raise_exception(self):
        repository = StubCargoRepository()
        service = CargoService(repository, self._provider)
        service.create(1, 10)
        cargo = repository.find_by_id(1)
        with self.assertRaises(AttributeError):
            cargo.id = 2

    def test_change_value_object_raise_exception(self):
        repository = StubCargoRepository()
        service = CargoService(repository, self._provider)
        service.create(1, 10)
        cargo = repository.find_by_id(1)
        with self.assertRaises(AttributeError):
            cargo.id = 2

if __name__ == '__main__':
    unittest.main()
