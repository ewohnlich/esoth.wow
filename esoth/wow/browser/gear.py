from five import grok
from Products.statusmessages.interfaces import IStatusMessage
from urllib2 import urlopen

from esoth.wow import _
from esoth.wow.interfaces import IGearItem
from esoth.wow.tools import get_item

grok.templatedir('.')

class GearView(grok.View):
  grok.context(IGearItem)
  grok.name('view')
  grok.template('gear')

  def resource_base_url(self):
    #return 'http://us.media.blizzard.com'
    return 'http://www.esoth.com/proxyi?u=http://us.media.blizzard.com'

class GearUpdate(grok.View):
  grok.context(IGearItem)
  grok.name('update')

  def render(self):
    contexts = get_item(self.context.item_id)
    for context in contexts:
      if context.get('name'):
        self.context.title = context['name']
        self.context.slot = context['slot']
        self.context.armor_class = context['armor_class']
        self.context.weapon_type = context['weapon_type']
        self.context.icon = context['icon']
        self.context.klass = context['klass']
        break
    self.context.contexts = contexts
    self.context.reindexObject()

    IStatusMessage(self.request).addStatusMessage(_(u"Item updated"),"info")
    self.request.response.redirect(self.context.absolute_url())