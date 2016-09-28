from rest_framework import serializers
from rest_framework.parsers import JSONParser


def deserialize(payload):
    data = JSONParser().parse(payload)
    return data

json.dumps(payload)
