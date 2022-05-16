from pymongo import MongoClient

from config import MONGO_CONF


class YaMongoDB():
    def __init__(self):
        self._mongo = MongoClient(
            MONGO_CONF['host'],
            MONGO_CONF['port']
        )

        self._db = self._mongo[MONGO_CONF['database']]
        self._coll = None

    def _get_all_dbs(self):
        return self._mongo.list_database_names()

    def _get_all_collections(self):
        return self._db.list_collection_names()

    def switch_db(self, db_name):
        self._db = self._mongo[db_name]
        return self._db

    def switch_coll(self, coll_name):
        self._coll = self._db[coll_name]
        return self._coll
