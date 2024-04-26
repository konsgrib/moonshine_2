import time
from multiprocessing import Process

from datetime import datetime
from sensor.factory import Factory
from output.two_pin.relay import Relay
from output.two_pin.buzzer import Buzzer
from settings.config import config
from lcd.lcd import Lcd
import RPi.GPIO as GPIO
from cycle_one import CycleOne
from cycle_two import CycleTwo

GPIO.setmode(GPIO.BCM)

factory = Factory()
temperature_1 = factory.create_sensor(
    "TempertureSensor", config["one-wire"]["temperature"]["sensor_1"]
)
temperature_2 = factory.create_sensor(
    "TempertureSensor", config["one-wire"]["temperature"]["sensor_2"]
)
water_1 = factory.create_sensor(
    "WaterLevelSensor", config["pins"]["water_level"]["water_pin_1"]
)

water_2 = factory.create_sensor(
    "WaterLevelSensor", config["pins"]["water_level"]["water_pin_2"]
)

humidity = factory.create_sensor("HumidityLevelSensor", config["pins"]["humidity_1"])

power_relay = Relay(config["pins"]["relay"]["power_relay_pin"])
cooler_relay = Relay(config["pins"]["relay"]["cooler_relay_pin"])
valve_1_relay = Relay(config["pins"]["relay"]["valve_1_relay_pin"])
valve_2_relay = Relay(config["pins"]["relay"]["valve_2_relay_pin"])
power_inc_relay = Relay(config["pins"]["relay"]["power_inc_pin"])
power_dec_relay = Relay(config["pins"]["relay"]["power_dec_pin"])
humidity = factory.create_sensor("HumidityLevelSensor", config["pins"]["humidity_1"])
buzzer = Buzzer(config["buzzer"])
hum_treshold = config["humidity-treshold"]

cycle_1_bt_pin = config["pins"]["buttons"]["cycle_1_pin"]
cycle_2_bt_pin = config["pins"]["buttons"]["cycle_2_pin"]
GPIO.setup(cycle_1_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cycle_2_bt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


lcd = Lcd(
    config["pins"]["lcd"]["data_pin"],
    config["pins"]["lcd"]["clk_pin"],
    config["pins"]["lcd"]["reset_pin"],
)
lcd.clear()
lcd.display_text("S Pm C V1 V2 Pr".ljust(16, " "), 0, 0)

relays = {
    "relay_pwr": power_relay,
    "relay_cooler": cooler_relay,
    "relay_v1": valve_1_relay,
    "relay_v2": valve_2_relay,
    "power_inc_relay": power_inc_relay,
    "power_dec_relay": power_dec_relay,
}
sensors = {
    "sensor_t1": temperature_1,
    "sensor_t2": temperature_2,
    "sensor_w1": water_1,
    "sensor_w2": water_2,
    "sensor_h1": humidity,
}


def cycle_one():
    cycle = CycleOne(
        config,
        sensors,
        relays,
        lcd,
    )
    cycle.run()


def cycle_two():
    cycle = CycleTwo(
        config,
        sensors,
        relays,
        lcd,
    )
    cycle.run()


p1 = Process(target=cycle_one)
p2 = Process(target=cycle_two)


def callback(channel):
    button_state = GPIO.input(channel)
    if not button_state:
        if channel == cycle_1_bt_pin:
            print(p1.is_alive())
            if not p1.is_alive():
                p1.start()
        if channel == cycle_2_bt_pin:
            if not p2.is_alive():
                p2.start()


GPIO.add_event_detect(cycle_1_bt_pin, GPIO.BOTH, callback=callback)
GPIO.add_event_detect(cycle_2_bt_pin, GPIO.BOTH, callback=callback)

while True:
    try:
        time.sleep(1)
        now = datetime.now()
        hum = humidity.get_value().value
        pwr = power_relay.get_value().value
        col = cooler_relay.get_value().value
        v1 = valve_1_relay.get_value().value
        v2 = valve_2_relay.get_value().value
        lcd.display_text(
            f"- {pwr}  {col}  {v1}  {v2}  -".ljust(16, " "),
            0,
            1,
        )
        lcd.display_text(
            f"Temp1:{temperature_1.get_value().value}  HUM".ljust(16, " "), 0, 2
        )
        lcd.display_text(
            f"Temp2:{temperature_2.get_value().value}  {str(humidity.get_value().value)}".ljust(
                16, " "
            ),
            0,
            3,
        )
        if hum >= hum_treshold:
            buzzer.set_state(1)
            power_relay.set_state(0)

    except KeyboardInterrupt:
        print("Interrupted by user")
        buzzer.set_state(0)
        GPIO.cleanup()
        break
    except Exception as e:
        print(str(e))
        buzzer.set_state(1)
        power_relay.set_state(0)
        cooler_relay.set_state(0)
        valve_1_relay.set_state(0)
        valve_2_relay.set_state(0)
        GPIO.cleanup()
        break
