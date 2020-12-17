import requests

baseUrl = 'https://api.opendota.com/api'

class DotaIndex:
  def getMatch(self):
    match = requests.get(f'{baseUrl}/matches/5340103082')
    return match.json()