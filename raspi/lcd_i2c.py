from time import sleep

from rpi_lcd import LCD


# should be handled in a separate thread
class LcdI2c:
    __lcd = LCD()
    __is_printing = False

    def wait_for_input(self):
        self.__lcd.clear()
        self.__lcd.text("Kerem erintse", 1)
        self.__lcd.text("a kartyajat!", 2)

    def allowed(self):
        self.print_on_lcd(["Belepes", "engedelyezve!"])

    def denied_generic(self):
        self.print_on_lcd(["Belepes", "megtagadva!"])

    def denied_locked(self):
        self.print_on_lcd(["Kartya", "letiltva!"])

    def denied_unknown(self):
        self.print_on_lcd(["Kartya nem", "ismert!"])

    def print_on_lcd(self, messages: list[str]):
        if not self.__is_printing:
            self.__is_printing = True
        self.__lcd.clear()
        self.__lcd.text(messages[0], 1)
        self.__lcd.text(messages[1], 2)
        # this is not async
        sleep(5)
        self.wait_for_input()
        self.__is_printing = False
