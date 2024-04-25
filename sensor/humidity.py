import Adafruit_DHT
from .abstract_sensor import AbstractSensor, SensorValue


class HumidityLevelSensor(AbstractSensor):
    def __init__(self, pin):
        self.pin = pin

    def get_value(self) -> SensorValue:
        sensor = Adafruit_DHT.AM2302
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        if humidity is not None and temperature is not None:
            return SensorValue(200, round(humidity, 1), "OK")
        return SensorValue(500, -1, "NOK")
