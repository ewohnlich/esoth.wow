import logging
from plone.dexterity.content import Item
from zope.component import getUtility
from zope.interface import implements, Interface

from esoth.wow import _
from esoth.wow.config import API_KEY

logger = logging.getLogger('esoth.wow')

class GearItem(Item):
  """ """

  def armory(self):
    return get_item(self.item_id)

  def getIcon(self,dummy=True):
    if not self.icon:
      return super(GearItem,self).getIcon(dummy)
    return '@@get_icon?tag=%s' % self.icon