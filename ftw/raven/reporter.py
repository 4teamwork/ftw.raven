from ftw.raven.client import get_raven_client


def maybe_report_exception(context, request, *exc_info):
    if get_raven_client() is None:
        return

    get_raven_client().captureException(exc_info=exc_info)
