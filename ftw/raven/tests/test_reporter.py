from ftw.raven import reporter
from ftw.raven.client import get_raven_client
from ftw.raven.tests import FunctionalTestCase


class TestReporter(FunctionalTestCase):

    def test_silent_handling_of_request_preparation_exceptions(self):
        """When an exception happens while preparing the request,
        the exception should be catched and reported as raven_meta_error.
        """
        self.make_raven_config()
        self.assertEquals(0, len(get_raven_client().captureException_calls))
        reporter.maybe_report_exception(*[None]*5)
        self.assertEquals(1, len(get_raven_client().captureException_calls),
                          'Expected exactly one error to be reported.')
        call, = get_raven_client().captureException_calls
        self.assertIn('raven_meta_error', call['data']['extra'])
