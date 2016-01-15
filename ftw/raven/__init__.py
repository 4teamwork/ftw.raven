from zope.i18nmessageid import MessageFactory
from ftw.raven.monkeypatches import install_patches


_ = MessageFactory('ftw.raven')


def initialize(context):
    """Initializer called when used as a Zope 2 product.

    This is referenced from configure.zcml. Regstrations as a "Zope 2 product"
    is necessary for GenericSetup profiles to work, for example.

    """
    install_patches()
