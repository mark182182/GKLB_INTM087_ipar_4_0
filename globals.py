from service.motor import MotorService
from repo.motor_event import MotorEventRepo
from db.db import Database

db = Database()
db.setup()
motor_event_repo = MotorEventRepo(db)
motor_service = MotorService(
    in1_pin=23, in2_pin=24, en_pin=25, motor_event_repo=motor_event_repo
)
