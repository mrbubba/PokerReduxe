import json

class TableEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
