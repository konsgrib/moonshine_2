#!/usr/bin/env python3

import os
import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

import subprocess
import psutil
from settings.config import config
from lcd.lcd import Lcd
from sensor.factory import Factory
from output.two_pin.buzzer import Buzzer
from output.two_pin.relay import Relay

dir_path = os.path.dirname(os.path.realpath(__file__))


GPIO.setmode(GPIO.BCM)
cycle_1_bt_pin = config["pins"]["buttons"]["cycle_1_pin"]
cycle_2_bt_pin = config["pins"]["buttons"]["cycle_2_pin"]

factory = Factory()
humidity = factory.create_sensor("HumidityLevelSensor", config["pins"]["humidity_1"])
temperature_1 = factory.create_sensor(
    "TempertureSensor", config["one-wire"]["temperature"]["sensor_1"]
)
temperature_2 = factory.create_sensor(
    "TempertureSensor", config["one-wire"]["temperature"]["sensor_2"]
)

buzzer = Buzzer(config["buzzer"])

power_relay = Relay(config["pins"]["relay"]["power_relay_pin"])
cooler_relay = Relay(config["pins"]["relay"]["cooler_relay_pin"])
valve_1_relay = Relay(config["pins"]["relay"]["valve_1_relay_pin"])
valve_2_relay = Relay(config["pins"]["relay"]["valve_2_relay_pin"])
hum_treshold = config["humidity-treshold"]


GPIO.setup(cycle_1_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cycle_2_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

LCD_DATA_PIN = config["pins"]["lcd"]["data_pin"]
LCD_CLK_PIN = config["pins"]["lcd"]["clk_pin"]
LCD_RESET_PIN = config["pins"]["lcd"]["reset_pin"]

print(f"Settings: {cycle_1_bt_pin}...")
print(f"Settings: {cycle_2_bt_pin}...")


lcd = Lcd(LCD_DATA_PIN, LCD_CLK_PIN, LCD_RESET_PIN)
lcd.clear()
lcd.display_text("S Pm C V1 V2 Pr".ljust(16, " "), 0, 0)


def is_process_running(process_path):
    for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
        if process_path.lower() in " ".join(proc.info["cmdline"]).lower():
            print(f"The process {process_path} already running")
            return True
    return False


def callback(channel):
    print(channel)


def callback(channel):
    button_state = GPIO.input(channel)
    if button_state == False:
        if channel == cycle_1_bt_pin:
            print("Button 1 Pressed")
            logging.info("Starting procedure 1!")
            if not is_process_running("cycle_1.py"):
                subprocess.run(
                    [
                        "/home/pi/Projects/moonshine/.venv/bin/python",
                        "/home/pi/Projects/moonshine/cycle_1.py",
                    ]
                )
        elif channel == cycle_2_bt_pin:
            print("Button 2 Pressed")
            logging.info("Starting procedure 2!")
            if not is_process_running("cycle_2.py"):
                subprocess.run(
                    [
                        "/home/pi/Projects/moonshine/.venv/bin/python",
                        "/home/pi/Projects/moonshine/cycle_2.py",
                    ]
                )


# "S Pm W V1 V2 Pr"

file_path = os.path.join(dir_path, "w1.txt")


GPIO.add_event_detect(cycle_1_bt_pin, GPIO.BOTH, callback=callback)
GPIO.add_event_detect(cycle_2_bt_pin, GPIO.BOTH, callback=callback)

while True:
    try:
        time.sleep(1)
        now = datetime.now()
        is_cycle_1_running = is_process_running("cycle_1.py")
        is_cycle_2_running = is_process_running("cycle_2.py")
        hum = humidity.get_value().value
        pwr = power_relay.get_value().value
        col = cooler_relay.get_value().value
        v1 = valve_1_relay.get_value().value
        v2 = valve_2_relay.get_value().value
        lcd.display_text(
            f"- {pwr}  {col} " f"{v1}  {v2}  -".ljust(16, " "),
            0,
            1,
        )
        lcd.display_text(
            f"Temp1:{temperature_1.get_value().value}  HUM".ljust(16, " "), 0, 2
        )
        lcd.display_text(
            f"Temp2:{temperature_2.get_value().value}  {str(humidity.get_value().value)}".ljust(
                16, " "
            ),
            0,
            3,
        )
        if hum >= hum_treshold:
            buzzer.set_state(1)
            power_relay.set_state(0)

    except KeyboardInterrupt:
        # lcd.display_text("ABORTED".center(16, "*"), 0, 0)
        print("Interrupted by user")
        buzzer.set_state(0)
        GPIO.cleanup()
        break
