import shelve
from utils import *

DB_PATH = "./resource/thing.db"

class Database:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
    
    def get(self):
        if not hasattr(self, '__db'):
            self.__db = shelve.open(DB_PATH, writeback=True)
        return self.__db
    
    def close(self):
        if not hasattr(self, '__db'):
            return 0
        self.__db.close()
        del self.__db

def get_db():
    return Database().get()

def close_db():
    Database().close()
