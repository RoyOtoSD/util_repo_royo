import json
import dateutil
from datetime import datetime
from bson import ObjectId
from ipaddr import IPAddress, IPv4Address, IPv6Address


class SdccJsonDecoder(json.JSONDecoder):
    _objectid_marker = '_oid'
    _datetime_marker = '_date_time'
    _ipaddress_marker = '_ipaddr'

    def __init__(self, encoding=None, object_hook=None, parse_float=None,
                 parse_int=None, parse_constant=None, strict=True):
        object_hook = object_hook if object_hook is not None else self._to_object
        super(SdccJsonDecoder, self).__init__(encoding=encoding, object_hook=object_hook,
                                              parse_float=parse_float, parse_int=parse_int,
                                              parse_constant=parse_constant, strict=strict)

    def _to_object(self, data):
        if self._objectid_marker in data:
            return ObjectId(data[self._objectid_marker])

        if self._datetime_marker in data:
            return dateutil.parser.parse(data[self._datetime_marker])

        if self._ipaddress_marker in data:
            return IPAddress(data[self._ipaddress_marker])

        return data


class SdccJsonEncoder(json.JSONEncoder):
    _objectid_marker = '_oid'
    _datetime_marker = '_date_time'
    _ipaddress_marker = '_ipaddr'

    def default(self, o):
        if isinstance(o, ObjectId):
            return {self._objectid_marker: str(o)}

        if isinstance(o, datetime):
            return {self._datetime_marker: o.isoformat()}

        if isinstance(o, (IPv4Address, IPv6Address)):
            return {self._ipaddress_marker: str(o)}

        return json.JSONEncoder.default(self, o)