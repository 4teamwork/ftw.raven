from App.ZApplication import ZApplicationWrapper
from ftw.raven.reporter import maybe_report_exception
from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
from ZODB.POSException import ConflictError
from ZPublisher.Publish import Retry
from Zope2.App.startup import ZPublisherExceptionHook
import re
import sys


def exception_hook_wrapper(self, published, REQUEST, t, v, traceback):
    report_exception = True
    args = [published, REQUEST, t, v, traceback]

    try:
        try:
            return self.__ori_call__(*args)

        except Retry:
            # There was probably a conflict, resulting in a Retry
            # and the request will be done once again completely.
            report_exception = False
            raise

        except ConflictError:
            # This request was probably executed 3 times
            # (with Retry-exceptions, see above) but could not be
            # finished because of a ConflictError.
            # We want to report the ConflictError now, that's why
            # we replace the previous exception (which was probably
            # a Retry exception) with our ConflictError.
            args[-3:] = sys.exc_info()
            report_exception = True
            raise

    finally:
        if report_exception:
            maybe_report_exception(*args)


def ZApplicationWrapper__repr__(self):
    """ZApplicationWrapper has no __repr__ because it does not inherit
    from object.
    For having stack locals in sentry, the raven client tries to make
    repr() for each object, which fails with the ZApplicationWrapper
    because there is no implementation.
    Therefore we add the __repr__ to the ZApplicationWrapper class.
    """
    mod = self.__class__.__module__
    cls = self.__class__.__name__
    mem = '0x' + hex(id(self))[2:].zfill(8).upper()
    return '<{0}.{1} instance at {2}>'.format(mod, cls, mem)


def SiteErrorLog_raising_wrapper(self, info):
    """The default error_log assigns random, not guessable IDs to errors.
    The return value of ``raising`` is usually the URL to the error_log
    entry identified by its ID.
    In order to be able to report the error_log ID to sentry later,
    we store it on the exception.
    """
    result = self.raising_original(info)
    if not info[1] or not isinstance(result, (str, unicode)):
        return result

    match = re.match('.*error_log/showEntry\?id=([\d\.]*)$', result)
    if match:
        info[1].error_log_id = match.group(1)

    return result


def install_patches():
    ZPublisherExceptionHook.__ori_call__ = ZPublisherExceptionHook.__call__
    ZPublisherExceptionHook.__call__ = exception_hook_wrapper
    ZApplicationWrapper.__repr__ = ZApplicationWrapper__repr__
    if SiteErrorLog.raising != SiteErrorLog_raising_wrapper:
        SiteErrorLog.raising_original = SiteErrorLog.raising
        SiteErrorLog.raising = SiteErrorLog_raising_wrapper
