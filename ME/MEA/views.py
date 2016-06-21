# Create your views here.
import pymongo
import mongoengine
from django.http import HttpResponse
import json
from common.json.encoders import SdccJsonEncoder
from common.db.dbtools import get_db
from MEA.models import *


orig_dumps = json.dumps

def _dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=None, indent=None, separators=None,
          encoding='utf-8', default=None, **kw):
    try:
        return orig_dumps(obj, skipkeys, ensure_ascii, check_circular,
          allow_nan, cls, indent, separators,
          encoding, default, **kw)
    except:
        if isinstance(obj, pymongo.cursor.Cursor):
            obj = list(obj)
        elif isinstance(obj, mongoengine.queryset.queryset.QuerySet):
            use_db_field = kw.pop('use_db_field', True)
            lst = []
            for o in obj:
                lst.append(o.to_mongo(use_db_field))
            obj = lst
        elif isinstance(obj, RootDocument):
            use_db_field = kw.pop('use_db_field', True)
            obj = obj.to_mongo(use_db_field)
        return orig_dumps(obj, skipkeys, ensure_ascii, check_circular,
          allow_nan, cls, indent, separators,
          encoding, default, **kw)

json.dumps = _dumps




#_get
def home(request):
    db = get_db()

    obj = EvgTest()
    obj['name'] = 'roy'
    obj.ip_addr = '127.0.0.1'
    obj.save()

    documents = db.EvgTest.find()
    return HttpResponse(json.dumps(documents, cls=SdccJsonEncoder))


def _post(request):
    db = get_db()
    obj = db.EvgTest()
    obj['name'] = str(request.POST.get('name'))
    obj['ip_addr'] = str(request.POST.get('ip_addr'))

    obj1 = {
        'name' : "SecurityDAM",
        'ip_addr' : "192.168.0.1"
    }
    db.EvgTests.save(obj1)
    try:
        obj.save()
    except:
        import traceback
        print traceback.format_exc()
        return HttpResponse(status=401)
    return HttpResponse(json.dumps(obj, cls=SdccJsonEncoder))



