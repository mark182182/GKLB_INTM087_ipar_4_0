class UserDto:
    __userId: int
    __userName: str

    def __init__(self, userId: int, userName: str):
        self.__userId = userId
        self.__userName = userName

    def get_user_id(self) -> int:
        return self.__userId

    def get_user_name(self) -> str:
        return self.__userName
