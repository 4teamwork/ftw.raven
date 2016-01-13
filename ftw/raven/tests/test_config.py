from ftw.raven.config import get_raven_config
from ftw.raven.tests import FunctionalTestCase


class TestRavenConfigDirective(FunctionalTestCase):

    def test_no_raven_config_by_default(self):
        self.assertIsNone(get_raven_config())

    def test_raven_config_is_configured_in_ZCML(self):
        dsn = 'https://123:456@sentry.local/2'
        self.make_raven_config(dsn=dsn)
        config = get_raven_config()
        self.assertIsNotNone(config)
        self.assertEquals(dsn, config.dsn)
