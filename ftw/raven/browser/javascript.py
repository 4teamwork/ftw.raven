from ftw.raven import reporter
from ftw.raven.config import get_raven_config
from Products.Five.browser import BrowserView
import json
import os
import re
import socket


class RavenJavaScript(BrowserView):

    def __call__(self):
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        self.request.response.setHeader(
            'Content-Type', 'application/javascript; charset=utf-8')
        if not get_raven_config().enabled:
            return ''

        return '\n'.join((self.get_raven_js(),
                          '',
                          self.get_config_js()))

    def get_raven_js(self):
        path = os.path.join(os.path.dirname(__file__),
                            'resources',
                            'raven.min.js')
        with open(path, 'r') as shim:
            return shim.read()

    def get_config_js(self):
        return '\n'.join((
            '/* Raven Configuration: */',
            'Raven.setUserContext({});'.format(
                json.dumps(
                    reporter.prepare_user_infos(self.context, self.request,
                                                include_roles=False))),

            'Raven.config("{}", {}).install();'.format(
                self._get_dsn_without_private_key(),
                json.dumps(self._get_install_args()))))

    def _get_install_args(self):
        args = {}

        release = reporter.get_release()
        if release:
            args['release'] = release

        if hasattr(socket, 'gethostname'):
            args['serverName'] = socket.gethostname()

        return args

    def _get_dsn_without_private_key(self):
        dsn = get_raven_config().dsn
        return re.sub(r'(://[^:]*):[^@]*(@)', '\g<1>\g<2>', dsn)
