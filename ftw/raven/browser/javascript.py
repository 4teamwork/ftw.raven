from ftw.raven import reporter
from ftw.raven.config import get_raven_config
from Products.Five.browser import BrowserView
import json
import os
import re
import socket


class RavenUserConfiguration(BrowserView):

    def __call__(self):
        if not get_raven_config().enabled:
            return ''

        config = {
            'dsn': self._get_dsn_without_private_key(),
            'options': self._get_install_args(),
            'user_context': reporter.prepare_user_infos(
                self.context, self.request,
                include_roles=False)}

        return 'var raven_config = {};'.format(
            json.dumps(config, sort_keys=True, indent=4))

    def _get_install_args(self):
        args = {}

        release = reporter.get_release()
        if release:
            args['release'] = release

        if hasattr(socket, 'gethostname'):
            args['serverName'] = socket.gethostname()

        tags = reporter.get_default_tags()
        if tags:
            args['tags'] = tags

        return args

    def _get_dsn_without_private_key(self):
        dsn = get_raven_config().dsn
        return re.sub(r'(threaded\+requests\+)?([^:]*://[^:]*):[^@]*(@)', '\g<2>\g<3>', dsn)


class RavenJavaScript(BrowserView):

    def __call__(self):
        self.request.response.setHeader('X-Theme-Disabled', 'True')
        self.request.response.setHeader(
            'Content-Type', 'application/javascript; charset=utf-8')
        return '\n\n'.join((self.get_resource_content('raven.min.js'),
                            self.get_resource_content('raven-integration.js')))

    def get_resource_content(self, filename):
        path = os.path.join(os.path.dirname(__file__),
                            'resources',
                            filename)
        with open(path, 'r') as shim:
            return shim.read()
