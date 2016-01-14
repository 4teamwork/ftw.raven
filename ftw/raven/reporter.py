from AccessControl.users import nobody
from Acquisition import aq_acquire
from ftw.raven.client import get_raven_client
from yolk.yolklib import Distributions
import logging
import sys


LOG = logging.getLogger('ftw.raven.reporter')


def maybe_report_exception(context, request, *exc_info):
    try:
        client = get_raven_client()
        if client is None:
            return

        try:
            data = {'request': prepare_request_infos(request),
                    'user': prepare_user_infos(context, request),
                    'extra': prepare_extra_infos(context, request),
                    'modules': prepare_modules_infos()}
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


def prepare_user_infos(context, request):
    user = request.get('AUTHENTICATED_USER', nobody)

    data = {'ip_address': request.getClientAddr(),
            'roles': user.getRoles(),
            'roles_in_context': user.getRolesInContext(context)}

    if user and user != nobody:
        data.update({'id': user.getId(),
                     'username': user.getUserName(),
                     'email': user.getProperty('email', ''),
                     'fullname': user.getProperty('fullname', ''),
                     'authentication': 'authenticated'})
    else:
        data.update({'authentication': 'anonymous'})

    return data


def prepare_modules_infos():
    dists = (dist for (dist, active) in Distributions().get_distributions('all')
             if active)
    modules = dict((dist.project_name, dist.version) for dist in dists)
    modules['python'] = sys.version_info
    return modules


def prepare_extra_infos(context, request):
    return {'context': context,
            'request.other': request.other.copy()}
