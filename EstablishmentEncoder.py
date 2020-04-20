import json


class EstablishmentEncoder(json.JSONEncoder):
    def default(self, object):
        return object.__dict__
