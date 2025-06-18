from dto.rfid import RfidDto
from dto.user_id import UserIdentifierDto
from db.db import Database
from repo.rfid import RfidRepository


class UserIdentifierRepository:
    __db: Database

    def __init__(self, db: Database, rfidRepo: RfidRepository):
        self.__db = db
        self.__rfidRepo = rfidRepo

    def get_user_identifier_by_user(self, userId: str) -> list[UserIdentifierDto]:
        cursor = self.__db.conn.cursor()

        cursor.execute(
            """SELECT userIdentifierId, userId, rf.rfidId, rf.rfidValue, disabled FROM iot.user_identifier as ui
    INNER JOIN iot.rfid as rf
    ON ui.rfidId = rf.rfidId
    WHERE userId = %s""",
            [userId],
        )

        results = cursor.fetchall()

        userIdentifiers: list[UserIdentifierDto] = []
        for row in results:
            userIdentifierId = row[0]
            userId = row[1]
            rfidId = row[2]
            rfidValue = row[3]
            disabled = bool(row[4])
            userIdentifiers.append(
                UserIdentifierDto(userIdentifierId, userId, rfidId, rfidValue, disabled)
            )

        self.__db.conn.commit()
        cursor.close()
        return userIdentifiers

    def get_user_identifier_by_rfid_value(self, rfidValue: str) -> UserIdentifierDto:
        cursor = self.__db.conn.cursor()

        cursor.execute(
            """SELECT userIdentifierId, userId, rf.rfidId, rf.rfidValue, disabled FROM iot.user_identifier as ui
    INNER JOIN iot.rfid as rf
    ON ui.rfidId = rf.rfidId
    WHERE rfidValue = %s""",
            [rfidValue],
        )

        userIdentifier = self.__create_user_identifier_from_results(cursor.fetchall())

        if userIdentifier is None:
            raise ValueError(f"{rfidValue} is not assigned to any user!")

        self.__db.conn.commit()
        cursor.close()
        return userIdentifier

    def add_rfid_to_user(self, userIdentifierDetails) -> UserIdentifierDto:
        cursor = self.__db.conn.cursor()

        existingRfid: RfidDto = self.__rfidRepo.get_rfid_by_value(
            userIdentifierDetails["rfidValue"]
        )

        cursor.execute(
            "INSERT INTO iot.user_identifier VALUES (NULL, %s, %s, 0)",
            [userIdentifierDetails["userId"], existingRfid.get_rfid_id()],
        )
        self.__db.conn.commit()

        cursor.execute(
            """SELECT userIdentifierId, userId, rf.rfidId, rf.rfidValue, disabled FROM iot.user_identifier as ui
      INNER JOIN iot.rfid as rf
      ON ui.rfidId = rf.rfidId
      ORDER BY rfidId DESC LIMIT 1"""
        )
        userIdentifier = self.__create_user_identifier_from_results(cursor.fetchall())

        self.__db.conn.commit()
        cursor.close()

        return userIdentifier

    def remove_rfid_from_user(self, rfidValue: str):
        cursor = self.__db.conn.cursor()

        existingUserIdentifier: UserIdentifierDto = (
            self.get_user_identifier_by_rfid_value(rfidValue)
        )

        cursor.execute(
            "DELETE FROM iot.user_identifier WHERE rfidId = %s",
            [existingUserIdentifier.get_rfid_id()],
        )
        self.__db.conn.commit()

        cursor.execute(
            """
    SELECT userIdentifierId, userId, rfidId, disabled FROM iot.user_identifier as ui
    WHERE rfidId = %s""",
            [existingUserIdentifier.get_rfid_id()],
        )

        removedUserIdentifier = self.__create_user_identifier_from_results(
            cursor.fetchall()
        )

        if removedUserIdentifier is not None:
            raise ValueError(f"Unable to remove rfid {rfidValue} from user!")

        self.__db.conn.commit()
        cursor.close()

    def update_disabled_for_user_identifier(
        self, userIdentifierDetails
    ) -> UserIdentifierDto:
        cursor = self.__db.conn.cursor()

        cursor.execute(
            "UPDATE iot.user_identifier SET disabled=%s WHERE userId=%s AND rfidId=%s",
            [
                userIdentifierDetails["disabled"],
                userIdentifierDetails["userId"],
                userIdentifierDetails["rfidId"],
            ],
        )
        self.__db.conn.commit()

        cursor.execute(
            """SELECT userIdentifierId, userId, rf.rfidId, rf.rfidValue, disabled FROM iot.user_identifier as ui
    INNER JOIN iot.rfid as rf
    ON ui.rfidId = rf.rfidId
    WHERE userId=%s AND rf.rfidId=%s""",
            [userIdentifierDetails["userId"], userIdentifierDetails["rfidId"]],
        )
        userIdentifier = self.__create_user_identifier_from_results(cursor.fetchall())

        self.__db.conn.commit()
        cursor.close()

        return userIdentifier

    def __create_user_identifier_from_results(self, results):
        userIdentifier = None
        for row in results:
            userIdentifierId = row[0]
            userId = row[1]
            rfidId = row[2]
            rfidValue = row[3]
            disabled = bool(row[4])
            userIdentifier = UserIdentifierDto(
                userIdentifierId, userId, rfidId, rfidValue, disabled
            )
        return userIdentifier
