import time

from abstract_cycle import AbatractCycle
from settings.config import config
from logger import logger
import RPi.GPIO as GPIO


class CycleTwo(AbatractCycle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = 0
        self.stop_time = 0
        self.current_step = 0
        self.warming_start_time = 0
        self.warming_time = 0
        self.working_start_time = 0
        self.working_end_time = 0
        self.t2_temperatures = []
        self.average_temperature = 0.0

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
        self.warming_start_time = time.time()
        for _ in range(config["power_inc_clicks"]):
            self.power_dec_relay.set_state(1)
            time.sleep(0.152)
            self.power_dec_relay.set_state(0)
            time.sleep(1.0)
        self.log_data()

    def step_four(self):
        self.current_step = 4
        self.warming_time = time.time() + config["warming-time-minutes"] * 60
        self.log_data()

    def step_five(self):
        self.current_step = 5
        self.relay_v1.set_state(1)
        self.log_data()

    def step_six(self):
        self.current_step = 6
        self.working_start_time = time.time()
        self.working_end_time = (
            self.working_start_time + config["work-time-minutes"] * 60
        )
        self.log_data()

    def step_seven(self):
        self.current_step = 7
        self.relay_v1.set_state(0)
        self.relay_v2.set_state(1)
        self.log_data()

    def step_eight(self):
        self.current_step = 8
        self.average_temperature = 0.0
        self.log_data()

    def step_nine(self):
        self.current_step = 9
        self.t2_temperatures.append(self.sensor_t2.get_value().value)
        self.average_temperature = sum(self.t2_temperatures) / len(self.t2_temperatures)
        self.log_data()

    def step_ten(self):
        self.current_step = 10
        self.restore_defaults()
        self.log_data()

    def run(self):
        self.power_inc_relay.set_state(1)
        time.sleep(10)
        self.power_inc_relay.set_state(0)
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
                    and self.sensor_t2.get_value().value
                    >= config["power-on-low-temperature"]
                ):
                    self.step_tree()
                if self.current_step == 3:
                    self.step_four()
                if self.current_step == 4 and self.warming_time <= time.time():
                    self.step_five()
                if self.current_step == 5 and self.sensor_w1.get_value().value == 1:
                    self.step_six()
                if self.current_step == 6:
                    self.step_seven()
                if self.current_step == 7 and self.working_end_time <= time.time():
                    self.step_eight()
                if self.current_step == 8:
                    self.step_nine()
                if (
                    self.current_step == 9
                    and self.sensor_t2.get_value().value
                    < self.average_temperature + 0.3
                ):
                    self.step_nine()
                if (
                    self.current_step == 9
                    and self.sensor_t2.get_value().value
                    >= self.average_temperature + 0.3
                ):
                    self.step_ten()
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
