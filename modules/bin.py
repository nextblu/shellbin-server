from modules.database import Database


class Bin:
    def __init__(self):
        self.__db = Database()

    def insert_bin(self, payload, url):
        cursor = self.__db.get_cursor()
        query = """INSERT INTO bin(`data`,url)
                        VALUES (%s,%s) """
        cursor.execute(
            query,
            (
                str(payload).encode(encoding='ascii', errors='ignore'),
                str(url)
            ),
        )
        cursor.close()
        self.__db.done()
        return True

    def get_bin(self, url):
        # return the whole list of orders
        cursor = self.__db.get_cursor()
        query = """
                        SELECT
                            *
                        FROM
                            `bin`
                        WHERE url = %s
                        """
        cursor.execute(query, (url,))
        result = list(cursor.fetchall())
        logs_list = []
        if len(result) >= 1:
            for data in result:
                log_data = {
                    "id": data[0],
                    "data": data[1].decode('ascii'),
                    "url": data[2],
                    "created": data[3]
                }
                logs_list.append(log_data)
        cursor.close()
        self.__db.done()
        return logs_list
