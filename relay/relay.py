import RPi.GPIO as GPIO
from .relay_value import RelayValue


class Relay:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        print(f"Relay pin: {pin}")

    def set_state(self, new_state):
        try:
            state = self.get_value()
            if new_state != state:
                GPIO.output(self.pin, new_state)
                state = self.get_value()
                if new_state == state:
                    return RelayValue(200, state, "OK")
                return RelayValue(500, state, "NOK")
            return RelayValue(200, state, "OK")
        except Exception as e:
            state = self.get_value()
            return RelayValue(500, state, str(e))

    def get_value(self):
        return GPIO.input(self.pin)