from abc import ABC, abstractmethod
from .temperature import TempertureSensor
from .water import WaterLevelSensor
from .humidity import HumidityLevelSensor


class AbstractSensorFactory(ABC):
    @abstractmethod
    def create_sensor(self):
        pass


class SensorFactory(AbstractSensorFactory):
    sensor_types = {
        "TempertureSensor": TempertureSensor,
        "WaterLevelSensor": WaterLevelSensor,
        "HumidityLevelSensor": HumidityLevelSensor,
    }

    def create_sensor(self, sensor_type, sensor_id):
        if sensor_type in SensorFactory.sensor_types:
            return SensorFactory.sensor_types[sensor_type](sensor_id)
        raise ValueError(f"Invalid sensor type: {sensor_type}")
