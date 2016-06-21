from mongoengine import connect, connection

class CollectionWrapper():
    def __init__(self, cls, collection):
        self._collection = collection
        self._cls = cls

    def save(self, to_save, manipulate=True,
             safe=None, check_keys=True, **kwargs):
        to_save.update({'_cls': self._cls})
        self._collection.save(to_save, manipulate, safe, check_keys, **kwargs)


class DbWrapper(object):
    def __init__(self):
        self.models = {}

    def register(self, clss):
        self.models[clss.__name__] = clss

    def find_cls_name(self, name):
        for cls_name, cls in self.models.iteritems():
            if cls._meta['collection'] == name:
                return cls_name
        return None


    def __getattr__(self, name):
        if name in self.models:
            return self.models[name]
        else:
            _db = connection.get_db()
            _coll = _db[name]
            cls_name = self.find_cls_name(name)
            return CollectionWrapper(cls_name, _coll) if cls_name else _coll

DBWRAPPER = DbWrapper()

def get_db():
    global DBWRAPPER
    connect('local', username='', password='') #TODO: verify Singletne connection
    return DBWRAPPER

