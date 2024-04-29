import RPi.GPIO as GPIO

from config_parser import ProgramBuilder
from event_loop import EventLoop
GPIO.setmode(GPIO.BCM)

config_yaml = "programs.yaml"
program = ProgramBuilder(config_yaml).get_program("cycle1")

el = EventLoop()
for cmd in program:
    el.add(cmd)
el.run()
