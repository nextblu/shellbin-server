from modules.database import Database
from modules import datetimeutil
from tentalog import Tentacle

import sys

logger = Tentacle().logger


class Stats:
    def __init__(self):
        self.__db = Database()

    def get_bin_per_day(self):
        # Getting the list of the number of bin creations in the last 60 days
        cursor = self.__db.get_cursor()
        logger.debug(f"Retrieving bin number per day")
        query = """
                        select
                            count(*) as count,
                            date(created) as date
                        from
                            `bin`
                        where
                            created >= date_sub(curdate(), interval 60 day)
                        group by 
                            date

                        """
        cursor.execute(query)
        result = list(cursor.fetchall())
        insertions_list = []
        if len(result) >= 1:
            logger.debug(f"Found {len(result)} Bins in time range")
            for data in result:
                log_data = {
                    "insertions": data[0],
                    "day": data[1]
                }
                insertions_list.append(log_data)
        cursor.close()
        self.__db.done()
        return insertions_list

    def get_last_bin_timestamp(self):
        cursor = self.__db.get_cursor()
        logger.debug(f"Getting last insertion datetime")
        query = """
                    SELECT `created` FROM `bin` ORDER BY id DESC LIMIT 1
                        """
        cursor.execute(query, )
        result = list(cursor.fetchall())
        if len(result) >= 1:
            logger.debug(f"Found latest insertion date")
            lastInsertTime = datetimeutil.ISO8601.from_datetime_obj(result[0][0])
            cursor.close()
            self.__db.done()
            return lastInsertTime
