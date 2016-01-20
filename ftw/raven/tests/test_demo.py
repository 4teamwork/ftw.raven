from ftw.raven.browser.demo import RavenConnectionTest
from ftw.raven.client import get_raven_client
from ftw.raven.tests import FunctionalTestCase
from plone.app.testing import SITE_OWNER_NAME
import os


class TestIntegration(FunctionalTestCase):

    def test_errors_in_requests_are_captured(self):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        self.request_to_error_view(view='raven-test', login_as=SITE_OWNER_NAME)
        calls = get_raven_client().captureException_calls
        self.assertEquals(1, len(calls), 'Expected one raven client call')
        self.assertEquals(RavenConnectionTest,
                          calls[0]['exc_info'][0],
                          'Expected a RavenConnectionTest to be reported.')
