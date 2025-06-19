from time import sleep
from globals import logged_in_user
import threading
import queue

from rpi_lcd import LCD

import logging

logger = logging.getLogger(__name__)


class LcdI2c:
    __lcd = LCD()

    def __init__(self):
        self._msg_queue = queue.Queue()
        self._thread = threading.Thread(target=self._process_queue, daemon=True)
        self._thread.start()
        self.__wait_for_login()

    def print_on_lcd(self, messages: list[str]):
        self._msg_queue.put(messages)

    def allowed(self):
        self.print_on_lcd(["Belepes", "engedelyezve!"])
        
    def logout(self):
        self.print_on_lcd(["Kilepes", "sikeres!"])

    def denied_generic(self):
        self.print_on_lcd(["Belepes", "megtagadva!"])

    def denied_locked(self):
        self.print_on_lcd(["Kartya", "letiltva!"])

    def denied_unknown(self):
        self.print_on_lcd(["Kartya nem", "ismert!"])

    def __wait_for_login(self):
        self.print_on_lcd(["Kerem erintse", "a kartyajat!"])

    def __display_logged_in_msg(self):
        self.print_on_lcd(["Belepve:", f"{logged_in_user.rfidValue}"])

    def _process_queue(self):
        while True:
            try:
                messages = self._msg_queue.get(timeout=1)
                logger.info(f"Displaying on LCD: {messages}")
                self.__lcd.clear()
                self.__lcd.text(messages[0], 1)
                self.__lcd.text(messages[1], 2)
                sleep(5)
                self._msg_queue.task_done()
            except queue.Empty:
                if logged_in_user.id is None:
                    self.__wait_for_login()
                else:
                    self.__display_logged_in_msg()
