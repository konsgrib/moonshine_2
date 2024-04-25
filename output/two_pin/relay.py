import RPi.GPIO as GPIO
from .abstract_two_pin import AbstractTwoPin, TwoPinValue
from logger import logger


class Relay(AbstractTwoPin):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.set_state(0)

    def set_state(self, new_state):
        try:
            state = self.get_value()
            if new_state != state:
                GPIO.output(self.pin, new_state)
                state = self.get_value()
                if new_state == state.value:
                    logger.info(f"RELAY: {self.pin} set to {new_state}")
                    return TwoPinValue(200, state.value, "OK")
                return TwoPinValue(500, state.value, "NOK")
            return TwoPinValue(200, state, "OK")
        except Exception as e:
            logger.error(f"RELAY: {self.pin} failed to set to {new_state}")
            return TwoPinValue(500, state.value, str(e))

    def get_value(self) -> TwoPinValue:
        try:
            state_pin = GPIO.input(self.pin)
            return TwoPinValue(200, state_pin, "OK")
        except Exception as e:
            return TwoPinValue(500, str(e), "NOK")
