from ftw.testing.layer import COMPONENT_REGISTRY_ISOLATION
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class RavenLayer(PloneSandboxLayer):
    defaultBases = (COMPONENT_REGISTRY_ISOLATION, )

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '  <include package="ftw.raven.tests" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'plone.app.linkintegrity')


RAVEN_FIXTURE = RavenLayer()
RAVEN_FUNCTIONAL = FunctionalTesting(
    bases=(RAVEN_FIXTURE, ),
    name="ftw.raven:functional")
