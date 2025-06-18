from db.db import Database
from dto.temperature import TemperatureDto


class TemperatureRepo:
    __db: Database

    def __init__(self, db: Database):
        self.__db = db

    def insert_temperature(self, value_celsius):
        sql = "INSERT INTO temperature (value_celsius) VALUES (%s)"
        cursor = self.__db.conn.cursor()
        try:
            cursor.execute(sql, (value_celsius,))
            self.__db.conn.commit()
        except Exception as e:
            self.__db.conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_temperatures(self, start=None, end=None) -> list[TemperatureDto]:
        sql = "SELECT id, measured_at, value_celsius FROM temperature"
        params = []
        if start and end:
            sql += " WHERE measured_at BETWEEN %s AND %s"
            params = [start, end]
        cursor = self.__db.conn.cursor()
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [TemperatureDto(*row) for row in results]
        except Exception as e:
            raise e
        finally:
            cursor.close()
