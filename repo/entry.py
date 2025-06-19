from config import is_arm
from dto.user import UserDto
from dto.user_entry import UserEntryDto
from dto.user_id import UserIdentifierDto
from db.db import Database


if is_arm:
    from raspi.lcd_i2c import LcdI2c


from repo.user_id import UserIdentifierRepository
from smtp.smtp_client import smtp
from globals import logged_in_user


import logging

logger = logging.getLogger(__name__)


class EntryRepository:
    __db: Database
    __userIdentifierRepo: UserIdentifierRepository

    def __init__(self, db: Database, userIdentifierRepo: UserIdentifierRepository):
        self.__db = db
        self.__userIdentifierRepo = userIdentifierRepo
        if is_arm:
            self.__lcdI2c = LcdI2c()

    def get_entry_by_user(
        self, userId: int, isTop1: bool = False
    ) -> list[UserEntryDto]:
        cursor = self.__db.conn.cursor()

        query = """
    SELECT ui.userId, u.userName, ui.rfidId, e.entryTime FROM iot.user_identifier as ui 
    INNER JOIN iot.entry as e
    ON ui.userIdentifierId = e.userIdentifierId
    INNER JOIN iot.users as u
    ON ui.userId = u.userId 
    WHERE u.userId = %s"""

        cursor.execute(
            f"{query} ORDER BY e.entryTime DESC LIMIT 1" if isTop1 else query, [userId]
        )

        userEntries: list[UserEntryDto] = self.__create_entry_from_results(
            cursor.fetchall()
        )

        self.__db.conn.commit()
        cursor.close()
        return userEntries

    def get_entries_for_all_users(self) -> list[UserEntryDto]:
        cursor = self.__db.conn.cursor()

        cursor.execute(
            """
    SELECT ui.userId, u.userName, ui.rfidId, e.entryTime FROM iot.user_identifier as ui
    INNER JOIN iot.entry as e
    ON ui.userIdentifierId = e.userIdentifierId
    INNER JOIN iot.users as u
    ON ui.userId = u.userId"""
        )

        userEntries: list[UserEntryDto] = self.__create_entry_from_results(
            cursor.fetchall()
        )

        self.__db.conn.commit()
        cursor.close()
        return userEntries

    def check_entry_for_rfid(self, rfidValue: str) -> UserEntryDto:
        cursor = self.__db.conn.cursor()
        try:
            try:
                existingUserIdentifier: UserIdentifierDto = (
                    self.__userIdentifierRepo.get_user_identifier_by_rfid_value(
                        rfidValue
                    )
                )
            except ValueError as e:
                self.__lcdI2c.denied_unknown()
                raise e
            cursor.execute(
                """
      INSERT INTO iot.entry VALUES (%s, CURRENT_TIMESTAMP)
      """,
                [existingUserIdentifier.get_user_identifier_id()],
            )
            self.__db.conn.commit()
            if existingUserIdentifier.is_disabled():
                self.__lcdI2c.denied_locked()
                self.__send_mail_on_too_many_attempts(existingUserIdentifier)
                raise ValueError(f"{rfidValue} is locked, cannot enter!")
            cursor.execute(
                """SELECT userIdentifierId, entryTime FROM iot.entry
       WHERE userIdentifierId = %s
       ORDER BY entryTime DESC LIMIT 1""",
                [existingUserIdentifier.get_user_identifier_id()],
            )
            results = cursor.fetchall()
            if len(results) != 1:

                if is_arm:
                    self.__lcdI2c.denied_generic()

                raise ValueError(f"Unable to enter using rfid value {rfidValue}!")
            userEntry = self.get_entry_by_user(
                existingUserIdentifier.get_user_id(), True
            )
            if len(userEntry) != 1:

                if is_arm:
                    self.__lcdI2c.denied_generic()

                raise ValueError(f"Unable to enter using rfid value {rfidValue}!")
            self.__db.conn.commit()

            if is_arm:
                if logged_in_user.id is None:
                    self.__lcdI2c.allowed()
                else:
                    self.__lcdI2c.logout()
            return userEntry[0]
        except ValueError as e:
            raise e
        finally:
            cursor.close()

    def __create_entry_from_results(self, results) -> list[UserEntryDto]:
        userEntries: list[UserEntryDto] = []

        for row in results:
            userId = row[0]
            userName = row[1]
            rfidId = row[2]
            entryTime = row[3]

            userEntries.append(
                UserEntryDto(UserDto(userId, userName), rfidId, str(entryTime))
            )
        return userEntries

    def __send_mail_on_too_many_attempts(self, userIdentifier: UserIdentifierDto):
        entries: list[UserEntryDto] = self.get_entry_by_user(
            userIdentifier.get_user_id()
        )
        entryTimes: list[str] = []
        for entry in entries:
            entryTimes.append(entry.get_entry_time())
        if len(entries) == 3:
            logger.warning("Too many attempts with locked card, sending e-mail")
            smtp.send_email_on_unauthorized(
                userIdentifier.get_rfid_value(),
                userIdentifier.get_user_id(),
                entryTimes,
            )
