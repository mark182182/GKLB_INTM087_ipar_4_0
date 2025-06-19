from config import is_arm
from service.motor import MotorService
from globals import motor_state


if is_arm:
    from raspi.lcd_i2c import LcdI2c
    from raspi.rfid_spi import RfidSpi
    from service.temp import TemperatureService, TemperatureMonitor
    from repos import entry_repo, temp_repo
    from raspi.switch_gpio import SwitchGPIO

    lcdI2c = LcdI2c()

    rfidSpi = RfidSpi(entry_repo)

    motor_service = MotorService(in1_pin=23, in2_pin=24, en_pin=25)

    temp_service = TemperatureService(temp_repo)

    temp_monitor = TemperatureMonitor(
        temp_service=temp_service, motor_service=motor_service, lcd=lcdI2c
    )
    temp_monitor.start()

    def toggle_motor():
        if not motor_state.is_running:
            threshold = motor_service.get_threshold()
            speed = threshold.speed_pct
            motor_service.set_speed(speed)
            motor_service.forward()
            motor_state.is_running = True
        else:
            motor_service.stop()
            motor_state.is_running = False

    switch = SwitchGPIO(lcd=lcdI2c, pin=17, callback=toggle_motor)

    motor_service.test_motor()
    motor_state.is_running = False
