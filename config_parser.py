from abc import ABC, abstractmethod
import yaml
from sensor.factory import Factory
from command_factory import CommandFactory

from logger import logger


class AbstractConfigReader(ABC):
    @abstractmethod
    def get_config_data(self):
        pass


class ConfigYamlReader(AbstractConfigReader):

    def get_config_data(self, config_yaml):
        try:
            with open(config_yaml, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error("Error reading config file: " + str(e))
        return {}


class DeviceBuilder:
    def __init__(self, config_file):
        self.config_reader = ConfigYamlReader()
        self.config_data = self.config_reader.get_config_data(config_file)

    def build_device(self, type, **kwargs):
        device_name = kwargs.pop("name", None)
        device = Factory().create_device(type, **kwargs)
        globals()[device_name] = device
        return device

    def build_devices(self):
        built_devices = {}
        for device in self.config_data["devices"]:
            built_device = self.build_device(**device)
            if built_device is not None:
                built_devices[device["name"]] = built_device
        return built_devices


class ProgramBuilder:
    def __init__(self, config_file) -> None:
        self.config_file = config_file
        self.command_factory = CommandFactory()
        self.device_builder = DeviceBuilder(self.config_file)
        self.config_reader = ConfigYamlReader()
        self.devices = self.device_builder.build_devices()

    def build_parameters(self, cmd: dict):
        parameters = {
            key: self.devices[value] if value in self.devices else value
            for key, value in cmd.items()
            if key not in ["command", "type", "commands"]
        }
        return parameters

    def get_program(self, program_name: str):
        config_data = self.config_reader.get_config_data(self.config_file)
        program_data = config_data["programms"][program_name]
        if not program_data:
            return {}
        commands = []
        for command in program_data:
            command_type = command["type"]
            if command_type == "RecurringCommand":
                subcommands = [self.command_factory.create_command(cmd["type"], self.build_parameters(cmd)) for cmd in command["commands"]]
                parameters = self.build_parameters(command)
                parameters["commands"] = subcommands
                command = self.command_factory.create_command(command_type, parameters)
            else:
                parameters = self.build_parameters(command)
                command = self.command_factory.create_command(command_type, parameters)
            commands.append(command)
        return commands


