from ftw.raven.config import get_raven_config
import raven


raven_client_class = raven.Client
_client_cache = None


def get_raven_client():
    config = get_raven_config()
    if not config.enabled:
        return None

    if globals().get('_client_cache', None) is not None:
        return globals()['_client_cache']

    globals()['_client_cache'] = raven_client_class(
        dsn=config.dsn,
        install_sys_hook=False)
    return globals()['_client_cache']


def purge_raven_client():
    globals()['_client_cache'] = None
