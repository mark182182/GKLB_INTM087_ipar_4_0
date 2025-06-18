from db.db import Database
from dto.rfid import RfidDto


class RfidRepository:
    __db: Database

    def __init__(self, db: Database):
        self.__db = db

    def get_rfid_by_value(self, rfidValue: str) -> RfidDto:
        cursor = self.__db.conn.cursor()

        cursor.execute(
            "SELECT rfidId, rfidValue FROM iot.rfid WHERE rfidValue = %s", [rfidValue]
        )
        existingRfid = self.__create_rfid_from_results(cursor.fetchall())
        if existingRfid is None:
            raise ValueError(f"Rfid with value: {rfidValue} does not exist!")

        self.__db.conn.commit()
        cursor.close()
        return existingRfid

    def get_rfids(self) -> list[RfidDto]:
        cursor = self.__db.conn.cursor()

        cursor.execute("SELECT rfidId, rfidValue FROM iot.rfid")
        results = cursor.fetchall()

        rfids = []
        for row in results:
            rfidId = row[0]
            rfidValue = row[1]
            rfids.append(RfidDto(rfidId, rfidValue))

        self.__db.conn.commit()
        cursor.close()
        return rfids

    def create_rfid(self, rfidDetails: any) -> RfidDto:
        cursor = self.__db.conn.cursor()

        cursor.execute("INSERT INTO iot.rfid VALUES (NULL, %s)", [rfidDetails["value"]])
        self.__db.conn.commit()

        cursor.execute(
            "SELECT rfidId, rfidValue FROM iot.rfid ORDER BY rfidId DESC LIMIT 1"
        )
        rfid = self.__create_rfid_from_results(cursor.fetchall())

        self.__db.conn.commit()
        cursor.close()

        return rfid

    def update_rfid(self, rfidDetails: any) -> RfidDto:
        cursor = self.__db.conn.cursor()

        try:
            existingRfid = self.get_rfid_by_value(rfidDetails["value"])
            if existingRfid is None:
                raise ValueError(f'Rfid with id: {rfidDetails["id"]} does not exist!')

            cursor.execute(
                "UPDATE iot.rfid SET rfidValue=%s WHERE rfidId=%s",
                [rfidDetails["value"], rfidDetails["id"]],
            )
            self.__db.conn.commit()

            rfid = self.get_rfid_by_value(rfidDetails["value"])
            return rfid

        finally:
            self.__db.conn.commit()
            cursor.close()

    def delete_rfid(self, rfidValue: str):
        cursor = self.__db.conn.cursor()
        try:
            existingRfid = self.get_rfid_by_value(rfidValue)
            if existingRfid is None:
                raise ValueError(f"Rfid with value: {rfidValue} does not exist!")
            cursor.execute(
                "DELETE FROM iot.rfid WHERE rfidId=%s", [existingRfid.get_rfid_id()]
            )

        finally:
            self.__db.conn.commit()
            cursor.close()

    def __create_rfid_from_results(self, results) -> RfidDto:
        rfid = None
        for row in results:
            rfidId = row[0]
            rfidValue = row[1]
            rfid = RfidDto(rfidId, rfidValue)
        return rfid
