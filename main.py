import RPi.GPIO as GPIO

from config_parser import ProgramBuilder
from event_loop import EventLoop
GPIO.setmode(GPIO.BCM)

config_yaml = "monitor.yaml"
program = ProgramBuilder(config_yaml).get_program("test")

el = EventLoop()
for cmd in program:
    el.add(cmd)
el.run()
GPIO.cleanup()
