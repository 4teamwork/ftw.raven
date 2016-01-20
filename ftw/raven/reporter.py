from AccessControl.users import nobody
from Acquisition import aq_acquire
from ftw.raven.client import get_raven_client
from ftw.raven.config import get_raven_config
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution
from plone.memoize import forever
from raven import fetch_git_sha
from raven.exceptions import InvalidGitRepository
from yolk.yolklib import Distributions
import logging
import sys


LOG = logging.getLogger('ftw.raven.reporter')


def maybe_report_exception(context, request, exc_type, exc, traceback):
    if is_exception_type_ignored(exc_type):
        return

    exc_info = exc_type, exc, traceback
    try:
        client = get_raven_client()
        if client is None:
            return

        try:
            data = {'request': prepare_request_infos(request),
                    'user': prepare_user_infos(context, request),
                    'extra': prepare_extra_infos(context, request),
                    'modules': prepare_modules_infos(),
                    'tags': prepare_tags(exc)}
            release = get_release()
            if release:
                data['release'] = release
        except:
            LOG.error('Error while preparing sentry data.')
            raise

        try:
            client.captureException(exc_info=exc_info, data=data)
        except:
            LOG.error('Error while reporting to sentry.')
            raise

    except:
        if context:
            aq_acquire(context, 'error_log').raising(sys.exc_info())
        try:
            get_raven_client().captureException(
                data={'extra': {
                    'raven_meta_error': 'Error occured while reporting'
                    ' another error.'}})
        except:
            LOG.error('Failed to report error occured while reporting error.')


def is_exception_type_ignored(exc_type):
    if exc_type is None:
        return True
    ignored_classnames = get_raven_config().ignored_exception_classnames
    return exc_type.__name__ in ignored_classnames


def prepare_request_infos(request):
    headers = {}
    environ = {}
    for key, value in request.environ.items():
        if key.upper().startswith('HTTP'):
            # HTTP_USER_AGENT -> User-Agent
            key = key[5:].replace('_', '-').title()
            headers[key] = value
        else:
            environ[key] = value

    return {
        'url': request.URL,
        'method': request.method,
        'data': request.form.copy(),
        'query_string': request.QUERY_STRING,
        'cookies': request.cookies.copy(),
        'headers': headers,
        'env': environ,
    }


def prepare_user_infos(context, request, include_roles=True):
    user = request.get('AUTHENTICATED_USER', nobody)

    data = {'ip_address': get_client_ip_address(request)}
    if include_roles:
        data['roles'] = user.getRoles()
        data['roles_in_context'] = user.getRolesInContext(context)

    if user and user != nobody:
        data.update({'id': user.getId(),
                     'username': user.getUserName(),
                     'email': user.getProperty('email', ''),
                     'fullname': user.getProperty('fullname', ''),
                     'authentication': 'authenticated'})
    else:
        data.update({'authentication': 'anonymous'})

    return data


def get_client_ip_address(request):
    """Returns the IP address of the host which sent the
    request initally.
    """
    ips = request.environ.get(
        'HTTP_X_FORWARDED_FOR',
        request.environ.get('REMOTE_ADDR'))

    if ips is None:
        return ''
    elif not hasattr(ips, 'split'):
        return ips
    else:
        return ips.split(',')[0].strip()


def prepare_modules_infos():
    dists = (dist for (dist, active)
             in Distributions().get_distributions('all')
             if active)
    modules = dict((dist.project_name, dist.version) for dist in dists)
    modules['python'] = '.'.join(map(str, sys.version_info[:3]))
    return modules


def prepare_tags(exc):
    tags = get_default_tags()
    if hasattr(exc, 'error_log_id'):
        tags['error_log_id'] = exc.error_log_id
    return tags


@forever.memoize
def get_default_tags():
    return get_raven_config().tags.copy()


def get_release():
    config = get_raven_config()
    if config.project_dist:
        try:
            return get_distribution(config.project_dist).version
        except DistributionNotFound:
            LOG.error('The distribution "{}" could not be found.'.format(
                config.project_dist))
            return None

    if config.buildout_root:
        try:
            return fetch_git_sha(config.buildout_root)
        except InvalidGitRepository:
            LOG.error('The path {} does not exist or is not'
                      ' a git repository'.format(config.buildout_root))
            return None

    return None


def prepare_extra_infos(context, request):
    return {'context': context,
            'request.other': request.other.copy()}
