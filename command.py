from abc import ABC, abstractmethod
from output.two_pin.abstract_two_pin import AbstractTwoPin
from sensor.abstract_sensor import AbstractSensor
from time import sleep


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class OutputDeviceCommand(Command):
    def __init__(self, device: AbstractTwoPin, action: str, delay: int = 0) -> None:
        self.device = device
        self.action = action
        self.delay = delay

    def execute(self):
        if self.action == "on":
            self.device.set_state(1)
        elif self.action == "off":
            self.device.set_state(0)
        elif self.action == "onoff":
            self.device.set_state(1)
            sleep(self.delay)
            self.device.set_state(0)

        else:
            raise ValueError(f"Incorrect command: {self.action}")


class DelayCommand(Command):
    def __init__(self, time_seconds: int) -> None:
        self.time_seconds = time_seconds

    def execute(self):
        sleep(self.time_seconds)


class StateUpdateCommand(Command):
    def __init__(self, sensor: AbstractSensor, treshold: float):
        self.sensor = sensor
        self.treshold = treshold

    def execute(self):
        while self.sensor.get_value().value < self.treshold:
            print("SENSOR VALUE: ", self.sensor.get_value().value)
            sleep(1)


class RepeaterCommand(Command):
    def __init__(self, cmd: Command, repeat_count: int):
        self.cmd = cmd
        self.repeat_count = repeat_count

    def execute(self):
        for _ in range(self.repeat_count):
            self.cmd.execute()


class BlockingCounterAVGCommand(Command):
    def __init__(self, sensor: AbstractSensor):
        self.sensor = sensor
        self.values = []
        self.average_value = 0.0

    def execute(self):
        for _ in range(10):
            self.values.append(self.sensor.get_value().value)
        self.average_value = sum(self.values) / len(self.values)

        while self.sensor.get_value().value < self.average_value + 0.3:
            print(
                f"SENSOR VALUE: {self.sensor.get_value().value} AVG: {self.average_value}"
            )
            self.values.append(self.sensor.get_value().value)
            self.average_value = sum(self.values) / len(self.values)


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
