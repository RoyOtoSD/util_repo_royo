import ipaddr
from mongoengine.base import *
from mongoengine.fields import *


class IpAddress(BaseField):
    mongo_type = StringField
    python_type = (ipaddr._BaseIP, StringField)

    def to_bson(self, value):
        if value is not None:
            return str(value)

    def to_python(self, value):
        if value is not None:
            return str(ipaddr.IPAddress(value))

    def validate(self, value, clean=True):
        if value is not None:
            ipaddr.IPAddress(value)



'''

import ipaddr
from mongokit import CustomType

class IpAddress(CustomType):
    """Maps IP addresses (both ipv4 and ipv6) to Python's ipaddr.IPAddress type.
    """
    mongo_type = basestring
    python_type = (ipaddr._BaseIP, basestring)

    def to_bson(self, value):
        if value is not None:
            return str(value)

    def to_python(self, value):
        if value is not None:
            return ipaddr.IPAddress(value)

    def validate(self, value, path):
        if value is not None:
            ipaddr.IPAddress(value)
'''