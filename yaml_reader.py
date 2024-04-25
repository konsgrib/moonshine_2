import yaml
from sensor.factory import SensorFactory
from output.two_pin.relay import Relay


def config_parser(config_yaml):
    with open(config_yaml) as f:
        config = yaml.safe_load(f)

    devices = {
        device: Relay(pin) for device, pin in config["devices"]["relays"].items()
    }
    sensors = {}
    for sensor_config in config["devices"]["sensors"]:
        sensor_type = sensor_config["type"]
        sensor_name = sensor_config["name"]
        sensor_id = sensor_config["sensor_id"]
        sensors[sensor_name] = SensorFactory().create_sensor(sensor_type, sensor_id)

    devices.update(sensors)
    return config, devices
