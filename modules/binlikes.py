from modules.database import Database
from tentalog import Tentacle

logger = Tentacle().logger


class BinLikes:
    def __init__(self):
        self.__db = Database()

    def get_bin_likes(self, url):
        cursor = self.__db.get_cursor()
        logger.debug(f"Retrieving likes for url {url}")
        query = "SELECT total_likes FROM binLikes WHERE slug = %s"
        cursor.execute(query, (url,))
        result = list(cursor.fetchall())
        total_likes = 0
        if result:
            total_likes = result[0][0]
        else:
            query = "INSERT INTO binLikes (slug, total_likes) VALUES(%s, 0)"
            cursor.execute(query, (url,))

        cursor.close()
        self.__db.done()
        return total_likes

    def increment_bin_likes(self, url):
        cursor = self.__db.get_cursor()
        logger.debug(f"Incrementing likes for url")
        query = "SELECT total_likes FROM binLikes WHERE slug = %s"
        cursor.execute(query, (url,))
        result = list(cursor.fetchall())

        if result:
            query = "UPDATE binLikes SET total_likes = total_likes + 1 WHERE slug = %s"
            cursor.execute(query, (url,))
        else:
            query = "INSERT INTO binLikes (slug, total_likes) VALUES(%s, 1)"
            cursor.execute(query, (url,))

        query = "SELECT total_likes FROM binLikes WHERE slug = %s"
        cursor.execute(query, (url,))
        result = list(cursor.fetchall())

        cursor.close()
        self.__db.done()
        return result[0][0]
