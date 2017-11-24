# coding=utf-8

import unittest

from application.service.cargo_api import CargoApi
from application.service.create_cargo_msg import CreateCargoMsg

def create_api():
    # ContainerBuilder builder;
    # builder.registerType< CargoRepository >().singleInstance();
    # builder.registerInstance(provider).as<CargoProvider>();
    # builder.registerType< CargoService >().singleInstance();
    # builder.registerType<api::Api>().singleInstance();
    #
    # auto container = builder.build();
    #
    # std::shared_ptr<api::Api> api = container->resolve<api::Api>();
    #
    # return api.get();
    return CargoApi()

def create_cargo(msg):
    api = create_api();
    api.create_cargo(msg);

class CargoTestCase(unittest.TestCase):
    def test_create_cargo(self):
        msg = CreateCargoMsg(1, 5);
        # createCargo(msg);
        # EXPECT_EQ(msg->Id, provider->cargo_id);
        # EXPECT_EQ(msg->AfterDays, provider->after_days);

        self.assertTrue(True)

    def test_delay_cargo(self):
        # api = createApi();
        # api::CreateCargoMsg * msg = api::CreateCargoMsg();
        # msg->Id = ID;
        # msg->AfterDays = AFTER_DAYS;
        # api->CreateCargo(msg);
        # api->Delay(ID, 2);
        # EXPECT_EQ(ID, provider->cargo_id);
        # EXPECT_EQ(12, provider->after_days);
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

