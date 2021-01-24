import json


def printJSON(s):
    print(json.dumps(s, sort_keys=True, indent=2))


class NotEnoughSongsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()
