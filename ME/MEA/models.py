
from mongoengine import Document
from common.model.custom_types import *
from common.db.dbtools import DBWRAPPER
import sys
import pymongo
from mongoengine.fields import *
import json

class RootDocument(Document):
    meta = {'allow_inheritance': True, 'abstract': True}


class pymongoSearch():
    def __init__(self, localDB, collection):
        self.collectionToSearch = collection
        self.localDBName = localDB

    def check_for_none_local_models(collection, host='localhost', port='27017'):
        retVal = False
        client = pymongo.MongoClient(host, port)
        db_list = client.database_names()
        if db_list.__len__() == 0:
            for db in db_list:
                if client[db].collection_names().__contains__(collection):
                    retVal = "%s + %s" % (retVal, client[db][collection].find())
        return retVal

class Interface():
    def __init__(self):
        self.name = 'eee'
        self.capacity = 30
        self.ip_addr = '170.0.0.1'
    name = StringField
    capacity = IntField
    ip_addr = IpAddress

class EvgTest(RootDocument):
#    def __init__(self):
#        self.interface = Interface()
    meta = {'collection': 'EvgTests'}
    name = StringField(required=True)
    ip_addr = IpAddress(required=True)
    interface = Interface()
    @staticmethod
    def find():
        self = EvgTest()
        return EvgTest.objects()

DBWRAPPER.register(EvgTest)