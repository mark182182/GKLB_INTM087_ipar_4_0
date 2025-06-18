class UserIdentifierDto:
    __userIdentifierId: int
    __userId: int
    __rfidId: int
    __rfidValue: str
    __disabled: bool

    def __init__(
        self,
        userIdentifierId: int,
        userId: int,
        rfidId: int,
        rfidValue: str,
        disabled: bool,
    ):
        self.__userIdentifierId = userIdentifierId
        self.__userId = userId
        self.__rfidId = rfidId
        self.__rfidValue = rfidValue
        self.__disabled = disabled

    def get_user_id(self) -> int:
        return self.__userId

    def get_user_identifier_id(self) -> int:
        return self.__userIdentifierId

    def get_rfid_id(self) -> int:
        return self.__rfidId

    def get_rfid_value(self) -> str:
        return self.__rfidValue

    def is_disabled(self) -> bool:
        return self.__disabled
