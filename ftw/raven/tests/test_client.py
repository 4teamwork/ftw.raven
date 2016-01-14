from ftw.raven.client import get_raven_client
from ftw.raven.client import purge_raven_client
from ftw.raven.tests import FunctionalTestCase
import os


class TestClient(FunctionalTestCase):

    def test_no_client_when_not_configured(self):
        self.assertIsNone(get_raven_client())

    def test_client_is_utility(self):
        os.environ['RAVEN_DSN'] = dsn = 'https://foo:bar@sentry.local/3'
        self.assertEquals(dsn, get_raven_client().dsn)

    def test_client_is_cached_and_can_be_purged(self):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        first_client = get_raven_client()
        self.assertTrue(first_client)
        self.assertEquals(id(first_client), id(get_raven_client()))
        purge_raven_client()
        self.assertNotEquals(id(first_client), id(get_raven_client()))
