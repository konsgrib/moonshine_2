import time
from abc import ABC, abstractmethod

from sensor.humidity import HumidityLevelSensor
from sensor.temperature import TempertureSensor
from sensor.water import WaterLevelSensor
from settings.config import config
from relay.relay import Relay
from logger import logger
import RPi.GPIO as GPIO
from lcd.lcd import Lcd


class AbatractCycle(ABC):
    def __init__(
        self,
        config,
        sensors: dict,
        relays: dict,
        lcd: Lcd,
    ) -> None:
        self.config = config
        self.sensors = sensors
        self.relays = relays
        for key, value in sensors.items():
            setattr(self, key, value)
        for key, value in relays.items():
            setattr(self, key, value)
        self.lcd = lcd
        self.restore_defaults()

    def log_data(self):
        sensor_values = " ".join(
            [
                f"{name}: {sensor.get_value().value}"
                for name, sensor in self.sensors.items()
            ]
        )
        relay_values = " ".join(
            [
                f"{name}: {relay.get_value().value}"
                for name, relay in self.relays.items()
            ]
        )
        logger.info(
            f"Class: {self.__class__.__name__}- Step{self.current_step}: {relay_values} {sensor_values}"
        )

    def collect_data(self):
        data = {name: sensor.get_value().value for name, sensor in self.sensors.items()}
        data.update(
            {name: relay.get_value().value for name, relay in self.relays.items()}
        )
        return data

    def restore_defaults(self) -> None:
        for relay in self.relays.values():
            relay.set_state(0)
