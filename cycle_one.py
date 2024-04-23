import time

from abstract_cycle import AbatractCycle
from settings.config import config
from logger import logger
import RPi.GPIO as GPIO


class CycleOne(AbatractCycle):

    def step_one(self):
        self.current_step = 1
        self.start_time = time.time()
        self.relay_pwr.set_state(1)
        self.log_data()

    def step_two(self):
        self.current_step = 2
        self.relay_cooler.set_state(1)
        self.log_data()

    def step_tree(self):
        self.current_step = 3
        time_now = time.time()
        self.stop_time = time_now + int(config["cooler-stop-delay"]) * 60
        self.relay_pwr.set_state(0)
        self.log_data()

    def step_four(self):
        self.current_step = 4
        pwr = self.relay_pwr.get_value()
        if pwr.value == 1:
            logger.error("Power isstill ON!!!")
        else:
            self.restore_defaults()
        self.log_data()

    def run(self):
        while True:
            try:
                print(
                    f"{self.relay_pwr.get_value().value} {self.relay_cooler.get_value().value} "
                    f"{self.sensor_w1.get_value().value} {self.sensor_t1.get_value().value} "
                    f"{self.sensor_t2.get_value().value} {self.sensor_h1.get_value().value} {self.current_step}"
                )
                time.sleep(1)
                if self.current_step == 0:
                    self.step_one()
                if (
                    self.current_step == 1
                    and self.sensor_t1.get_value().value >= config["min-temperature"]
                ):
                    self.step_two()
                if (
                    self.current_step == 2
                    and self.sensor_t1.get_value().value >= config["max-temperature"]
                ):
                    self.step_tree()
                if self.current_step == 3 and self.stop_time <= time.time():
                    self.step_four()
                if self.current_step == 4:
                    self.log_data()
                    logger.info("Finished")
                    GPIO.cleanup()
                    break
            except KeyboardInterrupt:
                self.restore_defaults()
                self.lcd.clear()
                self.lcd.display_text("ABORTED".center(16, "*"), 0, 0)
                GPIO.cleanup()
                break
            except Exception as e:
                self.restore_defaults()
                print(str(e))
                GPIO.cleanup()
                break
