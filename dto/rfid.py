class RfidDto:
    __rfidId: int
    __rfidValue: str

    def __init__(self, rfidId: int, rfidValue: str):
        self.__rfidId = rfidId
        self.__rfidValue = rfidValue

    def get_rfid_id(self) -> int:
        return self.__rfidId

    def get_rfid_value(self) -> str:
        return self.__rfidValue
