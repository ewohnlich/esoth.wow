from five import grok
from urllib2 import urlopen
from zope.interface import Interface

from esoth.wow.tools import get_icon

class GetIcon(grok.View):
  grok.context(Interface)
  grok.name('get_icon')

  def render(self):
    self.request.response.setHeader('Content-Type','image/jpeg; charset=utf-8')
    icon=get_icon(self.request['tag'],avatar=self.request.get('avatar'))
    return urlopen(get_icon(self.request['tag'],avatar=self.request.get('avatar'))).read()