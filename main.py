from sensor.fabric import SensorFactory
from relay.relay import Relay
from settings.config import config
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
factory = SensorFactory()
temperature_1 = factory.create_temperature_sensor( config["one-wire"]["temperature"]["sensor_1"])
temperature_2 = factory.create_temperature_sensor( config["one-wire"]["temperature"]["sensor_2"])
water_1 = factory.create_water_sensor(config["pins"]["water_level"]["water_pin_1"])

power_relay = Relay(config["pins"]["relay"]["power_relay_pin"])
water_relay = Relay(config["pins"]["relay"]["cooler_relay_pin"])


print(config["pins"]["relay"]["power_relay_pin"])
print(temperature_1.get_value())
print(temperature_2.get_value())
print(water_1.get_value())
print(power_relay.set_state(0))
print(power_relay.get_value())

GPIO.cleanup()