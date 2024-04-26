import yaml
from sensor.factory import Factory
from output.two_pin.relay import Relay
from command import (
    OutputDeviceCommand,
    DelayCommand,
    StateUpdateCommand,
    RepeaterCommand,
)


def config_parser(config_yaml):
    with open(config_yaml) as f:
        config = yaml.safe_load(f)

    devices = {
        device: Relay(pin) for device, pin in config["devices"]["relays"].items()
    }
    sensors = {}
    for sensor_config in config["devices"]["sensors"]:
        sensor_type = sensor_config["type"]
        sensor_name = sensor_config["name"]
        sensor_id = sensor_config["sensor_id"]
        sensors[sensor_name] = Factory().create_sensor(sensor_type, sensor_id)

    devices.update(sensors)
    return config, devices


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
