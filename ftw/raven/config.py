import os


def get_raven_config():
    return RavenConfig()


class RavenConfig(object):

    @property
    def enabled(self):
        return self.dsn is not None

    @property
    def dsn(self):
        value = os.environ.get('RAVEN_DSN', '')
        if value.strip():
            return value.strip()
        else:
            return None
