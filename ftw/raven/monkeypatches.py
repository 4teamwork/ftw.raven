from App.ZApplication import ZApplicationWrapper
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


def install_patches():
    monkey.zpublisher_exception_hook_wrapper = (
        zpublisher_exception_hook_wrapper_wrapper)
    ZApplicationWrapper.__repr__ = ZApplicationWrapper__repr__
