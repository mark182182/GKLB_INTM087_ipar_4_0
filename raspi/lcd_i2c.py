from time import sleep
from globals import logged_in_user
import threading
import queue

from rpi_lcd import LCD


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
        self._process_queue(["Belepes", "engedelyezve!"])

    def denied_generic(self):
        self.prin_process_queuet_on_lcd(["Belepes", "megtagadva!"])

    def denied_locked(self):
        self._process_queue(["Kartya", "letiltva!"])

    def denied_unknown(self):
        self._process_queue(["Kartya nem", "ismert!"])

    def __wait_for_login(self):
        self.__lcd.clear()
        self.__lcd.text("Kerem erintse", 1)
        self.__lcd.text("a kartyajat!", 2)

    def __display_logged_in_msg(self):
        self.__lcd.clear()
        self.__lcd.text("Belepve:", 1)
        self.__lcd.text(f"{logged_in_user.rfid}", 2)

    def _process_queue(self, messages: list[str]):
        while True:
            try:
                messages = self._msg_queue.get(timeout=1)
                self.__lcd.clear()
                self.__lcd.text(messages[0], 1)
                self.__lcd.text(messages[1], 2)
                sleep(5)
                self._msg_queue.task_done()
            except queue.Empty:
                if logged_in_user.id is not None:
                    self.__wait_for_login()
                else:
                    self.__display_logged_in_msg()
