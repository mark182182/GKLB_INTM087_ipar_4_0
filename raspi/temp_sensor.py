# Logic for reading temperature from DS18B20+ sensor
from w1thermsensor import W1ThermSensor


class TempSensor:
    def __init__(self):
        self.sensor = W1ThermSensor()

    def read_temperature(self) -> float:
        return self.sensor.get_temperature()
