from abc import ABC, abstractmethod
from output.two_pin.abstract_two_pin import AbstractTwoPin
from sensor.abstract_sensor import AbstractSensor
from time import sleep
from abstract_display import AbstractDisplay
from abstract_messenger import AbstractMessenger


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class RecurringCommand:
    def __init__(self, command, repeat_times=None):
        self.command = command
        self.counter = 0
        self.repeat_times = repeat_times

    def execute(self, event_loop):
        if self.repeat_times:
            self.command.execute(event_loop)
            self.counter += 1
            if self.counter < self.repeat_times:
                event_loop.add(self)
        else:
            self.command.execute(event_loop)
            event_loop.add(self)


class PrintCommand(Command):
    def __init__(self, text):
        self.text = text

    def execute(self, event_loop):
        print(self.text)


class SensorMeasureCommand(Command):
    def __init__(self, sensor: AbstractSensor):
        self.sensor = sensor

    def execute(self, event_loop):
        value = self.sensor.get_value().value
        print(self.sensor.__class__.__name__, value)
        return value


class MultiSensorMeasureCommand(Command):
    def __init__(
        self,
        sensor1: AbstractSensor,
        sensor2: AbstractSensor,
        sensor3: AbstractSensor,
        device1: AbstractTwoPin,
        device2: AbstractTwoPin,
        device3: AbstractTwoPin,
        device4: AbstractTwoPin,
        display: AbstractDisplay,
        messenger: AbstractMessenger,
    ):
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.sensor3 = sensor3
        self.device1 = device1
        self.device2 = device2
        self.device3 = device3
        self.device4 = device4
        self.display = display
        self.messenger = messenger

    def execute(self, event_loop):
        values = {
            "sensor1": self.sensor1.get_value().value,
            "sensor2": self.sensor2.get_value().value,
            "sensor3": self.sensor3.get_value().value,
            "device1": self.device1.get_value().value,
            "device2": self.device2.get_value().value,
            "device3": self.device3.get_value().value,
            "device4": self.device4.get_value().value,
            "message": self.messenger.get_message(),
        }
        self.display.show_data(values)
        print(values)
        return values


class MonitorAlertCommand(Command):
    rules = ["le", "ge"]
     
    def __init__(
        self,
        sensor: AbstractSensor,
        device: AbstractTwoPin,
        theshold: float,
        action: int,
        rule:str
    ):
        self.sensor = sensor
        self.device = device
        self.treshold = theshold
        self.action = action
        if rule in self.rules:
            self.rule = rule
        else:
            raise ValueError(f"Incorrect comparison rule {rule}")

    def execute(self, event_loop):
        if self.rule == "ge":
            if self.sensor.get_value().value >= self.treshold:
                self.device.set_state(self.action)
        elif self.rule == "le":
            if self.sensor.get_value().value <= self.treshold:
                self.device.set_state(self.action)
        
