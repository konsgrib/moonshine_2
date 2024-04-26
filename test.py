import RPi.GPIO as GPIO

import yaml
from sensor.factory import Factory
from sensor.abstract_sensor import AbstractSensor


GPIO.setmode(GPIO.BCM)



class DeviceBuilder:
    def __init__(self, config_yaml):
        with open(config_yaml, 'r') as file:
            self.config = yaml.safe_load(file)

    def build_device(self, type, **kwargs):
        device_name = kwargs.pop('name', None)
        device = Factory().create_sensor(type, **kwargs)
        globals()[device_name] = device
        return device

    def build_devices(self):
        built_devices = []
        for device in self.config['devices']:
            built_device = self.build_device(**device)
            if built_device is not None:
                built_devices.append(built_device)
        return built_devices



config_yaml = "monitor.yaml"
builder = DeviceBuilder(config_yaml)
devices = builder.build_devices()

for device in devices:
    print(type(device.__Class__))
    


# cooler_relay.set_state(0)
