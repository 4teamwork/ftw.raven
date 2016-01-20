from ftw.raven.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from pkg_resources import get_distribution
import json
import os
import re


class TestJavaScript(FunctionalTestCase):

    @browsing
    def test_lib_headers(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven.js')
        self.assertEquals('application/javascript; charset=utf-8',
                          browser.headers['Content-Type'])
        self.assertEquals('True',
                          browser.headers.get('X-Theme-Disabled'))

    @browsing
    def test_config_empty_when_not_configured(self, browser):
        browser.login().open(view='ftw.raven-config.js')
        self.assertEquals('', browser.contents)

    @browsing
    def test_user_context_configured(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven-config.js')
        config = self.extract_config_from_javascript(browser.contents)
        self.assertEquals({'username': 'test-user',
                           'authentication': 'authenticated',
                           'fullname': '',
                           'ip_address': '',
                           'id': 'test_user_1_',
                           'email': ''},
                          config['user_context'])

    @browsing
    def test_dsn_configured(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven-config.js')
        config = self.extract_config_from_javascript(browser.contents)
        self.assertEquals('https://x@sentry.local/1', config['dsn'])

    @browsing
    def test_server_name_in_config_args(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven-config.js')
        config = self.extract_config_from_javascript(browser.contents)
        self.assertIn('serverName', config['options'])

    @browsing
    def test_release_in_config_args(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        os.environ['RAVEN_PROJECT_DIST'] = 'zope.interface'
        browser.login().open(view='ftw.raven-config.js')
        config = self.extract_config_from_javascript(browser.contents)
        version = get_distribution('zope.interface').version
        self.assertDictContainsSubset({'release': version}, config['options'])

    @browsing
    def test_tags_in_config_args(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        os.environ['RAVEN_TAGS'] = '{"deployment_type": "demo"}'
        browser.login().open(view='ftw.raven-config.js')
        config = self.extract_config_from_javascript(browser.contents)
        self.assertDictContainsSubset({'tags': {'deployment_type': 'demo'}},
                                      config['options'])

    def extract_config_from_javascript(self, js):
        js = re.sub('^var raven_config = ', '', js)
        js = re.sub(';$', '', js)
        return json.loads(js)
