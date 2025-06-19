# Logic for handling a micro switch (button) on Raspberry Pi GPIO
import RPi.GPIO as GPIO
from globals import logged_in_user

import logging

from raspi.lcd_i2c import LcdI2c

logger = logging.getLogger(__name__)


class SwitchGPIO:
    def __init__(self, lcd: LcdI2c, pin, callback):
        self.lcd = lcd
        self.pin = pin
        self.callback = callback
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            self.pin, GPIO.FALLING, callback=self._handle_press, bouncetime=300
        )

    def _handle_press(self, channel):
        logger.info(f"Switch pressed on pin {self.pin}")
        if logged_in_user.id is None:
            self.lcd.print_on_lcd("Kerem", "lepjen be!")
        else:
            self.callback()

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)
