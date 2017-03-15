from ftw.raven.config import get_raven_config
from ftw.raven.tests import FunctionalTestCase
import os
import tempfile


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

    def test_ignored_exception_classnames(self):
        self.assertEquals(
            set(['Redirect', 'NotFound', 'Unauthorized', 'Intercepted']),
            set(get_raven_config().ignored_exception_classnames))

        os.environ['RAVEN_ENABLE_EXCEPTIONS'] = 'NotFound'
        self.assertEquals(
            set(['Redirect', 'Unauthorized', 'Intercepted']),
            set(get_raven_config().ignored_exception_classnames))

        os.environ['RAVEN_ENABLE_EXCEPTIONS'] = 'Unauthorized, Redirect'
        self.assertEquals(
            set(['NotFound', 'Intercepted']),
            set(get_raven_config().ignored_exception_classnames))

        os.environ['RAVEN_ENABLE_EXCEPTIONS'] = 'Unauthorized, Redirect, NotFound'
        self.assertEquals(
            set(['Intercepted']),
            set(get_raven_config().ignored_exception_classnames))

        os.environ['RAVEN_ENABLE_EXCEPTIONS'] = 'Unauthorized, Redirect, NotFound, Intercepted'
        self.assertEquals(
            set(),
            set(get_raven_config().ignored_exception_classnames))

    def test_disabling_custom_exceptions(self):
        self.assertNotIn('RandomError',
                         get_raven_config().ignored_exception_classnames)

        os.environ['RAVEN_DISABLE_EXCEPTIONS'] = 'RandomError'
        self.assertIn('RandomError',
                      get_raven_config().ignored_exception_classnames)

        os.environ['RAVEN_DISABLE_EXCEPTIONS'] = 'Foo, RandomError, Bar'
        self.assertIn('RandomError',
                      get_raven_config().ignored_exception_classnames)

    def test_no_tags_by_default(self):
        self.assertEquals({}, get_raven_config().tags)

    def test_custom_tags_with_env_variable(self):
        os.environ['RAVEN_TAGS'] = ('{"deployment_type": "production",'
                                    ' "maintainer": "peter"}')
        self.assertEquals({"deployment_type": "production",
                           "maintainer": "peter"},
                          get_raven_config().tags)

    def test_custom_tags_may_be_invalid(self):
        os.environ['RAVEN_TAGS'] = '{"something completely wrong":}'
        self.assertEquals({'RAVEN_TAGS': 'invalid configuration'},
                          get_raven_config().tags)

    def test_custom_tags_by_file(self):
        with tempfile.NamedTemporaryFile() as tags_file:
            os.environ['RAVEN_TAGS_FILE'] = tags_file.name
            tags_file.write('{"status": "testing"}')
            tags_file.seek(0)

            self.assertEquals({'status': 'testing'},
                              get_raven_config().tags)

    def test_file_content_may_be_invalid(self):
        with tempfile.NamedTemporaryFile() as tags_file:
            os.environ['RAVEN_TAGS_FILE'] = tags_file.name
            self.assertEquals({'RAVEN_TAGS_FILE': 'invalid content'},
                              get_raven_config().tags)

            tags_file.write('not json at all')
            tags_file.seek(0)
            self.assertEquals({'RAVEN_TAGS_FILE': 'invalid content'},
                              get_raven_config().tags)

    def test_file_may_not_exist(self):
        os.environ['RAVEN_TAGS_FILE'] = '/foo/br'
        self.assertEquals({'RAVEN_TAGS_FILE': 'missing file'},
                          get_raven_config().tags)

    def test_combining_tags_from_file_and_env_variable(self):
        os.environ['RAVEN_TAGS'] = '{"maintainer": "hans", "priority": "env"}'
        with tempfile.NamedTemporaryFile() as tags_file:
            os.environ['RAVEN_TAGS_FILE'] = tags_file.name
            tags_file.write('{"purpose": "demo", "priority": "file"}')
            tags_file.seek(0)

            self.assertEquals({'purpose': 'demo',
                               'maintainer': 'hans',
                               'priority': 'env'},
                              get_raven_config().tags)
