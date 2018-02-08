from ftw.builder import Builder
from ftw.builder import create
from ftw.raven.client import get_raven_client
from ftw.raven.tests import FunctionalTestCase
from ftw.raven.tests.client_mock import CrashingClientMock
from pkg_resources import get_distribution
import os


class TestIntegration(FunctionalTestCase):

    def test_errors_in_requests_are_captured(self):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        self.request_to_error_view()
        calls = get_raven_client().captureException_calls
        self.assertEquals(1, len(calls), 'Expected one raven client call')
        self.assertEquals(KeyError, calls[0]['exc_info'][0],
                          'Expected a KeyError to be reported.')

    def test_request_infos(self):
        call = self.make_error_and_get_capture_call(data={'foo': '3'})
        self.maxDiff = None

        expected = call['data']['request']

        # "X-Theme-Enabled" is available on Plone 5 but not on Plone 4.
        # It's irrelevant for our test so we can remove it.
        expected['headers'].pop('X-Theme-Enabled', None)

        self.assertEquals(
            {'cookies': {},
             'url': 'http://nohost/plone/make_key_error',
             'headers': {'Http-Referer': '',
                         'Connection': 'close',
                         'Referer': '',
                         'Host': 'nohost',
                         'User-Agent': 'Python-urllib/2.7'},
             'env': {'CONTENT_LENGTH': '5',
                     'CONTENT_TYPE': 'application/x-www-form-urlencoded',
                     'QUERY_STRING': '',
                     'REQUEST_METHOD': 'POST',
                     'PATH_INFO': '/plone/make_key_error',
                     'SERVER_PROTOCOL': 'HTTP/1.1'},
             'query_string': '',
             'data': {'foo': '3'},
             'method': 'POST'},
            expected)

    def test_user_infos_as_anonymous(self):
        call = self.make_error_and_get_capture_call()
        self.maxDiff = None
        self.assertEquals(
            {'authentication': 'anonymous',
             'ip_address': '',
             'roles': ('Anonymous',),
             'roles_in_context': ['Anonymous']},
            call['data']['user'])

    def test_user_infos_as_logged_in_user(self):
        user = create(Builder('user'))
        call = self.make_error_and_get_capture_call(login_as=user)
        self.maxDiff = None
        self.assertEquals(
            {'authentication': 'authenticated',
             'email': 'john@doe.com',
             'fullname': 'Doe John',
             'id': 'john.doe',
             'username': 'john.doe',
             'ip_address': '',
             'roles': ['Member', 'Authenticated'],
             'roles_in_context': ['Member', 'Authenticated']},
            call['data']['user'])

    def test_extra_infos(self):
        call = self.make_error_and_get_capture_call()
        self.assertIn('context', call['data']['extra'])
        self.assertIn('request.other', call['data']['extra'])

    def test_modules_infos(self):
        call = self.make_error_and_get_capture_call()
        self.assertIn('ftw.raven', call['data']['modules'])
        self.assertIn('python', call['data']['modules'])

    def test_release_not_sent_when_nothing_configured(self):
        call = self.make_error_and_get_capture_call()
        self.assertNotIn('release', call['data'])

    def test_release_with_project_dist(self):
        os.environ['RAVEN_PROJECT_DIST'] = 'zope.interface'
        call = self.make_error_and_get_capture_call()
        version = get_distribution('zope.interface').version
        self.assertDictContainsSubset({'release': version}, call['data'])

    def test_exceptions_catched_when_client_crashes(self):
        CrashingClientMock.install()
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        self.assertEquals(0, get_raven_client().crashes)
        self.request_to_error_view()
        self.assertEquals(
            2, get_raven_client().crashes,
            'We excpect exactly two attempts to report an exception:'
            ' 1. Report the actual exception,'
            ' 2. Report the meta exception that the first one failed.')

    def test_404_reporting_can_be_enabled(self):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        self.request_to_error_view(view='make_404_err')
        self.assertEquals(0, len(get_raven_client().captureException_calls))

        os.environ['RAVEN_ENABLE_EXCEPTIONS'] = 'NotFound'
        self.request_to_error_view(view='make_404_err')
        self.assertEquals(1, len(get_raven_client().captureException_calls))

    def test_error_log_id_is_reported_as_tag(self):
        call = self.make_error_and_get_capture_call()
        self.assertIn('error_log_id', call['data']['tags'])

    def test_additional_tags_are_reported(self):
        os.environ['RAVEN_TAGS'] = '{"maintainer": "hugo"}'
        call = self.make_error_and_get_capture_call()
        self.assertDictContainsSubset({'maintainer': 'hugo'},
                                      call['data']['tags'])

    def make_error_and_get_capture_call(self, **kwargs):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        self.request_to_error_view(**kwargs)
        calls = get_raven_client().captureException_calls
        self.assertEquals(1, len(calls), 'Expected one raven client call')
        return calls[0]
