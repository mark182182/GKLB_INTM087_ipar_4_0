import threading
from globals import logged_in_user

from repo.entry import EntryRepository

import logging

logger = logging.getLogger(__name__)


class RfidSpi:
    __entryRepo: EntryRepository
    __is_reading: bool = False

    def __init__(self, entry_repo: EntryRepository):
        from pirc522 import RFID
        import RPi.GPIO as GPIO

        self.__entryRepo = entry_repo
        self.__rdr = RFID(pin_mode=GPIO.BCM, pin_irq=None)
        self.__wait_for_input()

    def __wait_for_input(self):
        try:
            if not self.__is_reading:
                self.__is_reading = True
                uid = self.__rdr.read_id(as_number=True)
                if uid is not None:
                    logger.info(f"Reading card: {uid}")
                    userEntry = self.__entryRepo.check_entry_for_rfid(uid)
                    if logged_in_user.id is None:
                        logged_in_user.id = userEntry.get_user().get_user_id()
                        logged_in_user.rfidId = userEntry.get_rfid_id()
                        logged_in_user.rfidValue = uid
                    else:
                        logged_in_user.id = None
                        logged_in_user.rfidId = None
                        logged_in_user.rfidValue = None
                self.__is_reading = False
        except ValueError as e:
            logger.info(e)
            self.__is_reading = False
        finally:
            schedule = threading.Timer(1, self.__wait_for_input)
            schedule.start()
