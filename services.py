from config import is_arm
from service.motor import MotorService


if is_arm:
    from raspi.lcd_i2c import LcdI2c
    from raspi.rfid_spi import RfidSpi
    from service.temp import TemperatureService, TemperatureMonitor
    from repos import entry_repo, temp_repo

    lcdI2c = LcdI2c()

    rfidSpi = RfidSpi(entry_repo)
    lcdI2c.wait_for_input()

    motor_service = MotorService(in1_pin=23, in2_pin=24, en_pin=25)

    temp_service = TemperatureService(temp_repo)

    temp_monitor = TemperatureMonitor(
        temp_service=temp_service, motor_service=motor_service, lcd=lcdI2c
    )
    temp_monitor.start()
