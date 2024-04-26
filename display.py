from abstract_display import AbstractDisplay
from lcd.lcd import Lcd


class LcdDisplay(AbstractDisplay):
    def __init__(self, data_pin, clk_pin, reset_pin):
        self.data_pin = data_pin
        self.clk_pin = clk_pin
        self.reset_pin = reset_pin
        self.display = Lcd(self.data_pin, self.clk_pin, self.reset_pin)

    def show_data(self, data):
        self.display.clear()
        self.display.display_text("St Pm C V1 V2 Pr".ljust(16, " "), 0, 0)
        self.display.display_text(
            (
                f" {data['message'].split(':')[0]}  "
                f"{data['device1']} "
                f"{data['device2']}  "
                f"{data['device3']}  "
                f"{data['device4']} "
                f" {data['message'].split(':')[1]}"
            ).ljust(16, " "),
            0,
            1,
        )
        self.display.display_text(f"Temp1:{data['sensor1']}  HUM".ljust(16, " "), 0, 2)
        self.display.display_text(
            f"Temp2:{data['sensor2']}  {data['sensor3']}".ljust(16, " "), 0, 3
        )
