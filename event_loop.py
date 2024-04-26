from collections import deque
from exception_handler import ExceptionHandler
import RPi.GPIO as GPIO

# from command import OutputDeviceCommand
# LoggerCommand, RepeaterCommand, DoubleRepeatedCommand


class EventLoop:
    def __init__(self):
        self.ready = deque()

    def add(self, cmd):
        self.ready.append(cmd)

    def run(self):
        while self.ready:
            cmd = self.ready.popleft()
            try:
                cmd.execute(self)
            except Exception as e:
                ExceptionHandler(cmd, e).handle()
            except KeyboardInterrupt:
                GPIO.cleanup()
                break
