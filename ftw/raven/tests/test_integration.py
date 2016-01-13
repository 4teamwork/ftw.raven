from ftw.raven.client import get_raven_client
from ftw.raven.tests import FunctionalTestCase


class TestIntegration(FunctionalTestCase):

    def test_errors_in_requests_are_captured(self):
        self.make_raven_config()
        self.request_to_error_view()
        calls = get_raven_client().captureException_calls
        self.assertEquals(1, len(calls), 'Expected one raven client call')
        self.assertEquals(KeyError, calls[0]['exc_info'][0],
                          'Expected a KeyError to be reported.')
