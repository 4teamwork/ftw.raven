from zope import schema
from zope.component import queryUtility
from zope.component.zcml import handler
from zope.interface import implements
from zope.interface import Interface


class IRavenConfig(Interface):
    """Raven client configuration
    """

    dsn = schema.URI(
        title=u"DNS of Sentry project",
        description=u"e.g. https://hash1:hash2@sentry.local/17",
        required=True,
    )


def get_raven_config():
    return queryUtility(IRavenConfig)


class RavenConfig(object):
    implements(IRavenConfig)

    def __init__(self, dsn):
        self.dsn = dsn


def raven_config_directive(context, **kwargs):
    component = RavenConfig(**kwargs)
    provides = IRavenConfig
    context.action(
        discriminator=('raven:config', kwargs.get('dsn')),
        callable=handler,
        args=('registerUtility', component, provides))
