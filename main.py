import time
from sensor.factory import SensorFactory
from relay.relay import Relay
from settings.config import config
from lcd.lcd import Lcd
import RPi.GPIO as GPIO
from cycle_one import CycleOne
from cycle_two import CycleTwo

GPIO.setmode(GPIO.BCM)

factory = SensorFactory()
temperature_1 = factory.create_sensor(
    "TempertureSensor", config["one-wire"]["temperature"]["sensor_1"]
)
temperature_2 = factory.create_sensor(
    "TempertureSensor", config["one-wire"]["temperature"]["sensor_2"]
)
water_1 = factory.create_sensor(
    "WaterLevelSensor", config["pins"]["water_level"]["water_pin_1"]
)

water_2 = factory.create_sensor(
    "WaterLevelSensor", config["pins"]["water_level"]["water_pin_2"]
)

humidity = factory.create_sensor("HumidityLevelSensor", config["pins"]["humidity"])

power_relay = Relay(config["pins"]["relay"]["power_relay_pin"])
cooler_relay = Relay(config["pins"]["relay"]["cooler_relay_pin"])
valve_1_relay = Relay(config["pins"]["relay"]["valve_1_relay_pin"])
valve_2_relay = Relay(config["pins"]["relay"]["valve_2_relay_pin"])
power_inc_relay = Relay(config["pins"]["relay"]["power_inc_pin"])
power_dec_relay = Relay(config["pins"]["relay"]["power_dec_pin"])


lcd = Lcd(
    config["pins"]["lcd"]["data_pin"],
    config["pins"]["lcd"]["clk_pin"],
    config["pins"]["lcd"]["reset_pin"],
)


relays = {
    "relay_pwr": power_relay,
    "relay_cooler": cooler_relay,
    "relay_v1": valve_1_relay,
    "relay_v2": valve_2_relay,
    "power_inc_relay": power_inc_relay,
    "power_dec_relay": power_dec_relay,
}
sensors = {
    "sensor_t1": temperature_1,
    "sensor_t2": temperature_2,
    "sensor_w1": water_1,
    "sensor_w2": water_2,
    "sensor_h1": humidity,
}


cycle = CycleOne(
    config,
    sensors,
    relays,
    lcd,
)
cycle.run()
