from config import is_arm
from repo.entry import EntryRepository
from repo.motor_config import MotorConfigRepo
from repo.motor_event import MotorEventRepo
from db.db import Database
from repo.rfid import RfidRepository
from repo.temp import TemperatureRepo
from repo.user import UserRepository
from repo.user_id import UserIdentifierRepository

db = Database()
db.setup()

user_repo = UserRepository(db)
rfid_repo = RfidRepository(db)
user_id_repo = UserIdentifierRepository(db, rfid_repo)
entry_repo = EntryRepository(db, user_id_repo)
motor_event_repo = MotorEventRepo(db)
motor_config_repo = MotorConfigRepo(db)
motor_event_repo = MotorEventRepo(db)

if is_arm:
    temp_repo = TemperatureRepo(db)
