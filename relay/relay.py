import RPi.GPIO as GPIO
from logger import logger


class RelayValue:
    def __init__(self, status_code, value, message):
        self.status_code = status_code
        self.value = value
        self.message = message

    def __repr__(self):
        return str(self.__dict__)


class Relay:
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
                    return RelayValue(200, state.value, "OK")
                return RelayValue(500, state.value, "NOK")
            return RelayValue(200, state, "OK")
        except Exception as e:
            logger.error(f"RELAY: {self.pin} failed to set to {new_state}")
            return RelayValue(500, state.value, str(e))

    def get_value(self) -> RelayValue:
        try:
            state_pin = GPIO.input(self.pin)
            return RelayValue(200, state_pin, "OK")
        except Exception as e:
            return RelayValue(500, str(e), "NOK")
