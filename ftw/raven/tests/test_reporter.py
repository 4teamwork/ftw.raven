from ftw.raven import reporter
from ftw.raven.client import get_raven_client
from ftw.raven.tests import FunctionalTestCase
from pkg_resources import get_distribution
from zExceptions import NotFound
from zExceptions import Redirect
from zExceptions import Unauthorized
import os


class TestReporter(FunctionalTestCase):

    def test_silent_handling_of_request_preparation_exceptions(self):
        """When an exception happens while preparing the request,
        the exception should be catched and reported as raven_meta_error.
        """
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        self.assertEquals(0, len(get_raven_client().captureException_calls))
        reporter.maybe_report_exception(None, None, KeyError, None, None)
        self.assertEquals(1, len(get_raven_client().captureException_calls),
                          'Expected exactly one error to be reported.')
        call, = get_raven_client().captureException_calls
        self.assertIn('raven_meta_error', call['data']['extra'])

    def test_release_is_None_when_nothing_configured(self):
        self.assertIsNone(reporter.get_release())

    def test_release_can_be_project_dist_version(self):
        os.environ['RAVEN_PROJECT_DIST'] = 'zope.interface'
        version = get_distribution('zope.interface').version
        self.assertEquals(version, reporter.get_release())

    def test_no_exception_when_dist_not_existing(self):
        os.environ['RAVEN_PROJECT_DIST'] = 'foo.bar'
        self.assertIsNone(reporter.get_release())

    def test_release_can_be_buildout_git_hash(self):
        os.environ['RAVEN_BUILDOUT_ROOT'] = os.path.abspath(os.path.join(
            __file__, '..', '..', '..', '..'))
        release = reporter.get_release()
        self.assertTrue(release)
        self.assertEquals(40, len(release),
                          'Expected git SHA to be 40 bytes big.')

    def test_is_exception_type_ignored_can_handle_None(self):
        self.assertTrue(reporter.is_exception_type_ignored(None))

    def test_default_exceptions_are_not_ignored(self):
        self.assertFalse(reporter.is_exception_type_ignored(KeyError))
        self.assertFalse(reporter.is_exception_type_ignored(Exception))

    def test_default_ignored_exceptions(self):
        self.assertTrue(reporter.is_exception_type_ignored(NotFound))
        self.assertTrue(reporter.is_exception_type_ignored(Unauthorized))
        self.assertTrue(reporter.is_exception_type_ignored(Redirect))

    def test_enabling_default_ignored_exceptions(self):
        os.environ['RAVEN_ENABLE_EXCEPTIONS'] = 'NotFound'
        self.assertFalse(reporter.is_exception_type_ignored(NotFound))
        self.assertTrue(reporter.is_exception_type_ignored(Unauthorized))
        self.assertTrue(reporter.is_exception_type_ignored(Redirect))

        os.environ['RAVEN_ENABLE_EXCEPTIONS'] = 'Unauthorized, Redirect'
        self.assertTrue(reporter.is_exception_type_ignored(NotFound))
        self.assertFalse(reporter.is_exception_type_ignored(Unauthorized))
        self.assertFalse(reporter.is_exception_type_ignored(Redirect))

    def test_no_exception_when_buildout_root_invalid(self):
        os.environ['RAVEN_BUILDOUT_ROOT'] = '/invalid/buildout/root'
        self.assertIsNone(reporter.get_release())
