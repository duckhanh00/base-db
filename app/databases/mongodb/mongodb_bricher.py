from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.utils.logger_utils import get_logger
from pymongo import MongoClient
from config import MongoDBConfig

logger = get_logger('MongoDB Bricher')


class MongoBricher:
    def __init__(self, connection_url=None):
        if connection_url is None:
            connection_url = MongoDBConfig.BRICHER_TEST_URL

        self.connection_url = connection_url.split('@')[-1]
        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.BRICHER_DB]

        self._lendings_col = self.db[MongoCollections.lendings]
        self._borrows_col = self.db[MongoCollections.borrows]
        self._vaults_col = self.db[MongoCollections.vaults]


    def get_roi_change_logs(self, col, _id, batch=1000):
        try:
            filter_ = {'_id': _id}
            item = self.db[col].find_one(filter_)
            if 'roiChangeLogs' not in item:
                print("*****")
                print("roiChangeLogs not in ID", _id)
                print("*****")
                return None
            return {
                '_id': _id,
                'roiChangeLogs': item['roiChangeLogs']
            }
        except Exception as ex:
            logger.exception(ex)
        return None

    def get_detail_roi_change_logs(self, col, _id):
        try:
            filter_ = {'_id': _id}
            item = self.db[col].find_one(filter_)
            if 'detailROIChangeLogs' not in item:
                print("*****")
                print("detailROIChangeLogs not in ID", _id)
                print("*****")
                return None
            return {
                '_id': _id,
                'detailROIChangeLogs': item['detailROIChangeLogs']
            }
       
        except Exception as ex:
            logger.exception(ex)
        return None

    def get_liquidity_change_logs(self, col, _id):
        try:
            filter_ = {'_id': _id}
            item = self.db[col].find_one(filter_)
            if 'liquidityChangeLogs' not in item:
                print("*****")
                print("liquidityChangeLogs not in ID", _id)
                print("*****")
                return None
            return {
                '_id': _id,
                'liquidityChangeLogs': item['liquidityChangeLogs']
            }
       
        except Exception as ex:
            logger.exception(ex)
        return None

    def get_all_id(self, col, batch=1000):
        try:
            cursor = None
            filter_ = {}   
            cursor = self.db[col].find(filter_, projection={"_id": 1})
            result = []
            for item in cursor:    
                result.append(item['_id'])
            
            return result
       
        except Exception as ex:
            logger.exception(ex)
        return None