from config import is_arm
from flask import Flask

import logging

if is_arm:
    import RPi.GPIO as GPIO

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)

from repo.temp import TemperatureRepo

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

from route.user import user_route
from route.rfid import rfid_route
from route.user_id import user_id_route
from route.entry import entry_route
from route.temp import temp_route
from route.motor import motor_route

from services import motor_service


if is_arm:
    global motor_running

    motor_service.test_motor()
    motor_running = False


if is_arm:
    from raspi.switch_gpio import SwitchGPIO

    def toggle_motor():
        global motor_running
        if not motor_running:
            threshold = motor_service.get_threshold()
            speed = threshold.speed_pct
            motor_service.set_speed(speed)
            motor_service.forward()
            motor_running = True
        else:
            motor_service.stop()
            motor_running = False

    switch = SwitchGPIO(pin=17, callback=toggle_motor)


app.register_blueprint(user_route)
app.register_blueprint(rfid_route)
app.register_blueprint(user_id_route)
app.register_blueprint(entry_route)
app.register_blueprint(temp_route)
app.register_blueprint(motor_route)
