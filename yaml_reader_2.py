import yaml
from sensor.factory import Factory
from output.two_pin.relay import Relay
from command import (
    OutputDeviceCommand,
    DelayCommand,
    StateUpdateCommand,
    RepeaterCommand,
)


def read_yaml_config(config_yaml):
    with open(config_yaml) as f:
        config = yaml.safe_load(f)
    return config

def get_devices(config):
    devices =config["devices"]
    return devices



def get_programs(config): 
    programs = {program: details for program, details in config["programs"].items()}
    return programs



def create_events_queue(program, config, devices):
    events_queue = []
    for command_config in config["programs"][program]:
        if command_config["type"] == "OutputDeviceCommand":
            device = devices[command_config["device"]]
            command = OutputDeviceCommand(device, command_config["action"])
            events_queue.append(command)
        elif command_config["type"] == "RepeaterCommand":
            repeat_command_config = command_config["command"]
            device = devices[command_config["command"]["device"]]
            repeat_command = OutputDeviceCommand(
                device,
                repeat_command_config["action"],
                repeat_command_config.get("time"),
            )
            command = RepeaterCommand(repeat_command, command_config["repeat"])
            events_queue.append(command)
        elif command_config["type"] == "DelayCommand":
            delay = command_config["delay"]
            command = DelayCommand(delay)
            events_queue.append(command)
        elif command_config["type"] == "StateUpdateCommand":
            device = devices[command_config["device"]]
            state = command_config["state"]
            command = StateUpdateCommand(device, state)
            events_queue.append(command)
    return events_queue
