import os


def get_raven_config():
    return RavenConfig()


class RavenConfig(object):

    @property
    def enabled(self):
        return self.dsn is not None

    @property
    def dsn(self):
        return self._get_stripped_env_variable('RAVEN_DSN')

    @property
    def project_dist(self):
        return self._get_stripped_env_variable('RAVEN_PROJECT_DIST')

    @property
    def buildout_root(self):
        return self._get_stripped_env_variable('RAVEN_BUILDOUT_ROOT')

    @property
    def ignored_exception_classnames(self):
        ignored = set(['Redirect', 'NotFound', 'Unauthorized'])
        enabled = self._get_stripped_env_variable('RAVEN_ENABLE_EXCEPTIONS')
        if enabled:
            ignored -= set(map(str.strip, enabled.split(',')))

        return tuple(ignored)

    def _get_stripped_env_variable(self, name):
        value = os.environ.get(name, '')
        if value.strip():
            return value.strip()
        else:
            return None
