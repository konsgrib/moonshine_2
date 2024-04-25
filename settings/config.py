config = {
    "min-temperature": 25.2,
    "max-temperature": 28.5,
    "power-on-low-temperature": 30.0,
    "warming-time-minutes": 1,
    "work-time-minutes": 1,
    "work-normal-temperature": 28.2,
    "work-treshold-temperature": 28.5,
    "humidity-treshold": 50,
    "cooler-stop-delay": 1,
    "power_inc_clicks": 3,
    "buzzer": 26,
    "pins": {
        "humidity_1": 14,
        "humidity_2": 15,
        "relay": {
            "power_relay_pin": 19,
            "cooler_relay_pin": 13,
            "valve_1_relay_pin": 6,
            "valve_2_relay_pin": 5,
            "power_inc_pin": 23,
            "power_dec_pin": 24,
        },
        "water_level": {"water_pin_1": 17, "water_pin_2": 27},
        "lcd": {"data_pin": 7, "clk_pin": 8, "reset_pin": 25},
        "buttons": {"cycle_1_pin": 9, "cycle_2_pin": 10, "cycle_3_pin": 11},
    },
    "one-wire": {
        "temperature": {"sensor_1": "28-42f7d445552f", "sensor_2": "28-5be6d445359c"}
    },
}
