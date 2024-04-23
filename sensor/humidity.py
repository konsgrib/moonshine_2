from .abstract_sensor import AbstractSensor, SensorValue


class HumidityLevelSensor(AbstractSensor):
    def __init__(self, pin):
        self.pin = pin

    def get_value(self) -> SensorValue:
        return SensorValue(200, 0, "OK")
