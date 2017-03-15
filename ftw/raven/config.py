import json
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
        ignored = set(['Redirect', 'NotFound', 'Unauthorized', 'Intercepted'])
        enabled = self._get_stripped_env_variable('RAVEN_ENABLE_EXCEPTIONS')
        if enabled:
            ignored -= set(map(str.strip, enabled.split(',')))

        disabled = self._get_stripped_env_variable('RAVEN_DISABLE_EXCEPTIONS')
        if disabled:
            ignored |= set(map(str.strip, disabled.split(',')))

        return tuple(ignored)

    @property
    def tags(self):
        value = self._get_tags_from_file()
        value.update(self._get_tags_from_env())
        return value

    def _get_tags_from_env(self):
        value = self._get_stripped_env_variable('RAVEN_TAGS')
        if not value:
            return {}

        try:
            return json.loads(value)
        except ValueError:
            return {'RAVEN_TAGS': 'invalid configuration'}

    def _get_tags_from_file(self):
        value = self._get_stripped_env_variable('RAVEN_TAGS_FILE')
        if not value:
            return {}

        if not os.path.isfile(value):
            return {'RAVEN_TAGS_FILE': 'missing file'}

        try:
            with open(value) as tags_file:
                return json.load(tags_file)
        except ValueError:
            return {'RAVEN_TAGS_FILE': 'invalid content'}

    def _get_stripped_env_variable(self, name):
        value = os.environ.get(name, '')
        if value.strip():
            return value.strip()
        else:
            return None
