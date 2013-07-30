from zope.interface import implements
from interfaces import IMountUtility
import json, os

class MountUtility:
  implements(IMountUtility)
  
  def applyClasses(self, m, default_faction):
    klass = []
    faction = default_faction == 'Alliance' and 'A' or 'H'
    obtainable = 'Y'
    klass.append(m.get('isCollected') and 'obtainedMount' or 'unobtainedMount')
    klass.append(m.get('faction',faction) == 'A' and 'allianceMount' or m['faction'] == 'H' and 'hordeMount' or 'bothMount')
    klass.append(m.get('obtainable',obtainable) == 'Y' and 'obtainableMount' or 'unobtainableMount')
    klass.append(' '.join([m.get(k) and k or 'not'+k for k in ('isJumping','isGround','isFlying','isAquatic',)]))
    m = m.copy()
    m['classes'] = ' '.join(klass)
    return m
  
  def mountData(self, mounts, default_faction):
    """ Combine json info on all mounts with collected mount info
    """
    data = json.load(open(os.path.join(os.path.dirname(__file__),'mounts.json')))
    _mounts = []
    for id,info in data.items():
      _mount = {'icon':'','isCollected':False,'isGround':False,'isFlying':False,'isAquatic':False,'isJumping':False,
                'itemId':id,
                'name':info['name'],
                'location':info['location'],
                'obtainable':info['obtainable'],
                'faction':info['faction']}
      mkeys = mounts.keys()
      mkeys.sort()
        
      if id in mounts:
        _mount.update({'isCollected':True,
                       'icon':mounts[id]['icon'],
                       'name':mounts[id]['name'],
                       'isGround':mounts[id]['isGround'],
                       'isFlying':mounts[id]['isFlying'],
                       'isAquatic':mounts[id]['isAquatic'],
                       'isJumping':mounts[id]['isJumping']})
      _mounts.append(self.applyClasses(_mount,default_faction))
    _flag = False
    for id in mounts.keys():
      # we don't have any data on this one
      if id not in data:
        #import pdb; pdb.set_trace()
        _flag = True
        print 'Added ' + id + ' to mounts'
        data[id] = {'name':mounts[id]['name'],'faction':'U','obtainable':'U','location':'unknown'}
        _mounts.append(self.applyClasses({'isCollected':True,
                        'icon':mounts[id]['icon'],
                        'location':'unknown',
                        'faction':'U',
                        'obtainable':'U',
                        'itemId':id,
                        'name':mounts[id]['name'],
                        'isGround':mounts[id]['isGround'],
                        'isFlying':mounts[id]['isFlying'],
                        'isAquatic':mounts[id]['isAquatic'],
                        'isJumping':mounts[id]['isJumping']},default_faction))
                   
    if _flag:
      json.dump(data,open(os.path.join(os.path.dirname(__file__),'mounts.json'),'w'))       
    return _mounts