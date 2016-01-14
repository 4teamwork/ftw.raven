from ftw.raven.config import get_raven_config
from ftw.raven.tests import FunctionalTestCase
import os


class TestRavenConfig(FunctionalTestCase):

    def test_not_enabled_when_not_configured(self):
        self.assertFalse(get_raven_config().enabled)

    def test_enabled_when_dsn_configured(self):
        os.environ['RAVEN_DSN'] = 'https://123:456@sentry.local/2'
        self.assertTrue(get_raven_config().enabled)

    def test_dsn_is_accessible_as_attribute(self):
        os.environ['RAVEN_DSN'] = 'https://123:456@sentry.local/3'
        self.assertEquals('https://123:456@sentry.local/3',
                          get_raven_config().dsn)
