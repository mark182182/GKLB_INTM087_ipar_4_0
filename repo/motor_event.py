from db.db import Database
from dto.motor_event import MotorEventDto
from models.motor import MotorEvent


class MotorEventRepo:
    __db: Database

    def __init__(self, db: Database):
        self.__db = db

    def insert_event(self, userId, action: MotorEvent, speed=None):
        sql = "INSERT INTO motor_event (userId, action, speed) VALUES (%s, %s, %s)"
        cursor = self.__db.conn.cursor()
        try:
            cursor.execute(sql, (userId, action.value, speed))
            self.__db.conn.commit()
        except Exception as e:
            self.__db.conn.rollback()
            raise e
        finally:
            cursor.close()

    def __create_motor_event_from_results(self, row):
        return MotorEventDto(
            id=row[0], event_time=row[1], userId=row[2], action=row[3], speed=row[4]
        )

    def get_events(self, userId=None):
        sql = "SELECT id, event_time, userId, action, speed FROM motor_event"
        params = []
        if userId:
            sql += " WHERE userId = %s"
            params = [userId]
        cursor = self.__db.conn.cursor()
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            self.__db.conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return [self.__create_motor_event_from_results(row) for row in results]
