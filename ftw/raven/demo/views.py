from Products.Five.browser import BrowserView


class MakeKeyError(BrowserView):

    def __call__(self):
        raise KeyError(*self.request.form.values())
