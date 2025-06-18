from dto.user import UserDto


class UserEntryDto:
    __user: UserDto
    __rfidId: int
    __entryTime: str

    def __init__(self, user: UserDto, rfidId: int, entryTime: str):
        self.__user = user
        self.__rfidId = rfidId
        self.__entryTime = entryTime

    def get_user(self) -> UserDto:
        return self.__user

    def get_rfid_id(self) -> int:
        return self.__rfidId

    def get_entry_time(self) -> str:
        return self.__entryTime
