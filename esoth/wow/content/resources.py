from plone.dexterity.content import Container
from zope.interface import implements

from esoth.wow.interfaces import IWoWResources

class WoWResources(Container):
  """ """
  implements(IWoWResources)
  
  def resources(self):
    return self