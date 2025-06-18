import threading
from time import sleep
from user import logged_in_user

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
                    user_id = userEntry.get_user().get_user_id()
                    rfid_id = userEntry.get_rfid_id()
                    if getattr(logged_in_user, "id", None) == user_id:
                        # log out the current user
                        print(f"Logging out user: {user_id}")
                        logged_in_user.id = None
                        logged_in_user.rfid = None
                    else:
                        # new user logged in
                        print(f"Logging in user: {user_id} with RFID: {rfid_id}")
                        logged_in_user.id = user_id
                        logged_in_user.rfid = rfid_id
                self.__is_reading = False
        except ValueError as e:
            print(e)
            self.__is_reading = False
        finally:
            schedule = threading.Timer(1, self.__wait_for_input)
            schedule.start()
