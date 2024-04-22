from abc import ABC, abstractmethod
from .ds import DsSensor
from .water import WaterLevelSensor
from .humidity import HumidityLevelSensor

class AbstractSensorFactory(ABC):
    @abstractmethod
    def create_temperature_sensor(self):
        pass

    @abstractmethod
    def create_water_sensor(self):
        pass

    @abstractmethod
    def create_humidity_sensor(self):
        pass


class SensorFactory(AbstractSensorFactory):
    def create_temperature_sensor(self, sensor_id):
        return DsSensor(sensor_id)

    def create_water_sensor(self, pin):
        return WaterLevelSensor(pin)

    def create_humidity_sensor(self, pin):
        return HumidityLevelSensor(pin)
