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

    def test_project_dist(self):
        os.environ['RAVEN_PROJECT_DIST'] = 'my.project'
        self.assertEquals('my.project', get_raven_config().project_dist)

    def test_buildout_root(self):
        parent_dir = os.path.dirname(__file__)
        os.environ['RAVEN_BUILDOUT_ROOT'] = parent_dir
        self.assertEquals(parent_dir, get_raven_config().buildout_root)
