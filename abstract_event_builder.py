from abc import ABC, abstractmethod
from command import (
    OutputDeviceCommand,
    DelayCommand,
    StateUpdateCommand,
    RepeaterCommand,
)


class AbstractEventFactory(ABC):
    @abstractmethod
    def create_event(self):
        pass


class EventFactory(AbstractEventFactory):
    event_types = {
        "OutputDeviceCommand": OutputDeviceCommand,
        "RepeaterCommand": RepeaterCommand,
        "DelayCommand": DelayCommand,
        "StateUpdateCommand": StateUpdateCommand,
    }

    def create_event(self, event_type, *args, **kwargs):
        if event_type in EventFactory.event_types:
            return EventFactory.event_types[event_type](*args, **kwargs)
        raise ValueError(f"Invalid event type: {event_type}")
