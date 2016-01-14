from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.layer import COMPONENT_REGISTRY_ISOLATION
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig
import os


class RavenLayer(PloneSandboxLayer):
    defaultBases = (COMPONENT_REGISTRY_ISOLATION, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '  <include package="ftw.raven.demo" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'plone.app.linkintegrity')

    def testTearDown(self):
        for name in os.environ.keys():
            if name.startswith('RAVEN'):
                del os.environ[name]


RAVEN_FIXTURE = RavenLayer()
RAVEN_FUNCTIONAL = FunctionalTesting(
    bases=(RAVEN_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.raven:functional")
