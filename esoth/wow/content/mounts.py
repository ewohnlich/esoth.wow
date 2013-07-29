_mounts = []


def apicheck():
  """ Not meant to be run in Plone. """
  import json, urllib
  url = 'http://us.battle.net/api/wow/item/'
  for g in _gear:
    for id in g['ids']:
      try:
        data = json.load(urllib.urlopen(url+str(id)))
      except:
        try:
          data = json.load(urllib.urlopen('http://www.esoth.com/proxyw?u='+url+str(id)))
        except ValueError:
          print g['name'] + ' not found!'
      if data['name'] != g['name']:
        print g['name'] + ' should be renamed to ' + data['name']
      elif data['itemLevel'] != g['ilvls'][g['ids'].index(id)]:
        print g['name'] + ' item level mismatch (' + str(id) + ',' + str(data['itemLevel']) + ')'
if __name__ == '__main__':
  apicheck()