from abc import ABC, abstractmethod
from .temperature import TempertureSensor
from .water import WaterLevelSensor
from .humidity import HumidityLevelSensor
from output.two_pin.relay import Relay

from output.two_pin.relay import Relay
from output.two_pin.buzzer import Buzzer
from display import LcdDisplay
from messenger_file import MessengerFile


class AbstractFactory(ABC):
    @abstractmethod
    def create_device(self):
        pass


class Factory(AbstractFactory):
    device_types = {
        "TempertureSensor": TempertureSensor,
        "WaterLevelSensor": WaterLevelSensor,
        "HumidityLevelSensor": HumidityLevelSensor,
        "Relay": Relay,
        "Buzzer": Buzzer,
        "LcdDisplay": LcdDisplay,
        "MessengerFile": MessengerFile,
    }

    def create_device(self, sensor_type, **kwargs):
        if sensor_type in Factory.device_types:
            return Factory.device_types[sensor_type](**kwargs)
        raise ValueError(f"Invalid sensor type: {sensor_type}")
