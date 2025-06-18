# Logic for handling a micro switch (button) on Raspberry Pi GPIO
import RPi.GPIO as GPIO
import time

import logging

logger = logging.getLogger(__name__)


class SwitchGPIO:
    def __init__(self, pin, callback):
        self.pin = pin
        self.callback = callback
        # TODO: this does nothing for some reason, maybe the pin is wrong or the switch is not connected properly
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            self.pin, GPIO.FALLING, callback=self._handle_press, bouncetime=300
        )

    def _handle_press(self, channel):
        logger.info(f"Switch pressed on pin {self.pin}")
        self.callback()

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup(self.pin)
