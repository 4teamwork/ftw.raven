from ftw.raven.client import get_raven_client
from ftw.raven.client import purge_raven_client
from ftw.raven.testing import RAVEN_FUNCTIONAL
from ftw.raven.tests.client_mock import ClientMock
from ftw.testbrowser import Browser
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = RAVEN_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.load_zcml_string = self.layer['load_zcml_string']
        ClientMock.install()

    def tearDown(self):
        purge_raven_client()

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, roles)
        transaction.commit()

    def request_to_error_view(self, view='make_key_error', data=None,
                              login_as=None):
        # We need to make sure that the raven client mock is created
        # in this thread and not in the sub-thread created by the
        # testbrowser, in order to be able to read it later.
        get_raven_client()

        with Browser()(self.layer['app']) as browser:
            if login_as:
                browser.login(login_as)

            self.disable_handle_errors(browser)
            try:
                browser.open(view=view, data=data)
            except:
                pass

    def disable_handle_errors(self, browser):
        """If the testbrowser tells zope to not handle errors, as it does
        by default, the exception handling is not triggered, thus no errors
        are reported to sentry.
        In order to be able to test the reporting, we therefore need to
        enable error handling by removing the header.
        """
        header = ('X-zope-handle-errors', 'False')
        mechbrowser = browser.get_mechbrowser()
        if header in mechbrowser.addheaders:
            mechbrowser.addheaders.remove(header)
