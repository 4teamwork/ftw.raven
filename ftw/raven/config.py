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

    def _get_stripped_env_variable(self, name):
        value = os.environ.get(name, '')
        if value.strip():
            return value.strip()
        else:
            return None
