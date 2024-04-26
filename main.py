import RPi.GPIO as GPIO

from yaml_reader import config_parser, create_events_queue
from event_loop import EventLoop


GPIO.setmode(GPIO.BCM)

config_yaml = "config.yaml"
config, devices = config_parser(config_yaml)


queue_cmd = create_events_queue("cycle_1")
event_loop = EventLoop()
for command in queue_cmd:
    event_loop.add(command)
event_loop.run()
GPIO.cleanup()
