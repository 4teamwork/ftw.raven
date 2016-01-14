from ftw.raven import reporter
from ftw.raven.client import get_raven_client
from ftw.raven.tests import FunctionalTestCase
from pkg_resources import get_distribution
import os


class TestReporter(FunctionalTestCase):

    def test_silent_handling_of_request_preparation_exceptions(self):
        """When an exception happens while preparing the request,
        the exception should be catched and reported as raven_meta_error.
        """
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        self.assertEquals(0, len(get_raven_client().captureException_calls))
        reporter.maybe_report_exception(*[None]*5)
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

    def test_no_exception_when_buildout_root_invalid(self):
        os.environ['RAVEN_BUILDOUT_ROOT'] = '/invalid/buildout/root'
        self.assertIsNone(reporter.get_release())
