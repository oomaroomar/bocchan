import json

#print(f'__file__: {__file__}, __name__: {__name__}, __package__: {str(__package__)}')


def printJSON(s):
    print(json.dumps(s, sort_keys=True, indent=2))


class NotEnoughSongsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()
