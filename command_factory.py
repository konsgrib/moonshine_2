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
    def __init__(self, commands, repeat_times=None):
        self.commands = commands
        self.counter = 0
        self.repeat_times = repeat_times

    def execute(self, event_loop):
        if self.repeat_times:
            for command in self.commands:
                self.command.execute(event_loop)
                self.counter += 1
                if self.counter < self.repeat_times:
                    event_loop.add(self)
        else:
            for command in self.commands:
                command.execute(event_loop)
                event_loop.add(self)


class PrintCommand(Command):
    def __init__(self, device: AbstractMessenger, text: str):
        self.text = text
        self.device = device

    def execute(self, event_loop):
        self.device.send_message(self.text)


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
        treshold: float,
        action: int,
        rule: str,
    ):
        self.sensor = sensor
        self.device = device
        self.treshold = treshold
        self.action = action
        if rule in self.rules:
            self.rule = rule
        else:
            raise ValueError(
                f"Incorrect comparison rule {rule} "
                f"must be in {MonitorAlertCommand.rules}"
            )

    def execute(self, event_loop):
        print("MonitorAlertCommand")
        sleep(1)
        if self.rule == "ge":
            if self.sensor.get_value().value >= self.treshold:
                self.device.set_state(self.action)
                event_loop.clear_until(self)
        elif self.rule == "le":
            if self.sensor.get_value().value < self.treshold:
                self.device.set_state(self.action)



class BlockingCounterAVGCommand(Command):
    def __init__(self, sensor: AbstractSensor):
        self.sensor = sensor
        self.values = []
        self.average_value = 0.0

    def execute(self, event_loop):
        for _ in range(10):
            self.values.append(self.sensor.get_value().value)
        self.average_value = sum(self.values) / len(self.values)

        while self.sensor.get_value().value < self.average_value + 0.3:
            print(
                f"SENSOR VALUE: {self.sensor.get_value().value} AVG: {self.average_value}"
            )
            self.values.append(self.sensor.get_value().value)
            self.average_value = sum(self.values) / len(self.values)


class BlockingStateUpdateCommand(Command):
    def __init__(self, sensor: AbstractSensor, treshold: float):
        self.sensor = sensor
        self.treshold = treshold

    def execute(self, event_loop):
        while self.sensor.get_value().value < self.treshold:
            print("SENSOR VALUE: ", self.sensor.get_value().value)
            sleep(1)


class OutputDeviceCommand(Command):
    def __init__(self, device: AbstractTwoPin, action: str, delay: int = 0) -> None:
        self.device = device
        self.action = action
        self.delay = delay

    def execute(self, event_loop):
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

    def execute(self, event_loop):
        print("DelayCommand")
        sleep(self.time_seconds)


class StopCommand(Command):
    def execute(self, event_loop):
        print("StopCommand")
        raise StopIteration


class ClearQueue(Command):
    def execute(self, event_loop):
        print("ClearQueue")
        event_loop.clear()  


class CommandFactory:
    def create_command(self, type, parameters):
        # print(f"TYPE:{type},  PARAMS: {parameters}")
        if type == "MonitorAlertCommand":
            return MonitorAlertCommand(**parameters)
        elif type == "MultiSensorMeasureCommand":
            return MultiSensorMeasureCommand(**parameters)
        elif type == "RecurringCommand":
            return RecurringCommand(**parameters)
        elif type == "SensorMeasureCommand":
            return SensorMeasureCommand(**parameters)
        elif type == "OutputDeviceCommand":
            return OutputDeviceCommand(**parameters)
        elif type == "DelayCommand":
            return DelayCommand(**parameters)
        elif type == "BlockingStateUpdateCommand":
            return BlockingStateUpdateCommand(**parameters)
        elif type == "PrintCommand":
            return PrintCommand(**parameters)
        elif type == "StopCommand":
            return StopCommand(**parameters)
        elif type == "ClearQueue":
            return ClearQueue(**parameters)
        else:
            raise ValueError("Unknown type", type)
