from ftw.raven.reporter import maybe_report_exception
from plone.app.linkintegrity import monkey
from plone.app.linkintegrity.monkey import zpublisher_exception_hook_wrapper


def zpublisher_exception_hook_wrapper_wrapper(published, REQUEST,
                                              t, v, traceback):
    """Wrapper around linkintegrity's wrapper around zopes exception hook.
    This allows us to hook into the exception handling for
    reporting exceptions.
    """
    maybe_report_exception(published, REQUEST, t, v, traceback)
    return zpublisher_exception_hook_wrapper(published, REQUEST,
                                             t, v, traceback)


def install_patches():
    monkey.zpublisher_exception_hook_wrapper = (
        zpublisher_exception_hook_wrapper_wrapper)
