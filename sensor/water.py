import RPi.GPIO as GPIO
from .abstract_sensor import AbstractSensor, SensorValue


class WaterLevelSensor(AbstractSensor):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_value(self) -> SensorValue:
        try:
            current_value = GPIO.input(self.pin)
            if current_value:
                return SensorValue(200, 0, "OK")
            return SensorValue(200, 1, "OK")
        except Exception as e:
            return SensorValue(500, -1, "NOK")
