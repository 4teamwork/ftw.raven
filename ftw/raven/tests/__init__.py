from ftw.raven import client
from ftw.raven.testing import RAVEN_FUNCTIONAL
from ftw.raven.tests.client_mock import ClientMock
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = RAVEN_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.load_zcml_string = self.layer['load_zcml_string']
        client.raven_client_class = ClientMock

    def tearDown(self):
        client.purge_raven_client()

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, roles)
        transaction.commit()

    def make_raven_config(self, dsn='https://usr:pwd@sentry.local/1'):
        self.load_zcml_string(
            '<configure xmlns:raven="http://ns.4teamwork.ch/raven">' +
            '  <raven:config dsn="{}" />'.format(dsn) +
            '</configure>')
