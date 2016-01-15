from ftw.raven.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from pkg_resources import get_distribution
import json
import os
import re


class TestJavaScript(FunctionalTestCase):

    @browsing
    def test_empty_when_not_configured(self, browser):
        browser.login().open(view='ftw.raven.js')
        self.assertEquals('', browser.contents)

    @browsing
    def test_headers(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven.js')
        self.assertEquals('application/javascript; charset=utf-8',
                          browser.headers['Content-Type'])
        self.assertEquals('True',
                          browser.headers.get('X-Theme-Disabled'))

    @browsing
    def test_user_context_configured(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven.js')
        _shim, config = browser.contents.split('/* Raven Configuration: */')

        match = re.compile(r'Raven.setUserContext\(([^\)]*)\);').search(config)
        self.assertTrue(match, 'Could not find Raven.setUserContext config')
        user_context_config = json.loads(match.group(1))
        self.assertEquals({'username': 'test-user',
                           'authentication': 'authenticated',
                           'fullname': '',
                           'ip_address': '',
                           'id': 'test_user_1_',
                           'email': ''}, user_context_config)

    @browsing
    def test_dsn_configured(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven.js')
        _shim, config = browser.contents.split('/* Raven Configuration: */')

        match = re.compile(r'Raven.config\("([^,]*)",').search(config)
        # The private key (:y) should not be included.
        self.assertEquals('https://x@sentry.local/1', match.group(1))

    @browsing
    def test_server_name_in_config_args(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        browser.login().open(view='ftw.raven.js')
        _shim, config = browser.contents.split('/* Raven Configuration: */')
        xpr = re.compile(r'Raven.config\("[^"]*", ([^\)]*)\)')
        self.assertRegexpMatches(config, xpr)
        match = xpr.search(config)
        config_args = json.loads(match.group(1))

        self.assertIn('serverName', config_args)

    @browsing
    def test_release_in_config_args(self, browser):
        os.environ['RAVEN_DSN'] = 'https://x:y@sentry.local/1'
        os.environ['RAVEN_PROJECT_DIST'] = 'zope.interface'
        browser.login().open(view='ftw.raven.js')
        _shim, config = browser.contents.split('/* Raven Configuration: */')
        xpr = re.compile(r'Raven.config\("[^"]*", ([^\)]*)\)')
        self.assertRegexpMatches(config, xpr)
        match = xpr.search(config)
        config_args = json.loads(match.group(1))

        version = get_distribution('zope.interface').version
        self.assertDictContainsSubset({'release': version}, config_args)
