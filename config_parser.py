import yaml
from sensor.factory import Factory
from output.two_pin.relay import Relay
from command import (
    OutputDeviceCommand,
    DelayCommand,
    StateUpdateCommand,
    RepeaterCommand,
)


class ConfigParser:
    def __init__(self, filename):
        self.filename = filename
        self.config = self._read_yaml()
        self.relays = self._get_relays()
        self.sensors = self._get_sensors()
        self.programs = self._get_programs()
        self.devices = {**self.sensors, **self.relays}

    def _read_yaml(self):
        with open(self.filename) as f:
            config = yaml.safe_load(f)
        return config

    def _get_relays(self):
        relays = {
            device: Relay(pin)
            for device, pin in self.config["devices"]["relays"].items()
        }
        return relays

    def _get_sensors(self):
        sensors = {}
        for sensor_config in self.config["devices"]["sensors"]:
            sensor_type = sensor_config["type"]
            sensor_name = sensor_config["name"]
            sensor_id = sensor_config["sensor_id"]
            sensors[sensor_name] = Factory().create_sensor(sensor_type, sensor_id)

        return sensors

    def _get_programs(self):
        return self.config["programs"]
