import threading
from time import sleep
from globals import logged_in_user

from repo.entry import EntryRepository


class RfidSpi:
    __entryRepo: EntryRepository
    __is_reading: bool = False

    def __init__(self, entryRepo: EntryRepository):
        from pirc522 import RFID
        import RPi.GPIO as GPIO

        self.__entryRepo = entryRepo
        self.__rdr = RFID(pin_mode=GPIO.BCM, pin_irq=None)
        self.__wait_for_input()

    def __wait_for_input(self):
        try:
            if not self.__is_reading:
                self.__is_reading = True
                uid = self.__rdr.read_id(as_number=True)
                if uid is not None:
                    print(f"reading card: {uid}")
                    userEntry = self.__entryRepo.check_entry_for_rfid(uid)
                    logged_in_user.id = userEntry.get_user().get_user_id()
                    logged_in_user.rfid = userEntry.get_rfid_id()
                self.__is_reading = False
        except ValueError as e:
            print(e)
            self.__is_reading = False
        finally:
            schedule = threading.Timer(1, self.__wait_for_input)
            schedule.start()
