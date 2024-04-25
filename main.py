from yaml_reader import config_parser


from event_loop import EventLoop
from command import (
    OutputDeviceCommand,
    DelayCommand,
    StateUpdateCommand,
    RepeaterCommand,
)

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

config_yaml = "config.yaml"
config, devices = config_parser(config_yaml)
event_loop = EventLoop()


for command_config in config["event_loop_commands"]["cycle_1"]:
    if command_config["type"] == "OutputDeviceCommand":
        device = devices[command_config["device"]]
        command = OutputDeviceCommand(device, command_config["action"])
        event_loop.add(command)
    elif command_config["type"] == "RepeaterCommand":
        repeat_command_config = command_config["command"]
        device = devices[command_config["command"]["device"]]
        repeat_command = OutputDeviceCommand(
            device, repeat_command_config["action"], repeat_command_config.get("time")
        )
        command = RepeaterCommand(repeat_command, command_config["repeat"])
        event_loop.add(command)
    elif command_config["type"] == "DelayCommand":
        delay = command_config["delay"]
        command = DelayCommand(delay)
        event_loop.add(command)
    elif command_config["type"] == "StateUpdateCommand":
        device = devices[command_config["device"]]
        state = command_config["state"]
        command = StateUpdateCommand(device, state)
        event_loop.add(command)

event_loop.run()
GPIO.cleanup()
