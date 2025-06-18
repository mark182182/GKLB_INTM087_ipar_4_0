from dto.user import UserDto
from db.db import Database


class UserRepository:
    __db: Database

    def __init__(self, db: Database):
        self.__db = db

    def get_user_by_id(self, userId: str) -> UserDto:
        cursor = self.__db.conn.cursor()

        cursor.execute(
            "SELECT userId, userName FROM iot.users WHERE userId = %s", [userId]
        )
        existingUser = self.__create_user_from_results(cursor.fetchall())
        if existingUser is None:
            raise ValueError(f"User with id: {userId} does not exist!")

        self.__db.conn.commit()
        cursor.close()
        return existingUser

    def get_users(self) -> list[UserDto]:
        cursor = self.__db.conn.cursor()

        cursor.execute("SELECT userId, userName FROM iot.users")
        results = cursor.fetchall()

        users = []
        for row in results:
            userId = row[0]
            userName = row[1]
            users.append(UserDto(userId, userName))

        self.__db.conn.commit()
        cursor.close()
        return users

    def create_user(self, userDetails: any) -> UserDto:
        cursor = self.__db.conn.cursor()

        cursor.execute(
            "INSERT INTO iot.users VALUES (NULL, %s)", [userDetails["userName"]]
        )
        self.__db.conn.commit()

        cursor.execute(
            "SELECT userId, userName FROM iot.users ORDER BY userId DESC LIMIT 1"
        )
        user = self.__create_user_from_results(cursor.fetchall())

        self.__db.conn.commit()
        cursor.close()

        return user

    def update_user(self, userDetails: any) -> UserDto:
        cursor = self.__db.conn.cursor()

        try:
            existingUser = self.get_user_by_id(userDetails["userId"])
            if existingUser is None:
                raise ValueError(
                    f'User with id: {userDetails["userId"]} does not exist!'
                )

            cursor.execute(
                "UPDATE iot.users SET userName=%s WHERE userId=%s",
                [userDetails["userName"], userDetails["userId"]],
            )
            self.__db.conn.commit()

            user = self.get_user_by_id(userDetails["userId"])
            return user

        finally:
            self.__db.conn.commit()
            cursor.close()

    def delete_user(self, userId: str):
        cursor = self.__db.conn.cursor()
        try:
            existingUser = self.get_user_by_id(userId)
            if existingUser is None:
                raise ValueError(f"User with id: {userId} does not exist!")
            cursor.execute("DELETE FROM iot.users WHERE userId=%s", [userId])

        finally:
            self.__db.conn.commit()
            cursor.close()

    def __create_user_from_results(self, results) -> UserDto:
        user = None
        for row in results:
            userId = row[0]
            userName = row[1]
            user = UserDto(userId, userName)

        return user
