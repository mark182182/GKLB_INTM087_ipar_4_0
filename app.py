import logging

logging_format: str = "[%(asctime)s] - %(name)s - %(levelname)s: %(message)s"

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(logging_format)
handler.setFormatter(formatter)
logger.addHandler(handler)


from config import is_arm
from flask import Flask

if is_arm:
    import RPi.GPIO as GPIO

logging.basicConfig(level=logging.INFO, format=logging_format)

from repo.temp import TemperatureRepo


app = Flask(__name__)

app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

from route.user import user_route
from route.rfid import rfid_route
from route.user_id import user_id_route
from route.entry import entry_route
from route.temp import temp_route
from route.motor import motor_route


app.register_blueprint(user_route)
app.register_blueprint(rfid_route)
app.register_blueprint(user_id_route)
app.register_blueprint(entry_route)
app.register_blueprint(temp_route)
app.register_blueprint(motor_route)
