from .abstract_sensor import AbstractSensor, SensorValue


class WaterLevelSensor(AbstractSensor):
    def __init__(self, pin):
        self.pin = pin

    def get_value(self) -> SensorValue:
        return SensorValue(200, 1, "OK")
