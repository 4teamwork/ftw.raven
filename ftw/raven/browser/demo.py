from Products.Five.browser import BrowserView


class RavenConnectionTest(ValueError):
    pass


class MakeError(BrowserView):

    def __call__(self):
        raise RavenConnectionTest(self.request.form)
