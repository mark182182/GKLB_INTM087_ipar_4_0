from db.db import Database
from models.motor import MotorThreshold


class MotorConfigRepo:
    __db: Database

    def __init__(self, db: Database):
        self.__db = db

    def set_threshold(self, motor_threshold: MotorThreshold):
        sql = "REPLACE INTO motor_config (id, speed_pct, critical_temp) VALUES (1, %s, %s)"
        cursor = self.__db.conn.cursor()
        try:
            cursor.execute(
                sql, (motor_threshold.speed_pct, motor_threshold.critical_temp)
            )
            self.__db.conn.commit()
        except Exception as e:
            self.__db.conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_threshold(self) -> MotorThreshold:
        sql = "SELECT speed_pct, critical_temp FROM motor_config WHERE id=1"
        cursor = self.__db.conn.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return MotorThreshold(speed_pct=result[0], critical_temp=result[1])
        except Exception as e:
            raise e
        finally:
            cursor.close()
