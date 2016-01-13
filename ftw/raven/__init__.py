from zope.i18nmessageid import MessageFactory
from ftw.raven.monkeypatches import install_patches


_ = MessageFactory('ftw.raven')
install_patches()
