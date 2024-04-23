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
        sensor_t1: TempertureSensor,
        sensor_t2: TempertureSensor,
        sensor_w1: WaterLevelSensor,
        sensor_w2: WaterLevelSensor,
        sensor_h1: HumidityLevelSensor,
        relay_pwr: Relay,
        relay_cooler: Relay,
        relay_v1: Relay,
        relay_v2: Relay,
        power_inc_relay: Relay,
        power_dec_relay: Relay,
        lcd: Lcd,
    ) -> None:
        self.config = config
        self.sensor_t1 = sensor_t1
        self.sensor_t2 = sensor_t2
        self.sensor_w1 = sensor_w1
        self.sensor_w2 = sensor_w2
        self.sensor_h1 = sensor_h1
        self.relay_pwr = relay_pwr
        self.relay_cooler = relay_cooler
        self.relay_v1 = relay_v1
        self.relay_v2 = relay_v2
        self.power_inc_relay = power_inc_relay
        self.power_dec_relay = power_dec_relay
        self.lcd = lcd
        self.start_time = 0
        self.stop_time = 0
        self.current_step = 0
        self.restore_defaults()

    def log_data(self):
        logger.info(
            f"Step C1-{self.current_step}: {self.relay_pwr.get_value().value} {self.relay_cooler.get_value().value} "
            f"{self.sensor_w1.get_value().value} {self.sensor_t1.get_value().value} "
            f"{self.sensor_t2.get_value().value} {self.sensor_h1.get_value().value} {self.current_step}",
        )

    def restore_defaults(self) -> None:
        self.relay_pwr.set_state(0)
        self.relay_cooler.set_state(0)
        self.relay_v1.set_state(0)
        self.relay_v2.set_state(0)
        self.power_dec_relay.set_state(0)
        self.power_inc_relay.set_state(1)
        time.sleep(10)
        self.power_inc_relay.set_state(0)

    def step_one(self):
        self.current_step = 1
        self.start_time = time.time()
        self.relay_pwr.set_state(1)
        self.log_data()
