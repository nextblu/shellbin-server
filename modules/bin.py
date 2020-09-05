from modules.database import Database
from tentalog import Tentacle

import sys

logger = Tentacle().logger


class Bin:
    def __init__(self):
        self.__db = Database()

    def insert_bin_legacy(self, payload, url):
        cursor = self.__db.get_cursor()
        logger.debug(f"Inserting new Bind at url {str(url)}")
        query = """INSERT INTO bin(`data`,url)
                        VALUES (%s,%s) """
        cursor.execute(
            query,
            (
                str(payload).encode(sys.stdout.encoding, errors='replace'),
                str(url)
            ),
        )
        cursor.close()
        self.__db.done()
        return True

    def get_bin_legacy(self, url):
        cursor = self.__db.get_cursor()
        logger.debug(f"Retrieving bin for url {url}")
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
            logger.debug(f"Found {len(result)} Bins for url {url}")
            for data in result:
                log_data = {
                    "id": data[0],
                    "data": data[1].decode(),
                    "url": data[2],
                    "created": data[3]
                }
                logs_list.append(log_data)
        cursor.close()
        self.__db.done()
        return logs_list

    def insert_bin_v2(self, creator, title, data, private, url, language):
        cursor = self.__db.get_cursor()
        logger.debug(f"Inserting new Bind at url {str(url)}")
        query = """INSERT INTO bin(`data`, url, creator, title, isPrivate, `language`)
                        VALUES (%s,%s,%s,%s,%s,%s) """
        cursor.execute(
            query,
            (
                str(data).encode(sys.stdout.encoding, errors='replace'),
                str(url),
                str(creator),
                str(title),
                private,
                language
            ),
        )
        cursor.close()
        self.__db.done()
        return True

    def get_bin_v2(self, url):
        cursor = self.__db.get_cursor()
        logger.debug(f"Retrieving bin for url {url}")
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
            logger.debug(f"Found {len(result)} Bins for url {url}")
            for data in result:
                log_data = {
                    "id": data[0],
                    "data": data[1].decode(),
                    "url": data[2],
                    "created": data[3],
                    "creator": data[4],
                    "title": data[5],
                    "isPrivate": data[6],
                    "language": data[7]
                }
                logs_list.append(log_data)
        cursor.close()
        self.__db.done()
        return logs_list
