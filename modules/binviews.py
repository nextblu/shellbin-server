from modules.database import Database
from tentalog import Tentacle

logger = Tentacle().logger


class BinViews:
    def __init__(self):
        self.__db = Database()

    def get_bin_views(self, url):
        cursor = self.__db.get_cursor()
        logger.debug(f"Retrieving views for url {url}")
        query = "SELECT total_views FROM binViews WHERE slug = %s"
        cursor.execute(query, (url,))
        result = list(cursor.fetchall())
        total_views = 0
        if result:
            total_views = result[0][0]
        else:
            query = "INSERT INTO binViews (slug, total_views) VALUES (%s, 0)"
            cursor.execute(query, (url,))

        cursor.close()
        self.__db.done()
        return total_views

    def increment_bin_views(self, url):
        cursor = self.__db.get_cursor()
        logger.debug(f"Incrementing likes for url")
        query = "SELECT total_views FROM binViews WHERE slug = %s"
        cursor.execute(query, (url,))
        result = list(cursor.fetchall())
        query = None
        if result:
            query = "UPDATE binViews SET total_views = total_views + 1 WHERE slug = %s"
        else:
            query = "INSERT INTO binViews (slug, total_views) VALUES (%s, 1)"
        cursor.execute(query, (url,))
        query = "SELECT total_views FROM binViews WHERE slug = %s"
        cursor.execute(query, (url,))
        result = list(cursor.fetchall())

        cursor.close()
        self.__db.done()
        return result[0][0]
