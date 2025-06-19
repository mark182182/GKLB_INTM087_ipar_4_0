from config import is_arm
from flask import Flask

from db.db import Database

import logging

if is_arm:
    import RPi.GPIO as GPIO

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)

from models.motor import MotorThreshold
from repo.entry import EntryRepository
from repo.user_id import UserIdentifierRepository
from repo.user import UserRepository
from repo.rfid import RfidRepository
from repo.motor_event import MotorEventRepo
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

db = Database()
db.setup()

if is_arm:
    from raspi.lcd_i2c import LcdI2c

    lcdI2c = LcdI2c()


userRepo = UserRepository(db)
rfidRepo = RfidRepository(db)
userIdRepo = UserIdentifierRepository(db, rfidRepo)
entryRepo = EntryRepository(db, userIdRepo)
motor_event_repo = MotorEventRepo(db)

if is_arm:
    from raspi.rfid_spi import RfidSpi

    rfidSpi = RfidSpi(entryRepo)
    lcdI2c.wait_for_input()

from route.user import user_route
from route.rfid import rfid_route
from route.user_id import user_id_route
from route.entry import entry_route
from route.temp import temp_route
from route.motor import motor_route

from globals import motor_service


if is_arm:
    from service.temp import TemperatureService, TemperatureMonitor
    from repo.temp import TemperatureRepo

    temp_repo = TemperatureRepo(db)
    temp_service = TemperatureService(temp_repo)

    temp_monitor = TemperatureMonitor(temp_service, lcdI2c)
    temp_monitor.start()

    global motor_running

    motor_running = False
    motor_service.test_motor()

    motor_running = True


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

    # TODO: does not work for some reason
    switch = SwitchGPIO(pin=17, callback=toggle_motor)


app.register_blueprint(user_route)
app.register_blueprint(rfid_route)
app.register_blueprint(user_id_route)
app.register_blueprint(entry_route)
app.register_blueprint(temp_route)
app.register_blueprint(motor_route)
