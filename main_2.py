import time
from sensor.factory import SensorFactory
from output.two_pin.relay import Relay
from settings.config import config

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

from event_loop import EventLoop
from command import (
    OutputDeviceCommand,
    DelayCommand,
    StateUpdateCommand,
    RepeaterCommand,
    CounterAVGCommand,
)


min_t = config["min-temperature"]
max_t = config["max-temperature"]
warming_time = config["warming-time-minutes"]
work_start_t = config["power-on-low-temperature"]
cooler_delay = config["cooler-stop-delay"] * 60
work_time = config["work-time-minutes"] * 60
power_dec_pressed_time = 0.152


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


power_relay = Relay(config["pins"]["relay"]["power_relay_pin"])
cooler_relay = Relay(config["pins"]["relay"]["cooler_relay_pin"])
valve_1_relay = Relay(config["pins"]["relay"]["valve_1_relay_pin"])
valve_2_relay = Relay(config["pins"]["relay"]["valve_2_relay_pin"])
power_inc_relay = Relay(config["pins"]["relay"]["power_inc_pin"])
power_dec_relay = Relay(config["pins"]["relay"]["power_dec_pin"])

power_down_command = OutputDeviceCommand(
    power_dec_relay, "onoff", power_dec_pressed_time
)
power_up_command = OutputDeviceCommand(power_inc_relay, "onoff", 0.5)

event_loop = EventLoop()
event_loop.add(OutputDeviceCommand(power_relay, "on"))  # 1
event_loop.add(RepeaterCommand(power_up_command, 50))  # 3
event_loop.add(StateUpdateCommand(temperature_1, min_t))  # 2
event_loop.add(OutputDeviceCommand(cooler_relay, "on"))  # 2
event_loop.add(RepeaterCommand(power_down_command, 30))  # 3
event_loop.add(StateUpdateCommand(temperature_2, work_start_t))  # 4
event_loop.add(DelayCommand(warming_time))  # 4
event_loop.add(OutputDeviceCommand(valve_1_relay, "on"))  # 5
event_loop.add(StateUpdateCommand(water_1, 1))  # 6
event_loop.add(OutputDeviceCommand(valve_1_relay, "off"))  # 7
event_loop.add(OutputDeviceCommand(valve_2_relay, "on"))  # 7
event_loop.add(DelayCommand(work_time))  # 8
event_loop.add(CounterAVGCommand(temperature_2))  # 9
event_loop.add(OutputDeviceCommand(power_relay, "off"))  # 10
event_loop.add(DelayCommand(cooler_delay))  # 10
event_loop.add(OutputDeviceCommand(cooler_relay, "off"))  # 10
event_loop.add(OutputDeviceCommand(valve_2_relay, "off"))  # 10

event_loop.run()
GPIO.cleanup()
