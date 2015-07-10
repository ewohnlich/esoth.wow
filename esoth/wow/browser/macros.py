from five import grok
from zope.interface import Interface

grok.templatedir('.')

class Macros(grok.View):
  grok.name('wow_macros')
  grok.context(Interface)