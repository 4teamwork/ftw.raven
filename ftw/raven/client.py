from ftw.raven.config import get_raven_config
import raven


raven_client_class = raven.Client
_client_cache = None


def get_raven_client():
    if globals().get('_client_cache', None) is not None:
        return globals()['_client_cache']

    config = get_raven_config()
    if config is not None:
        globals()['_client_cache'] = raven_client_class(**vars(config))
        return globals()['_client_cache']
    else:
        return None


def purge_raven_client():
    globals()['_client_cache'] = None
